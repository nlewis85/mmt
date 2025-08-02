# mmt - My Multitool 

## Summary
Intending for this code to be used for executing of multiple tasks at the same time. 
This is primarily for personal use. 
Testing and developement was completed on python 3.11.9, although the only known dependency at 
the moment is on graphlib which requires python 3.9. 

## Current Status
This script doesn't execute anything atm, but is a proof of concept of how the script will be ran. 
It does validate recursiona and calculates time to execute. 

## Next Up
* Implement process/threads in time calcuation and execution
* Optimization of code (ex: unused imports, extra loops through code that we don't need to take)
* Implement execution code 
* Implement execution time calculation and comparison to calculated expected execution time


## Other Potential Improvements and Thoughts
* Pytest to test example test files for me e2e as well as individual function tests
* API Implementation
* Revised/improved logging amnd debug logs
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

Could even have those tasks have variables/branches per OS. So it would be "nslookup" on windows but "host" on *nix.
Could even leverage ansible for the above executions? 

## Examples
Attached are a few broken examples and one working example. 

normal_test.txt - A normal list of tasks I'd expect to be able to execute
```
python mmt.py -e -f ../normal_test.txt
...
time:
528.001
0 Errors Found
-- Script Complete --
```

broken1.txt - Test for a task calling itself
```
$ python mmt.py -e -f ../broken1.txt
...
time:
0
2 Errors Found
["Task 'init' depends on itself.", 'Dependency recursion found!']
-- Script Complete --
```

broken2.txt - Test for a task calling itself
```
$ python mmt.py -e -f ../broken2.txt
...
time:
528.001
1 Errors Found
["Listed dependency 'noreference' not found."]
-- Script Complete --
```

broken3.txt - Test for recursion of dependencies. This logic isn't implemented yet. 
```
$ python mmt.py -e -f ../broken3.txt
...
time:
0
1 Errors Found
['Dependency recursion found!']
-- Script Complete --
```