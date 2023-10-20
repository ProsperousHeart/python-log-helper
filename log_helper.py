"Module providing easy use of logging."
# ===========================================================================
# More information on logging can be found here:
#   https://www.blog.pythonlibrary.org/2012/08/02/python-101-an-intro-to-logging/
#   https://www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3
#   https://www.loggly.com/ultimate-guide/python-logging-basics/
# ===========================================================================

import os
import logging
import io
import functools
from datetime import date

import pprint
pp = pprint.PrettyPrinter(indent=4)

today = date.today()

# ===========================================================================
# https://docs.python.org/3.12/howto/logging-cookbook.html#how-to-treat-a-logger-like-an-output-stream
# could be used when considering creation of a class instead of a function
# ===========================================================================

# logging levels:  https://docs.python.org/3/library/logging.html#logging-levels
def create_logger(file_name:str="Test_File",
                  file_mode:str="a",
                  file_lvl:int=logging.DEBUG,
                  console_lvl:int=logging.WARNING,
                  log_loc:str=f"{os.getcwd()}/logs"):
    """
    Takes in the following:
        file_name       STR name of file to write to
        file_mode       STR mode to write file (needs to be checked)
        console_level   INT must tie in to logging level INTs (else raise error)
        log_loc         STR by default will use local script's folder/logs
    
    With provided inputs, creates & returns a logger object
    with specific formatting for file and console needs.
    """
    # if file for writing logs does not exist, create it
    if not os.path.exists(log_loc):
        os.makedirs(log_loc)

    # =======================================================================
    # logging to multiple locations
    # https://docs.python.org/3.12/howto/logging-cookbook.html#logging-to-multiple-destinations
    # =======================================================================

    # log to file
    logging.basicConfig(
        datefmt="%Y-%m-%d %H:%M",
        filename=f"{log_loc}/{today}_{file_name}.log",
        filemode=file_mode,
        level=file_lvl,
        format="%(asctime)s %(filename)-15s %(funcName)-18s %(levelname)-8s %(message)s"
    )

    logger = logging.getLogger(__name__)    # root logger from main script

    # log to console (sys.stderr)
    console = logging.StreamHandler()
    console.setLevel(console_lvl)
    c_formatter = logging.Formatter("%(name)-12s line %(lineno)-s %(levelname)-8s | %(message)s")
    console.setFormatter(c_formatter)
    logger.addHandler(console)              # add to root logger

    logging_buffer = io.StringIO()
    logger.addHandler(logging.StreamHandler(logging_buffer))

    return logger

def func_wrapper(func):
    """
    Wrapper function to provide start and end logging
    when running functions without interfering with
    other arguments or returned data.
    """
    @functools.wraps(func)
    def log_func_wrapper(*args, **kwargs):
        logger = [arg for arg in args if isinstance(arg, logging.Logger)][0]
        logger.debug(f"Starting {func.__qualname__} from module:\t{func.__module__}")
        rtn_data = func(*args, **kwargs)
        logger.debug(f"Ending {func.__qualname__} from module:\t{func.__module__}")
        return rtn_data
    return log_func_wrapper

def sol_wrapper(func):
    """
    Wrapper function to provide start and end logging
    for entire solution - meant to only run ONCE.
    """
    @functools.wraps(func)
    def log_func_wrapper(*args, **kwargs):
        logger = [arg for arg in args if isinstance(arg, logging.Logger)][0]
        logger.debug(f"{'='*3} Starting of Logs {'='*3}")
        rtn_data = func(*args, **kwargs)
        logger.debug(f'{"="*3} Ending of Logs {"="*3}')
        return rtn_data
    return log_func_wrapper

@sol_wrapper
def main(log_obj:logging.Logger) -> None:
    """
    Takes in a logging object pre-defined for formatting
    then runs a few test functions to confirm use.
    """
    print("Default choices")
    log_obj.debug("This is a debug test ...")
    log_obj.info("This is a info test ...")
    log_obj.warning("This is a warning test ...")
    print("initial testing done!")


if __name__ == "__main__":
    logger_obj = create_logger(file_mode="a")   # default
    main(logger_obj)
