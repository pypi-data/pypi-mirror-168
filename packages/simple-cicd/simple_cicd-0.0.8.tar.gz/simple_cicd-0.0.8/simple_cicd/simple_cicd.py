#! /bin/python3
"""
SIMPLE CI: Dead simple CI/CD pipeline executor.
author: François Sevestre
email: francois.sevestre.35@gmail.com
"""

############## Imports   ##############
import sys
import os
import time
from subprocess import getoutput, PIPE, run
from datetime import datetime
import yaml

############## Functions ##############
def get_root_dir():
    """ Get the root directory of the git repo.
    Returns:
        An absolute path.
    """
    return getoutput("git rev-parse --show-toplevel")

def get_git_branch():
    """ Get the current git branch.
    Returns:
        A string, the name of the branch.
    """
    return getoutput("git branch | grep '*' | awk '{print $2}'")

def manage_hook(git_root_dir, present=True):
    """ Creates or remove the hook from the .git/hook/ folder.

    Args:
        present (bool): True -> create, False -> remove
    Returns:
        A bool.
    Raises:
        FileExistsError: The file already exists, can't be created.
        FileNotFoundError: The file doesn't exists, can't delete.
    """

    # Git hook script
    pre_commit_hook = """
    #!/bin/env bash

    simpleci exec
    """
    # manage hook
    if present:                                             # Create the hook file
        with open(git_root_dir+"/.git/hooks/pre-commit", 'w', encoding="utf-8") as file:
            file.write(pre_commit_hook)
        os.chmod(git_root_dir+"/.git/hooks/pre-commit", 0o755)
        print("Git hook created.                                 \
            \nIt will execute the pipeline before the next commit.\
            \nAlternatively, you can trigger the pipeline with \'simple-ci exec\'")
    else:
        os.remove(git_root_dir+"/.git/hooks/pre-commit")   # Remove the hook file
    return True

def create_example_file(git_root_dir):
    """
    Creates an example .simple-ci.yml file at the git root dir if it doesn't exists
    """
    # Example
    example_file_data = \
"""---
variables:
  GLOBAL_VAR: "last"

stages:
  - stage1
  - stage2

stage1:
  variables:
    MYVAR: "second"
  jobs:
    - job1
    - job2

stage2:
  inside_docker:
    image: ruby:2.7
    path: /tmp/
  jobs:
    - job3

job1:
  script:
    - echo "This is the first job."

job2:
  inside_docker:
    image: ruby:2.7
    path: /tmp/
  script:
    - echo "This is the $MYVAR job."

job3:
    script:
    - echo "This is the $GLOBAL_VAR job, that will be executed after stage1 is completed."
"""
    # check if file exists
    if os.path.isfile(git_root_dir+"/.simple-ci.yml"):
        print("File exists: Example creation skipped.")
    else:
        # create file
        with open(git_root_dir+"/.simple-ci.yml", 'w', encoding="utf-8") as file:
            file.write(example_file_data)
        print("The .simple-ci.yml file has been created. Check it, try it and customize it!")

def get_pipeline_data(git_root_dir, ci_script=".simple-ci.yml"):
    """ Get the pipeline data from file.
    Returns:
        A dict.
    """
    try:
        yaml_data = False
        with open(git_root_dir+"/"+ci_script, 'r', encoding="utf-8") as file:
            yaml_data = yaml.load(file, Loader=yaml.Loader)
        return yaml_data
    except FileNotFoundError:
        log("Pipeline file not found", "red")
        sys.exit(1)

def log(line, color=""):
    """ Prints line and saves it to simple.log file
    Args:
        line (str)
        color (bool)
    """
    with open("simple.log", 'a', encoding="utf-8") as log_file:
        log_file.write(line+"\n")
    if color == "green":
        print("\033[32m"+line+"\033[0m")
    elif color == "red":
        print("\033[31m"+line+"\033[0m")
    elif color == "blue":
        print("\033[36m"+line+"\033[0m")
    else:
        print(line)

