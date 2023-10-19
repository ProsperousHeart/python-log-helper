# About

This `python-log-helper` repo is the culmination of a long standing desire to make logging easier while leveraging decorators.

# Business Requirements

Here are the requirements & nice to haves in relation to this project.

## Must Have

Aside from being easily imported into any repo ...

1. Provide easy way to add logging to a repo without having to recreate the settings for each project
2. Have a decorator function that provides `DEBUG` entry and exit for functions
3. Provide way to turn on / off logging to console (set level to anything other than `WARNING`)
4. Provide way for choice in what logging file is saved
5. Have some way to show start/end of logging in the file per run
6. Have formatting show time, file name, function name, and logging level in saved logs (to start)

## Nice to Have

1. Leverage built in functions of logger to limit the number of files chosen when starting run
2. Flexible options for formatting (both console and file)
3. Have way to email log file(s)

