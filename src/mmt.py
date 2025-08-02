import sys
import os
import threading
import time

from helpers.parser import *
from helpers.validations import *

def main():
    """ Main """
    try: 
        args = parse_args()
    except Exception as error:
        print("Error: ", error)
    
    
    print(f"""
-- Welcome to MMT (My MultiTool) --
Mode: {args.mode}
File: {args.file}
Verbosity: {args.verbose}
Parallel Tasks: {args.parallel}
    """)
    
    steps, estimated_time, errors = validate_tasks(load_file(args.file), int(args.parallel))

    if len(errors) > 0:
        # Error Summary Message
        print(f"-- {len(errors)} Errors Found --")
        for error in errors:
            print(error)
    else:
        # Successful Execution Summary Message

        print(f"Order of execution will be:")
        i=0
        for step in steps:
            i+=1
            print(f"Step {i}:")
            for task in step:
                print(f"  - {task['name']}")
        print(f"\n No errors in {args.file}")
        print(f"\n Estimated duration to complete tasks is: {estimated_time} seconds")

if __name__ == "__main__":
    main()