def command_execution(command_to_execute):
    """
    Executes the given command, manage logs and exit pipeline if necessary
    """
    res = run(command_to_execute, shell=True, stdout=PIPE, stderr=PIPE, \
            universal_newlines=True, check=False)
    log(res.stdout)
    if res.returncode != 0:
        log(f"return code: {res.returncode}", "red")
        log(res.stdout, "red")
        return False
    return True

def exec_script_command(script_command, env):
    """  Execute a command with a given env
    Args:
        command (str)
        env (dict)
    """
    env_cmd = "true"

    for var_key in env:                                         # Add env variables declaration
        env_cmd = env_cmd + \
                " && " +    \
                var_key + "=\"" + str(env[var_key]) + "\""

    passed_command = "bash -c \'" + \
            env_cmd +               \
            " && " +                \
            script_command +        \
            "\'"                                                # Assemble final command
    return command_execution(passed_command)

def create_container(docker_image):
    """
    Creates a docker container of the specified image.
    Returns:
        container_hash (str)
    """
    cont = getoutput("docker run -td " + docker_image) # Create container
    cont = cont.split(sep='\n')[-1][0:11]
    # os.system("docker container start " + cont + " > /dev/null")          # start container
    return cont

def exec_script_command_in_docker(script_command, env, cont_id):
    """
    Execute a command with the given env in the given container.
    """
    env_cmd = "true"

    for var_key in env:                                         # Add env variables declaration
        env_cmd = env_cmd + \
                " && " +    \
                var_key + "=\"" + str(env[var_key]) + "\""

    passed_command = "sh -c \'" + \
            env_cmd +             \
            " && " +              \
            script_command +      \
            "\'"                                                # Assemble final command
    full_command = "docker exec " + cont_id + " " + passed_command+ " \n"
    return command_execution(full_command)

def copy_files_to_docker(cont_id, path): # TODO Function impure
    """
    Copies the current git folder to container at the given path.
    """
    log(f"Files will be copied to the container {cont_id} at \'{path}\'", "blue")
    # os.system(f"cp -r . {get_root_dir()}_simple-ci/" )
    os.system(f"docker cp . {cont_id}:{path}")

def stop_container(cont_id):
    """
    Stops a docker container.
    """
    os.system("docker rm -f " + cont_id + " > /dev/null")

