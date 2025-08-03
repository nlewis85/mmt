import subprocess
import time
import threading

"""
Module for multithreaded execution of tasks
"""



def command_execute (cmd,cmdtimeout,executed_tasks,output_file):
    """Execute one command"""
    cmd_time = time.time()
    cmd_output = None
    error_message = None
    cmd_result = False
    try:
        cmd_output = subprocess.run(
            cmd, 
            shell=True,
            capture_output=True,
            text=True,
            timeout=cmdtimeout,
        )
    except Exception as error:
        error_message = str(error)
    
    # Succes and failure variable setting
    if cmd_output.returncode == 0: 
        cmd_result = True
    elif not error_message: 
        error_message = "FAILURE: Task did not complete successfully. See output file for details."
    
    cmd_duration = round(time.time() - cmd_time,4)
    
    # Lock Thread and add to file/executed tasks
    with threading.Lock():
        #executed_tasks[cmd] = cmd_result
        if cmd_result:
            executed_tasks[cmd] = "Success"
        elif error_message:
            executed_tasks[cmd] = error_message
        else:
            executed_tasks[cmd] = "FAILURE: See output file for details." 
        with open(output_file, 'a') as file:
            file.write(f"""
---------- "{cmd}" Execution Result ----------
Output: {cmd_output.stdout if cmd_output else 'No output'}

Error: {error_message if cmd_result == False  else 'No errors'}
Duration: {cmd_duration:.2f} seconds
""")
        print(f"  {cmd} -- {'SUCCESS' if cmd_result else 'FAILED'} ")
        
    return cmd_result, cmd_duration

def can_task_run(task, executed_tasks):
    """Check if a task can run based on its dependencies"""
    for dependency in task['dependencies']:
        if dependency in executed_tasks:
            if executed_tasks[dependency] != "Success":
                return False
    return True
     
def steps_execute(steps, max_processes, output_file):
    """Manage steps and execute commands based on number of allowed processes"""
    execution_time = 0
    step_counter = 0
    cmd_timeout=60
    executed_tasks = {}
    
    # Initial File Write
    with open(output_file, 'w') as file:
        file.write(f"""
-- MMT Execution Output --
Execurtion Started at: {time.strftime('%H:%M:%S')}
Max Processes: {max_processes}\n\n
                    """)
    
    # Loop through each step
    for tasks in steps: 
        step_counter+=1
        step_timer=time.time()
    
        print(f"\n Executing Step {step_counter}:\n")
        
        # Build a list of executable tasks
        executable_tasks=[]
        for task in tasks:
            if can_task_run(task, executed_tasks):
                executable_tasks.append(task)
            else:
                # Actions taken if task is skipped
                print(f"  {task['name']} -- ** Skipping task due to failed dependency. **")
                executed_tasks[task["name"]] = "SKIPPED: Skipped task due to missed dependency."
                with open(output_file, 'a') as file:
                    file.write(f"""
---------- "{task['name']}" Execution Result ----------
Skipped due to failed dependency. \n
                            """)
        
        # Loop through tasks in batches
        for i in range(0, len(executable_tasks), max_processes):
            batch = executable_tasks[i:i + max_processes]
            processes = []
            # Batch loop
            for j in range(len(batch)):
                thread = threading.Thread(target=command_execute, args=(batch[j]['name'], cmd_timeout, executed_tasks, output_file))
                thread.start()
                processes.append(thread)

            for thread in processes:
                thread.join()

            execution_time+=time.time() - step_timer
            
    return executed_tasks, round(execution_time,4)
            