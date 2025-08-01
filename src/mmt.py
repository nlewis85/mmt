import sys
import os
import threading
import time

from helpers.parser import *


def main():
    """ Main """
    try: 
        args = parse_args()
    except Exception as error:
        print("Error: ", error)
    
    intitial_message=f"""
    Welcome to MMT (My MultiTool)
    Mode: {args.mode}
    File: {args.file}
    Verbosity: {args.verbose}
    Parallel Tasks: {args.parallel}
    """
    
    print(intitial_message)
    
    #DEBUG tasks = load_file(args.file)
    ordered_tasks, errors = validate_tasks(load_file(args.file))

    #DEBUG print(ordered_tasks)
    print(f"{len(errors)} Errors Found")
    if len(errors) > 0:
        print(errors)
    print("-- Script Complete --")


if __name__ == "__main__":
    main()