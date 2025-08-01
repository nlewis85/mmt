# mmt - My Multitool 

## Summary
Intending for this code to be used for executing of multiple tasks at the same time. 
This is primarily for personal use. 

## Current Status
This script doesn't execute anything atm, but is a proof of concept of how the script will be ran. 

## Examples
Attached are a few broken examples and one working example. 

normal_test.txt - A normal list of tasks I'd expect to be able to execute
```
python mmt.py -e -f ../normal_test.txt
...
0 Errors Found
-- Script Complete --
```

broken1.txt - Test for a task calling itself
```
$ python mmt.py -e -f ../broken1.txt
...
["Task 'init' depends on itself."]
-- Script Complete --
```

broken2.txt - Test for a task calling itself
```
$ python mmt.py -e -f ../broken2.txt
...
["Listed dependency 'noreference' not found."]
-- Script Complete --
```

broken3.txt - Test for recursion of dependencies. This logic isn't implemented yet. 
```
$ python mmt.py -e -f ../broken3.txt
...
["Listed dependency 'noreference' not found."]
-- Script Complete --
```