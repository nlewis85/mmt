# mmt - My Multitool 

## Summary
** This is primarily for personal use. Use/clone at your own risk. **
This script executes a list of tasks and dependencies with the expected following format: 
```
task,duration,dependencies
```

You can see the examples folder for some working and broken examples that were used for testing. 
Fields are defined as: 
'task' - Required - This is the task to run. So "curl amazon.com" or something like that. 
'duration'  - Required - This the length of time you expect the task to take. This is required. This is a number followed by ms (millisecond), s(second), or m(minute).
'dependencies' - Not Required - This is a space seperated list of tasks that are required before this one can be executed. If the task you referring to also has spaces, you simply need to wrap the dependency is double quotes

A functional file would be:
```
ping 8.8.8.8,1s,none
curl amazon.com,500ms,ping 8.8.8.8
```

## Usage
Testing and developement was completed on python 3.11.9, although the only known dependency at 
the moment is on graphlib which requires python 3.9. 

Accepted parameters: 
```
  -h, --help            show this help message and exit
  --execute, -e         Execute the list of tasks from the specified file
  --dryrun, -d          Perform a dry run without executing any tasks
  --file FILE, -f FILE  Specify input file path. Default is ./template.txt
  --output OUTPUT, -o OUTPUT
                        Specify output file path. Default is ./output_results.txt
  --parallel PARALLEL, -p PARALLEL
                        Number of parallel tasks to run. Default is 3.
  --verbose, -v         Enable verbose logging 
```

**Execute Details** 
Execute will not run any commands if the file is determined to be invalid. 
Additionally, any commands with dependencies that have failed, will be skipped. 
Otherwise it will run the commands in order of the quickest way it can 

**Dryrun Details**
Dryrun will validate your file formatting for you, as well as check for recursion or other issues.
These same validations are done before execution, and if any fail the excution will not run. 

**Parallel Details**
This is the number of threads you want to use for each task. Generally speaking more will be quicker execution, but there are many scenarios where this will not be the case. Additional threads will only be used if it will benefit the execution time, which is entirely dependent on the list and order of dependencies. 

**Verbose Note:**
At present this does nothing. 

## Example Executions
Included in the examples folder is a list of fails used for testing during developement of this script. 

A break down of their usage is as follows: 
1. broken_test_1.txt - A task that references itself as a dependency. 
1. broken_test_2.txt - A dependency that references a task that doesn't exist. 
1. broken_test_3.txt - Circular dependencies with "postanalysis" and "task1" 
1. execute_test_fail.txt - This has commands and dependencies that will pass all validations, but will fail to execute (Unless you have a script/alias in your path for "asdfasdfasdf"). This validates the script will not execute tasks that are have dependencies that failed.  
1. execute_test.txt - This is a normal execution where everything runs as expected. 
1. normal_test.txt - This was used initially to verify validation and recursion checks. It doesn't really serve a use today but was kept as an example. 

Normal successful execution: 
```
$ python src/mmt.py -e -f examples/example_test.txt
...
 ----- Execution Summary -----

* "cd /tmp" : -- Success
* "nslookup google.com" : -- Success
* "ping 8.8.8.8" : -- Success
* "ping google.com" : -- Success
* "curl google.com > test.txt" : -- Success
* "curl newegg.com" : -- Success
* "curl amazon.com" : -- Success
* "ls | grep test.txt" : -- Success
* "rm test.txt" : -- Success


Total Execution Time: 6.5965
Expected Execution Time: 348.0
Calculated execution time was 341.4035 more seconds than actual execution.
```

Dryrun Example: 
```
$ python src/mmt.py -d -f examples/normal_test.txt

-- Welcome to MMT (My MultiTool) --
Mode: dryrun
File: examples/normal_test.txt
Verbosity: False
Parallel Tasks: 3
Output File: output_results.txt

Order of execution will be:
Step 1:
  - init
Step 2:
  - ping
  - nslookup
Step 3:
  - healthcheck
Step 4:
  - task1
  - task2
  - task3
Step 5:
  - postanalysis
Step 6:
  - cleanup

 No errors in examples/normal_test.txt

 Estimated duration to complete tasks is: 348.0 seconds
```

Example of script not running tasks that where it has detected issues. 
```
$ python src/mmt.py --execute -f examples/broken_test_1.txt

-- Welcome to MMT (My MultiTool) --
Mode: execute
File: examples/broken_test_1.txt
Verbosity: False
Parallel Tasks: 3
Output File: output_results.txt

-- FAILURE: 2 Errors Found --
Error - Task 'init' depends on itself.
Error - Dependency recursion found!
```

## Other Potential Improvements and Thoughts
* Pytest to test example test files as well as individual function tests
* API Implementation
* Formatting optimization and improvements 
* Revised and improved logging and debug logs
* Optimization of existing python loops (Low priority unless we need to execute this script en mass or on very low capacity devices)
* Support comparison per task of expected vs actual execution time
* Related to the above, could support updating the file with new expected time
* Bind tasks to a list of commands to be ran. For example right now we have:
```
init,5s,none
ping,1ms,init
nslookup,1s,init
```
We could have a seperate tasks.cfg file that binds those to actual commands to execute by the OS. 
```
init:
-run some command

ping:
-ping 8.8.8.8
-ping 8.8.4.4

nslookup:
-nslookup google.com
```

Could also have those tasks have variables/branches per OS. So it would be "nslookup" on windows but "host" on *nix.


