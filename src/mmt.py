import sys
import os

import helpers.filehandler
from helpers.parser import parse_args


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

    print("Script Done")


if __name__ == "__main__":
    main()