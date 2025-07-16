import argparse
import sys

"""
Module to parse parameters and arguments used in the script.     
"""

def parse_args():
    parser = argparse.ArgumentParser(
        description="""
        MMT - My Multitool
        A small python script to allow execution of multiple other commands in parallel.
        """
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        '--execute', '-e',
        help='Execute the list of tasks from the specified file',
        action="store_true"
    )
    
    mode.add_argument(
        '--dryrun', '-d',
        help='Perform a dry run without executing any tasks',
        action="store_true"
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Specify input file path. Default is ./template.txt',
        default="template.txt"
    )
    
    parser.add_argument(
        '--parallel', '-p',
        help='Number of parallel tasks to run. Default is 3.',
        default=3,
    )
    
    parser.add_argument(
        '--verbose', '-v',
        help='Enable verbose logging',
        action='store_true'
    )
    
    parsed_args = parser.parse_args(sys.argv[1:])
    
    if parsed_args.execute:
        parsed_args.mode = 'execute'
    elif parsed_args.dryrun:
        parsed_args.mode = 'dryrun'
    
    return parsed_args