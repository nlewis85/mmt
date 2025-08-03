import sys
import os
import threading
import time

from helpers.parser import *
from helpers.validations import *
from helpers.execute import *

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
Output File: {args.output}
    """)
    
    steps, estimated_time, errors = validate_tasks(load_file(args.file), int(args.parallel))
    



    if len(errors) > 0:
        print(f"-- FAILURE: {len(errors)} Errors Found --")
        for error in errors:
            print(f"Error - {error}")
        #Quit if errors
        quit()
    else:
        i=0
        print(f"Order of execution will be:")
        for step in steps:
            i+=1
            print(f"Step {i}:")
            for task in step:
                print(f"  - {task['name']}")
        print(f"\n No errors in {args.file}")
        print(f"\n Estimated duration to complete tasks is: {estimated_time} seconds")
        
    if args.mode == "execute":
            executed_tasks, execution_time = steps_execute(steps, int(args.parallel), args.output)
            print("\n ----- Execution Summary -----\n")
            for task,status in executed_tasks.items():
                print(f"* \"{task}\" : -- {status}")
                
            print(f"\n\nTotal Execution Time: {execution_time}")
            print(f"Expected Execution Time: {estimated_time}")
            if estimated_time >= execution_time:
                print(f"Calculated execution time was {estimated_time - execution_time} more seconds than actual execution.")
            else:
                print(f"Calculated execution time was {execution_time - estimated_time} less seconds than actual execution.")
            
if __name__ == "__main__":
    main()