def create_artifacts_folder(git_root_dir):
    """
    Creates an artifacts folder next to the git folder with same name + '-artifacts'.
    Also creates a sub-folder name after launch time.
    """
    artifacts_dir_to_be_created = git_root_dir+"-artifacts"
    try:
        os.mkdir(artifacts_dir_to_be_created)       # Create the common artifacts folder
        print("Artifacts folder created.")
    except FileExistsError:
        pass
    run_dir = os.path.join(artifacts_dir_to_be_created,\
            datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    try:
        os.mkdir(run_dir)             # Create the run folder
    except FileExistsError:
        print("Run folder already exists. (last one created less than a second ago)")
    return run_dir

def run_script(script_parameters_to_run):
    """Execution of the script commands on the given env"""

    script_to_run = script_parameters_to_run[0]
    job_env_to_run = script_parameters_to_run[1]
    job_docker_to_run = script_parameters_to_run[2]
    job_artifacts_to_run = script_parameters_to_run[3]
    git_root_dir = script_parameters_to_run[4]

    start_script_time = time.time()

    # Prepare artifacts folder
    if job_artifacts_to_run:
        current_artifacts_dir = create_artifacts_folder(git_root_dir)
    else:
        current_artifacts_dir = create_artifacts_folder("/tmp/simpleci")

    if job_docker_to_run != {}: # For inside_docker execution
        log(f"A \'{job_docker_to_run['image']}\' container is required.", "blue")
        container_id = create_container(job_docker_to_run['image'])     # Creating container
        log(f"Container \'{container_id}\' as been created.", "blue")
        copy_files_to_docker(container_id, job_docker_to_run['path'])   # copy files to docker
        for command in script_to_run:                                   # Exec script in docker
            log("## > " + str(command), "green")
            if not exec_script_command_in_docker(command, job_env_to_run, container_id):
                stop_container(container_id)                                    # Kill container
                end_of_pipeline()


        # Artifacts
        if job_artifacts_to_run:
            paths = job_artifacts_to_run['paths']
            for file in paths:
                os.system(f"docker cp {container_id}:{file} {current_artifacts_dir}")
                log(f"Artifact \"{file}\" saved in {current_artifacts_dir}.", "blue")

        stop_container(container_id)                                    # Kill container

    else: # for local execution

        tmp_artifacts_dir = "/tmp/" + os.path.basename(current_artifacts_dir)
        os.system(f"cp -r {git_root_dir} {tmp_artifacts_dir} 2> /dev/null")

        current_dir = os.getcwd()
        os.chdir(tmp_artifacts_dir)
        for command in script_to_run:
            log("## > " + str(command), "green")
            if not exec_script_command(command, job_env_to_run):
                end_of_pipeline()

        # Artifacts
        if job_artifacts_to_run:
            paths = job_artifacts_to_run['paths']
            for file in paths:
                os.system(f"cp -r -t {current_artifacts_dir} {tmp_artifacts_dir}/{file} ")
                log(f"Artifact \"{file}\" saved in {current_artifacts_dir}.", "blue")

        os.chdir(current_dir)
    stop_script_time = time.time()
    return stop_script_time - start_script_time

def end_of_pipeline():
    """
    Display a message when pipeline failed and exits with error.
    """
    log("Pipeline failed.", "red")
    sys.exit(1)

############## Main ##############
def main():
    args = sys.argv
    script_name = args.pop(0)                       # Remove script name from the list
    SELECTOR = args[0]
    if len(args) > 1:
        OPTIONS = args[1:]
    else:
        OPTIONS = [False]

    if SELECTOR == "start":
        sys.exit(manage_hook(get_root_dir()))       # Create the hook file

    elif SELECTOR == "stop":
        sys.exit(manage_hook(get_root_dir(), False))# Delete the hook file

    elif SELECTOR == "init":
        create_example_file(get_root_dir())         # Create the .simple-ci.yml file
        sys.exit(manage_hook(get_root_dir()))       # start

    elif SELECTOR == "exec":                        # Execution of the .simple-ci.yml script
        time_summary = "Execution times:\n----------------\n"

        # check suplemental args
        if OPTIONS[0] in ("--file", "-f"):
            path_to_script = OPTIONS[1]
            data = get_pipeline_data(get_root_dir(), str(path_to_script)) # Collect data from script
        else:
            data = get_pipeline_data(get_root_dir())    # Collect data from script

        log("\n>>>>>>\nStarting the pipeline execution\n", "green")
        ### Global scope ###

        try:
            # Variables
            if 'variables' in data:                     # if user declared variables in global scope
                global_env = data['variables']
            else:
                global_env = {}

            # Inside docker                             # if user declared a docker (global scope)
            if 'inside_docker' in data:
                global_docker = data['inside_docker']
            else:
                global_docker = {}

            # Artifacts
            if 'artifacts' in data:
                global_artifacts = data['artifacts']
            else:
                global_artifacts = {}

            # stages
            if 'stages' in data:                        # if user declared stages in global scope
                for stage in data['stages']:
                    STAGE_NAME = str(stage)
                    stage_start_time = time.time()
                    log("###### Stage \'" + STAGE_NAME + "\' ######\n", "green")

                    ### Stage scope ###
                    stage = data[stage]                 # get data from stage

                    # variables
                    if 'variables' in stage:        # if user declared variables in the stage scope
                        stage_env = global_env | stage['variables'] # merge dicts with overwrite
                    else:
                        stage_env = global_env

                    # Inside docker
                    if 'inside_docker' in stage:    # if user declared variables in the stage scope
                        # merge dicts + overwrite
                        stage_docker = stage['inside_docker']
                    else:
                        stage_docker = global_docker

                    # Jobs
                    if 'jobs' in stage:                 # Check if user declared jobs in this stage
                        job_time_summary = ""
                        for job in stage['jobs']:
                            JOB_NAME = str(job)
                            log("#### Job \'" + JOB_NAME + "\' ####", "green")

                            ### Job scope ###
                            job = data[job]             # get data from job

                            # variables
                            if 'variables' in job:  # if user declared variables in the job scope
                                job_env = stage_env | job['variables']
                            else:
                                job_env = stage_env

                            # Inside docker
                            if 'inside_docker' in job: # if user declared variables in the job scope
                                job_docker = job['inside_docker']
                            else:
                                job_docker = stage_docker

                            # Artifacts
                            if 'artifacts' in job:
                                job_artifacts = job['artifacts']
                            else:
                                job_artifacts = {}

                            # Script
                            if 'script' in job:         # Check if user defined script in this job
                                job_script = job['script']
                                script_parameters = [job_script, job_env, job_docker, \
                                        job_artifacts, get_root_dir()]
                                exec_time = run_script(script_parameters)
                                job_time_summary += f"|-->\t{JOB_NAME} ({float(f'{exec_time:.2f}')}s)\n"
                                # log(f"Execution time: {float(f'{exec_time:.2f}')} secondes", "blue")

                            else:
                                log(f"No script found for the job \"{JOB_NAME}\".", "red")
                                end_of_pipeline()

                        stage_stop_time = time.time()
                        stage_exec_time = stage_stop_time - stage_start_time
                        time_summary += f"{STAGE_NAME} ({float(f'{stage_exec_time:.2f}')}s)\n"
                        time_summary += job_time_summary

                    else:
                        log(f"No jobs found fo the stage \"{STAGE_NAME}\".", "red")
                        end_of_pipeline()
            # Jobs
            else:
                if 'jobs' in data:                      # if user declared jobs in global scope
                    job_time_summary = ""
                    for job in data['jobs']:
                        JOB_NAME = str(job)
                        log("#### Job \'" + JOB_NAME + "\' ####", "green")

                        ### Job scope ###
                        job = data[job]

                        # variables                 # if user declared variables in the job scope
                        if 'variables' in job:
                            job_env = global_env | job['variables']
                        else:
                            job_env = global_env

                        # Inside docker             # if user declared a docker option (job scope)
                        if 'inside_docker' in job:  # if user declared variables in the job scope
                            job_docker = job['inside_docker']
                        else:
                            job_docker = global_docker

                        # Artifacts
                        if 'artifacts' in job:
                            job_artifacts = job['artifacts']
                        else:
                            job_artifacts = {}

                        # Script
                        if 'script' in job:         # Check if user defined script in this job
                            job_script = job['script']
                            script_parameters = [job_script, job_env, job_docker, \
                                    job_artifacts, get_root_dir()]
                            exec_time = run_script(script_parameters)
                            job_time_summary += f"{JOB_NAME} ({float(f'{exec_time:.2f}')}s)\n"

                        else:
                            log(f"No script found for the job \"{JOB_NAME}\".", "red")
                            end_of_pipeline()

                        time_summary += job_time_summary

            # Script
                else:
                    if 'script' in data:         # Check if user defined script in this job
                        global_script = data['script']
                        script_parameters = [global_script, global_env, global_docker, \
                                global_artifacts, get_root_dir()]
                        exec_time = run_script(script_parameters)
                        time_summary += f"Script ({float(f'{exec_time:.2f}')}s)\n"
                    else:
                        log("No script found.", "red")
                        end_of_pipeline()

        except TypeError:
            log("Failed to read pipeline script. Please check the syntax.", "red")
            end_of_pipeline()

        log(time_summary, "blue")
        log("<<<<<\nEnd of the pipeline", "green")

    elif SELECTOR == "cron":
        # TODO Create cron job
        pass

    elif SELECTOR == "clean":
        artifacts_dir = get_root_dir() + "-artifacts"
        if confirm:=input(f"Delete {artifacts_dir} directory? (y/N)\n>") \
                in ('y', 'yes', 'Y', 'YES'):
            os.system(f"rm -rf {artifacts_dir}")

    elif SELECTOR == "test":
        # For dev purpose only
        pass
    else:
        print("Wrong argument")
        sys.exit(1)


if __name__ == '__main__':
    main()
