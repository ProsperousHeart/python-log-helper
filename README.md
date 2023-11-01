# About

This `python-log-helper` repo is the culmination of a long standing desire to make logging easier while leveraging decorators.

## Table of Contents

- [Business Requirements](#business-requirements)
    - [Must Have](#must-have)
    - [Nice to Have](#nice-to-have)
- [Current Status](#current-status)
- [Additional Resources](#additional-resources)

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
7. easy way to show start and stop of log file logs for each run

## Nice to Have

1. Leverage built in functions of logger to limit the number of files chosen when starting run
2. Flexible options for formatting (both console and file)
3. Have way to email log file(s)
4. Consider [this](https://docs.python.org/3.12/howto/logging-cookbook.html#how-to-treat-a-logger-like-an-output-stream) when looking to move to a class


# Current Status

TBD


# Additional Resources

The following were used to build this repo:
- [PEP 454](https://peps.python.org/pep-0484/) - type hints (see [here](https://docs.python.org/3/library/typing.html) for typing support in python 3)
- Jupyter Python class [training](https://github.com/ProsperousHeart/TrainingUsingJupyter/blob/master/Python/Python-INTER/01%20-%20Python%20Classes.ipynb)
