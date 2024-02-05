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

from dataclasses import dataclass

import pprint
pp = pprint.PrettyPrinter(indent=4)

today = date.today()
ConfiguredLoggingObject = logging.Logger

@dataclass
class ConfiguredLogger:
    """
    Class to provide single instance of configured logger & wrappers.
    """
    # https://docs.python.org/3/library/logging.html#logging-levels
    file_lvl: int
    console_lvl: int

    file_name: str="Test_File_As_Class"
    # file_name: str
    file_mode: str="a"

    logging_loc: str=f"{os.getcwd()}/logs"

    def __init__(self, file_name: str="Test_File_As_Class",
                  file_mode: str="a",
                  file_lvl: int=logging.DEBUG,
                  console_lvl: int=logging.WARNING,
                  log_loc: str=f"{os.getcwd()}/logs"):
        self.file_name = file_name
        self.file_mode = file_mode
        self.file_lvl = file_lvl
        self.console_lvl = console_lvl
        self.logging_loc = log_loc
        self.logger_obj = self.create_logger(
                                            self.file_name,
                                            self.file_mode,
                                            self.file_lvl,
                                            self.console_lvl,
                                            self.logging_loc
                                            )

    def __enter__(self):
        # self.logger_obj.debug(f"{'='*3} Starting of Logs {'='*3}")
        self.logger_obj.debug("%s Starting of Logs %s", '='*3, '='*3)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.logger_obj.debug(f"There has been an error of type:\t{exc_type}")
        self.logger_obj.debug("There has been an error of type:\t%s", exc_type)
        if exc_val:
            # self.logger_obj.debug(f"Exception instance::\n{exc_val}")
            self.logger_obj.debug("Exception instance::\n%s", exc_val)
        # self.logger_obj.debug(f"TRACEBACK:\n{pprint.pformat(exc_tb)}")
        self.logger_obj.debug("TRACEBACK:\n%s", pprint.pformat(exc_tb))

        # https://stackoverflow.com/a/7787832/10474024
        # self.logger_obj.critical(f"""There has been an ERROR!!! Be sure to check your logs:
        self.logger_obj.critical("There has been an ERROR!!! Be sure to check your logs:\n%s",
                                 {", ".join(
            [item.baseFilename for item in self.logger_obj.__dict__['parent'].__dict__['handlers']
             if item.__class__.__name__ == "FileHandler"])})
        # self.logger_obj.debug(pprint.pformat(err))
        # self.logger_obj.debug(f'{"="*3} Ending of Logs {"="*3}')
        self.logger_obj.debug("%s Ending of Logs %s", '='*3, '='*3)

    # ===========================================================================
    # https://docs.python.org/3.12/howto/logging-cookbook.html#how-to-treat-a-logger-like-an-output-stream
    # could be used when considering creation of a class instead of a function
    # ===========================================================================

    # logging levels:  https://docs.python.org/3/library/logging.html#logging-levels
    def create_logger(self, file_name:str,
                  file_mode:str,
                  file_lvl:int,
                  console_lvl:int,
                  logging_loc:str) -> ConfiguredLoggingObject:
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
        if not os.path.exists(logging_loc):
            os.makedirs(logging_loc)

        # =======================================================================
        # logging to multiple locations
        # https://docs.python.org/3.12/howto/logging-cookbook.html#logging-to-multiple-destinations
        # =======================================================================

        # log to file
        logging.basicConfig(
            datefmt="%Y-%m-%d %H:%M",
            filename=f"{logging_loc}/{today}_{file_name}.log",
            filemode=file_mode,
            level=file_lvl,
            format="%(asctime)s %(filename)-15s " +
                "line %(lineno)-s %(funcName)-18s %(levelname)-8s " +
                "%(message)s"
        )

        logger = logging.getLogger(__name__)    # root logger from main script

        # log to console (sys.stderr)
        console = logging.StreamHandler()
        console.setLevel(console_lvl)
        c_formatter = logging.Formatter(
            "%(name)-12s line %(lineno)-s %(levelname)-8s | %(message)s"
            )
        console.setFormatter(c_formatter)
        logger.addHandler(console)              # add to root logger

        logging_buffer = io.StringIO()
        logger.addHandler(logging.StreamHandler(logging_buffer))

        return logger


    def get_logger(self, ) -> ConfiguredLoggingObject:
        """
        Returns configured logging.Logger object.
        """
        return self.logger_obj

    @classmethod
    def func_wrapper(self, func):
        """
        Wrapper function to provide start and end logging
        when running functions without interfering with
        other arguments or returned data.
        """
        @functools.wraps(func)
        def log_func_wrapper(*args, **kwargs):
            pp.pprint([arg for arg in args if isinstance(arg, logging.Logger)])
            logger = [arg for arg in args if isinstance(arg, logging.Logger)][0]
            logger.debug(f"Starting {func.__qualname__} from module:\t{func.__module__}")
            try:
                rtn_data = func(*args, **kwargs)
            except Exception as err:
                logger.critical(pprint.pformat(err))
                raise err
            else:
                return rtn_data
            finally:
                logger.debug(f"Ending {func.__qualname__} from module:\t{func.__module__}")
        return log_func_wrapper


    # def sol_wrapper(self, func):
    #     """
    #     Wrapper function to provide start and end logging
    #     for entire solution - meant to only run ONCE.
    #     """
    #     @functools.wraps(func)
    #     def log_func_wrapper(*args, **kwargs):
    #         """
    #         Wraps function around DEBUG lines to say start & end
    #         of a solution / script. If the script fails,
    #         it will log it then gracefully exit so the logs are
    #         finalized when closing.
    #         """
    #         # logger = [arg for arg in args if isinstance(arg, logging.Logger)][0]
    #         logger = [
    #             arg for arg in args
    #             if isinstance(arg, ConfiguredLogger)
    #             and isinstance(arg.logger_obj, ConfiguredLoggingObject)
    #             # if isinstance(arg, ConfiguredLoggingObject)
    #         ][0].logger_obj
    #         # ][0]
    #         # logger.debug(f"{'='*3} Starting of Logs {'='*3}")
    #         try:
    #             rtn_data = func(*args, **kwargs)
    #         except Exception as err:
    #             # https://stackoverflow.com/a/7787832/10474024
    #             logger.critical(f"""There has been an ERROR!!! Be sure to check your logs:
    #             {", ".join([item.baseFilename
    #             for item in logger.__dict__['parent'].__dict__['handlers']
    #             if item.__class__.__name__ == "FileHandler"])}""")
    #             logger.debug(pprint.pformat(err))
    #         else:
    #             return rtn_data
    #         # finally:
    #         #     logger.debug(f'{"="*3} Ending of Logs {"="*3}')
    #     return log_func_wrapper


# must have a file_name or else no fileHandler is created
# even with the default provided in init!
configured_logger_obj = ConfiguredLogger(file_name="Test_File_As_Class",
                                 file_mode="w")
# sol_wrapper = configured_logger_obj.sol_wrapper
func_wrapper = configured_logger_obj.func_wrapper

@func_wrapper
def info_test(log_obj:ConfiguredLoggingObject) -> None:
    """
    Function to show usage for INFO logging.
    """
    log_obj.info("TEST:\tInfo function")

# @sol_wrapper
def main(configured_logger:ConfiguredLogger) -> None:
    """
    Takes in a logging object pre-defined for formatting
    then runs a few test functions to confirm use.
    """
    log_obj = configured_logger.logger_obj
    log_obj.debug("This is a debug test ...")
    info_test(log_obj)
    # log_obj.info("This is a info test ...")

    log_obj.warning("This is a warning test ...")

if __name__ == "__main__":
    # main(configured_logger_obj)
    with ConfiguredLogger(file_name="Test_File_As_Class",
                          file_mode="w") as conf_logger:
        main(conf_logger)
