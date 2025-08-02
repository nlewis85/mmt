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
    
    ordered_tasks, time, errors = validate_tasks(load_file(args.file), args.parallel)

    # Some Debug print messages
    print(f"ordered_tasks:")
    print(ordered_tasks)
    print(f"time:")
    print(time)

    print(f"{len(errors)} Errors Found")
    if len(errors) > 0:
        print(errors)
    print("-- Script Complete --")


if __name__ == "__main__":
    main()