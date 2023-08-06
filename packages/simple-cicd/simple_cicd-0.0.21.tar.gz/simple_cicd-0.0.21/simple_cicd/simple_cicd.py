#! /bin/python3
"""
SIMPLE CI: Dead simple CI/CD pipeline executor.
author: François Sevestre
email: francois.sevestre.35@gmail.com
"""

############## Imports   ###########
import sys
from getpass import getpass
import argparse

from simple_cicd.functions import \
        log,                      \
        manage_hook,              \
        create_example_file,      \
        get_root_dir,             \
        get_pipeline_data,        \
        end_of_pipeline,          \
        command_execution         \

from simple_cicd.script_parsing import \
        parse

############## Main ###############################################################################
def main():
    """
    Main function, call with simpleci command.
    """

    ### Arguments parsing #########################################################################
    parser = argparse.ArgumentParser(                     \
            prog="simpleci",                              \
            description="Dead simple pipeline executor.", \
            )
    selector = parser.add_subparsers(dest='selector') # Create parsers for subcommands
    # start
    start_parser = selector.add_parser('start', help="Create the git hook.")
    #       --sudo
    start_parser.add_argument("-S","--sudo",\
            help="Make simpleci use sudo priviledges when triggered.", action="store_true")
    # exec
    exec_parser = selector.add_parser('exec', help="Execute the pipeline.")
    #      --file
    exec_parser.add_argument("-f","--file", help="Specify a file to use as pipeline.")
    #      --sudo
    exec_parser.add_argument("-S","--sudo", \
            help="Execute the pipeline with sudo priviledges.", action="store_true")
    # stop
    selector.add_parser('stop', help="Delete the git hook.")
    # init
    selector.add_parser('init', help="Create the git hook and an example .simple-ci.yml file.")
    # clean
    selector.add_parser('clean', help="Remove artifacts folder.")
    # cron
    selector.add_parser('cron', help="Create a cronjob.")
    # test
    selector.add_parser('test', help="For test purpose.")
    args = parser.parse_args()
    ###############################################################################################

    ### sub-commands ##############################################################################
    if args.selector == 'start':
        start_args = parser.parse_args()                        # Checking for options
        sys.exit(not manage_hook(get_root_dir(), sudo=start_args.sudo))    # Create hook file

    elif args.selector == 'stop':
        sys.exit(not manage_hook(get_root_dir(), False))            # Delete the hook file

    elif args.selector == 'init':
        create_example_file(get_root_dir())                     # Create the .simple-ci.yml file
        sys.exit(not manage_hook(get_root_dir()))                   # start

    elif args.selector == 'cron':
        print("This feature is not implemented yet.")

    elif args.selector == 'clean':
        artifacts_dir = get_root_dir() + "-artifacts"
        if input(f"Delete {artifacts_dir} directory? (y/N)\n>") \
                in ('y', 'yes', 'Y', 'YES'):
            sys.exit(not command_execution(f"rm -rf {artifacts_dir}"))

    elif args.selector == 'test':
        # For dev purpose only
        print("Test of simpleci install succeded!")

    elif args.selector == 'exec':
        exec_args = parser.parse_args()

        # Vars initialization
        sudo_prefix = ""

        # check suplemental args
        path_to_script = ".simple-ci.yml"
        if exec_args.file:
            path_to_script = exec_args.file
        data = get_pipeline_data(get_root_dir(), str(path_to_script)) # Collect data from script

        if exec_args.sudo:
            pswd = getpass()
            sudo_prefix = f"echo {pswd} | sudo -S "

        log("\n>>>>>>\nStarting the pipeline execution\n", "green")

        try:
            parse(data, sudo_prefix)

        except TypeError:
            log("Failed to read pipeline script. Please check the syntax.", "red")
            end_of_pipeline()

        log("<<<<<\nEnd of the pipeline", "green")

if __name__ == '__main__':
    main()
