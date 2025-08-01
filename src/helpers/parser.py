import argparse
import sys
import shlex
from graphlib import TopologicalSorter

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

def parse_line(line):
    sections = line.strip().split(',')
    for section in sections:
        print(section)
    if len(sections) != 3:
        raise ValueError(f"""
        Expected format is 3 strings seperated by commas, like:\n
        ping 8.8.8.8,4s,none\n\n
        
        {len(sections)}
        """)
    
    name = sections[0].strip("'")

    # Parse duration
    duration = sections[1]
    if duration.endswith('ms'):
        duration = (float(duration[:-2]) / 1000)
    elif duration.endswith('s'):
        duration = float(duration[:-1])
    elif duration.endswith('m'):
        duration = float(duration[:-1]) * 60

    dependencies = shlex.split(sections[2]) if sections[2].lower() != 'none' else []

    return {
        'name': name,
        'duration': duration,
        'dependencies': dependencies
    }


def load_file(file):
    """ Load Tasks from a file"""
    with open(file) as f:
        lines = f.readlines()
    
    tasks = []
    for line in lines:
        tasks.append(parse_line(line))
        
    return tasks

def validate_tasks(tasks):
    """ Validate and order tasks and dependencies"""
    errors = []
    task_names = {task['name'] for task in tasks}

    
    for task in tasks:
        for dependency in task["dependencies"]:
            ### Verify each dependency is a valid task
            if dependency not in task_names:
                errors.append(f"Listed dependency '{dependency}' not found.")
                
            ### Verify listed dependency isn't self
            if task["name"] == dependency:  
                errors.append(f"Task '{task['name']}' depends on itself.")
                
    if len(errors) > 0:
        return tasks, errors
    
    ### Order Tasks
    task_order = []
    completed_tasks = []

    return task_order, errors

def calculate_expected_runtime(tasks, threads):
    calculated_time = 5
    return calculated_time