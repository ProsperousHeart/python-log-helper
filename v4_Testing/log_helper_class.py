"Module providing easy use of logging."
# ===========================================================================
# More information on logging can be found here:
#   https://www.blog.pythonlibrary.org/2012/08/02/python-101-an-intro-to-logging/
#   https://www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3
#   https://www.loggly.com/ultimate-guide/python-logging-basics/
# ===========================================================================

import os
import logging
import functools
from datetime import date
from dataclasses import dataclass
import traceback

import pprint
pp = pprint.PrettyPrinter(indent=4)

today = date.today()
ConfiguredLoggingObject = logging.Logger


# ===========================================================================
# https://docs.python.org/3.12/howto/logging-cookbook.html#how-to-treat-a-logger-like-an-output-stream
# could be used when considering creation of a class instead of a function
# ===========================================================================
@dataclass()
class ConfiguredLogger:
    """
    Class to provide single instance of configured logger & wrappers.
    """
    # logging levels:  https://docs.python.org/3/library/logging.html#logging-levels
    # file_name_in: str = "Test_File_As_Class"
    file_name_in: str
    file_mode: str = "a"
    log_loc: str = f"{os.getcwd()}/logs"
    datefmt: str = "%Y-%m-%d %H:%M"

    new_exception: int = 0
    fresh_start: int = 1

    init_file_setup: int = 1
    file_lvl: int = logging.DEBUG
    log_file_format: str = logging.Formatter(
        "%(asctime)s %(levelname)-8s | %(filename)-20s:%(lineno)-5s | %(funcName)-25s %(message)s"
        )

    init_console_setup: int = 1
    console_lvl: int = logging.WARNING
    console_format: str = logging.Formatter("%(asctime)s [%(levelname)-8s] %(message)s\n")

    # TODO: write class input that will trigger enabling of logs after creation

    # logging levels:  https://docs.python.org/3/library/logging.html#logging-levels
    # https://docs.python.org/3/library/dataclasses.html#dataclasses.__post_init__
    def __post_init__(self):
        """
        Creates & returns a logger object with specific
        formatting for file and console needs.
        """

        self.file_name_out: str = f"{self.log_loc}/{today}_{self.file_name_in}.log"

        # if file for writing logs does not exist, create it
        if not os.path.exists(self.log_loc):
            os.makedirs(self.log_loc)

        self.logger = logging.getLogger(__name__)    # root logger from main script
        self.logger.setLevel(logging.DEBUG)

        if self.init_file_setup:
            self.setup_file_logging()

        if self.init_console_setup:
            self.setup_console_logging()

        self.logger.info("Logging setup!")


    def __enter__(self):
        """
        Allows for use of 'with' statement.
        """
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        To be used in conjunction with 'with' statement.
        This will close the logger when done.
        If exception occurs, it will log only to file then close logger.
        """
        if exc_type:
            if self.logger.handlers:
                self.disable_console_logging()
            self.logger.warning("Exception occurred...")
            # self.logger.debug(exc_type)
            # self.logger.debug(exc_val)
            # self.logger.debug(pprint.pformat(exc_tb.print_tb, indent=4))
            # self.logger.debug("Full Traceback:",
            #                   exc_info=(exc_type, exc_val, exc_tb))
        self.logger.debug("Ending program ...")
        self.disable_all_logging()
        # self.logger.file_handler.close()  # needed in test file
        for handler in self.logger.handlers:
            handler.close()


    def setup_console_logging(self):
        """
        Setup logging to console.
        """
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(self.console_lvl)
        self.console_handler.setFormatter(self.console_format)
        self.enable_console_logging()
        self.logger.info("Console logging setup")


    def setup_file_logging(self):
        """
        Setup logging to file.
        """
        self.file_handler = logging.FileHandler(self.file_name_out, mode=self.file_mode)
        self.file_handler.setLevel(self.file_lvl)
        self.file_handler.setFormatter(self.log_file_format)
        self.enable_file_logging()
        self.logger.info("File logging setup")


    # def enable_console_logging(self, program_start: int = 1):
    def enable_console_logging(self):
        """
        Enable logging to console.
        """

        if self.console_handler not in self.logger.handlers:
            self.logger.addHandler(self.console_handler)
            self.logger.debug("Console logging enabled")


    def enable_file_logging(self):
        """
        Setup logging to file.
        """

        if self.file_handler not in self.logger.handlers:
            self.logger.addHandler(self.file_handler)
            self.logger.debug("%s Starting of Logs %s",
                                '='*3, '='*3)
            self.logger.debug("File logging enabled")


    def disable_console_logging(self):
        """
        Disable logging to console.
        """

        if self.console_handler in self.logger.handlers:
            self.logger.removeHandler(self.console_handler)
            if self.logger.handlers:
                self.logger.debug("Console logging disabled")


    def disable_file_logging(self):
        """
        Disable logging to file.
        """

        if self.file_handler in self.logger.handlers:
            self.logger.removeHandler(self.file_handler)
            if self.logger.handlers:
                self.logger.debug("File logging disabled")


    def disable_all_logging(self):
        """
        Disables all logging - file and console.
        """
        if self.file_handler in self.logger.handlers:
            self.logger.debug("Disabling all logging ...")
            self.logger.debug("%s Ending of Logs %s",
                              '='*3, '='*3)
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)


    def func_wrapper(self, func):
        """
        Wrapper function to provide start and end logging
        when running functions without interfering with
        other arguments or returned data.
        """
        @functools.wraps(func)
        def log_func_wrapper(*args, **kwargs):
            # self.logger.debug("Starting %s from module:\t%s.%s",
            #                   func.__qualname__,
            #                   func.__module__,
            #                   func.__name__)
            self.logger.debug("Starting:\t%s.%s", func.__module__, func.__name__)
            try:
                rtn_data = func(*args, **kwargs)
            except Exception as err:
                if self.new_exception == 0:
                    self.new_exception = 1
                    # self.logger.debug(pprint.pformat(err))
                    self.disable_console_logging()

                    self.logger.debug("%s exception within %s.%s:\t%s",
                                    type(err).__name__,
                                    func.__module__,
                                    func.__name__,
                                    str(err)
                                    )

                    # self.logger.warning("%s message:\t%s", type(err).__name__, str(err))
                    self.logger.error("\n%s", traceback.format_exc())
                    
                    # # using exception method to log error also posts to console - defeating the purpose
                    # self.logger.exception("%s within %s.%s:\t%s",
                    #                       type(err).__name__,
                    #                       func.__module__,
                    #                       func.__name__,
                    #                       str(err)
                    #                       )
                    
                    if self.init_console_setup:
                        self.enable_console_logging()
                    self.logger.critical("Log review needed!\nBe sure to check your logs:\n%s",
                                        # next(iter([handler.baseFilename
                                        #         for handler in self.logger.handlers
                                        #         if isinstance(handler, logging.FileHandler)
                                        #         ])
                                        # )
                                        self.file_name_out
                    )
                    # self.logger.info("Exception args:\t%s", err.args)
                    # self.logger.critical(pprint.pformat(str(err)))

                raise
            else:
                return rtn_data
            finally:
                # self.logger.debug(f"Ending {func.__qualname__} from module:\t{func.__module__}")
                self.logger.debug("Ending:\t%s.%s", func.__module__, func.__name__)
        return log_func_wrapper


    def sol_wrapper(self, using_exit:bool = False):
        """
        Wrapper function to provide start and end logging
        for entire solution - meant to only run ONCE.
        """
        def actual_decorator(func):
            @functools.wraps(func)
            def sol_func_wrapper(*args, **kwargs):
                """
                Wraps function around DEBUG lines to say start & end
                of a solution / script. If the script fails,
                it will log it then gracefully exit so the logs are
                finalized when closing.
                """

                try:
                    rtn_data = func(*args, **kwargs)
                except Exception as err:
                    self.logger.info("%s exception forced script to close ...",
                                     type(err).__name__)
                else:
                    return rtn_data
                finally:
                    self.logger.debug("Ending:\t%s.%s",
                                      func.__module__,
                                      func.__name__)

                    if not using_exit:
                        self.__exit__(None, None, None)

            return sol_func_wrapper
        return actual_decorator


# =========================================
# Example usage
# =========================================

# TODO: write class input that will trigger enabling of logs after creation
logger_obj = ConfiguredLogger(file_name_in="EXAMPLE_Class_Log_File",
                              file_mode="w",
                              init_console_setup=1)

log_obj = logger_obj.logger
func_wrapper = logger_obj.func_wrapper
sol_wrapper = logger_obj.sol_wrapper


@sol_wrapper(using_exit=False)
@func_wrapper
def main() -> None:
    """
    Takes in a logging object pre-defined for formatting
    then runs a few test functions to confirm use.
    """
    log_obj.debug("This is a debug test ...")
    log_obj.info("This is a info test ...")
    log_obj.warning("This is a warning test ...")

    assert True is False, "Just testing failure! Does it still finish solution wrap?"

if __name__ == "__main__":

    main()
