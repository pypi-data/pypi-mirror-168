"""
SIMPLE CI: Dead simple CI/CD pipeline executor.
author: François Sevestre
email: francois.sevestre.35@gmail.com

This modules contains data parsing functions and pipeline execution.
"""

import time

from simple_cicd.functions import \
        run_script,               \
        get_root_dir,             \
        end_of_pipeline,          \
        log                       \

def get_variables(data, upper_scope):
    """
    Get variables from data parsing in the right scope.
    """
    if 'variables' in data:                     # if user declared variables in global scope
        return upper_scope | data['variables']
    return upper_scope

def get_docker(data, upper_scope):
    """
    Get docker infos from data parsing in the right scope.
    """
    if 'inside_docker' in data:
        return data['inside_docker']
    return upper_scope

def get_artifacts(data):
    """
    Get artifacts from data parsing.
    """
    if 'artifacts' in data:
        return data['artifacts']
    return {}

def get_script(data, job_name):
    """
    Get command from data parsing.
    """
    if 'script' in data:         # Check if user defined script in this job
        return data['script']
    return end_of_pipeline(f"No script found in \"{job_name}\".")

def get_stages(data):
    """
    Get stages from data parsing.
    """
    if 'stages' in data:         # Check if user defined script in this job
        return data['stages']
    return False

def get_jobs(data, stage_name="No stages"):
    """
    Get stages from data parsing.
    """
    if 'jobs' in data:         # Check if user defined script in this job
        return data['jobs']
    if stage_name != "No stages":
        return end_of_pipeline(f"No jobs found fo the stage \"{stage_name}\".")
    return False

def parse(data, sudo_prefix):
    """
    Parses and executes pipeline.
    """
    time_summary = "Execution times:\n----------------\n"

    ### Global scope ###
    global_env = get_variables(data, {})        # Variables
    global_docker = get_docker(data, {})        # Inside docker
    global_artifacts = get_artifacts(data)  # Artifacts

    # stages
    if stages:=get_stages(data):
        for stage in stages:
            ### Stage scope ###
            stage_name = str(stage)
            stage_start_time = time.time()
            stage = data[stage]                                 # get data from stage
            stage_env = get_variables(stage, global_env)        # variables
            stage_docker = get_docker(stage, global_docker)     # Inside docker

            log("###### Stage \'" + stage_name + "\' ######\n", "green")

            # Jobs
            if jobs:=get_jobs(stage, stage_name):       # Check if user declared jobs in this stage
                job_time_summary = ""
                for job in jobs:
                    job_name = str(job)
                    run_name = ''.join(e for e in stage_name+"_"+job_name if e.isalnum())
                    log("#### Job \'" + job_name + "\' ####", "green")

                    ### Job scope ###
                    job = data[job]                             # get data from job
                    job_env = get_variables(job, stage_env)     # variables
                    job_docker = get_docker(job, stage_docker)  # Inside docker
                    job_artifacts = get_artifacts(job)          # Artifacts

                    # Script
                    if job_script:=get_script(job, job_name):

                        script_parameters = [       \
                                job_script,         \
                                job_env,            \
                                job_docker,         \
                                job_artifacts,      \
                                get_root_dir(),     \
                                sudo_prefix,        \
                                run_name            \
                                ]
                        exec_time = run_script(script_parameters)
                        job_time_summary += \
                            f"|-->\t{job_name} ({float(f'{exec_time:.2f}')}s)\n"

                stage_exec_time = time.time() - stage_start_time
                time_summary += f"{stage_name} ({float(f'{stage_exec_time:.2f}')}s)\n"
                time_summary += job_time_summary

    # Jobs
    else:
        if jobs:=get_jobs(data):                 # Check if user declared jobs in this stage
            job_time_summary = ""
            for job in jobs:
                job_name = str(job)
                run_name = job_name
                run_name = ''.join(e for e in run_name if e.isalnum())
                log("#### Job \'" + job_name + "\' ####", "green")

                ### Job scope ###
                job = data[job]
                job_env = get_variables(job, global_env)     # variables
                job_docker = get_docker(job, global_docker)  # Inside docker
                job_artifacts = get_artifacts(job)           # Artifacts

                # Script
                if job_script:=get_script(job, job_name):

                    script_parameters = [       \
                            job_script,         \
                            job_env,            \
                            job_docker,         \
                            job_artifacts,      \
                            get_root_dir(),     \
                            sudo_prefix,        \
                            run_name            \
                            ]
                    exec_time = run_script(script_parameters)
                    job_time_summary += f"{job_name} ({float(f'{exec_time:.2f}')}s)\n"

                time_summary += job_time_summary

    # Script
        else:
            run_name = "simple"
            if global_script:=get_script(data, "pipeline"):
                script_parameters = [       \
                        global_script,      \
                        global_env,         \
                        global_docker,      \
                        global_artifacts,   \
                        get_root_dir(),     \
                        sudo_prefix,        \
                        run_name            \
                        ]
                exec_time = run_script(script_parameters)
                time_summary += f"Script ({float(f'{exec_time:.2f}')}s)\n"

    log(time_summary, "blue")
