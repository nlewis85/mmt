from graphlib import TopologicalSorter

""" 
Module for validations, ordering, and calculations of tasks.
"""

def validate_tasks(tasks, processes):
    """ Validate and order tasks and dependencies"""
    errors = []
    task_names = {task['name'] for task in tasks}

    
    for task in tasks:
        for dependency in task["dependencies"]:
            # Verify each dependency is a valid task
            if dependency not in task_names:
                errors.append(f"Listed dependency '{dependency}' not found.")
                
            # Verify listed dependency isn't self
            if task["name"] == dependency:  
                errors.append(f"Task '{task['name']}' depends on itself.")
    
    # Order Tasks and check for recursion with TopologicalSorter
    steps = []
    task_graph = {task['name']: task['dependencies'] for task in tasks}
    ts = TopologicalSorter(task_graph)
    
    try:
        ts.prepare()
        while ts.is_active():
            ready_tasks = ts.get_ready()
            # Break if done
            if not ready_tasks:
                break
            
            # Iterate through tasks 
            step_tasks = []
            for name in ready_tasks:
                    for task in tasks:  
                        if task['name'] == name:
                            step_tasks.append(task)
                            break  
            
            steps.append(step_tasks)
            ts.done(*ready_tasks)

        estimated_time = calculate_expected_runtime(steps, processes)
        return steps, estimated_time, errors
        
    except ValueError:
        errors.append(f"Dependency recursion found!")
        return steps, 0, errors
    
def calculate_expected_runtime(steps, processes):
    """Calculate expected runtime based on steps and number of processes"""
    calculated_time = 0
    
    for step in steps:
        # Create list as long as there are processes
        task_duration_times = [int()] * processes
        
        #Sorting tasks by duration, this allows for proper calculations
        tasks_by_duration = sorted(step, key=lambda t: t['duration'], reverse=True)
        
        # Iterate through list based on earliest duration
        for task in tasks_by_duration:
            earliest_thread = min(range(processes), key=lambda i: task_duration_times[i])
            task_duration_times[earliest_thread] += task['duration']
        
        step_time = max(task_duration_times)
            
        calculated_time += step_time

    return round(calculated_time, 4)