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
import traceback

import pprint
pp = pprint.PrettyPrinter(indent=4)

today = date.today()
ConfiguredLoggingObject = logging.Logger


@dataclass
class ConfiguredLogger:
    """
    Class to provide single instance of configured logger & wrappers.
    """
    # logging levels:  https://docs.python.org/3/library/logging.html#logging-levels
    new_exception = 0
    fresh_start = 1
    file_name_in: str = "Test_File_As_Class"
    file_mode: str = "a"
    log_loc: str = f"{os.getcwd()}/logs"
    datefmt: str = "%Y-%m-%d %H:%M"

    file_name_out: str = f"{log_loc}/{today}_{file_name_in}.log"

    init_file_setup: int = 1
    file_lvl: int = logging.DEBUG
    log_file_format: str = logging.Formatter(
        "%(asctime)s %(levelname)-8s | %(filename)-18s:%(lineno)-6s | %(funcName)-25s %(message)s"
        )

    init_console_setup: int = 1
    console_lvl: int = logging.WARNING
    console_format: str = logging.Formatter("%(asctime)s [%(levelname)-8s] %(message)s\n")

    # logging levels:  https://docs.python.org/3/library/logging.html#logging-levels
    # https://docs.python.org/3/library/dataclasses.html#dataclasses.__post_init__
    def __post_init__(self):
        """
        Creates & returns a logger object with specific
        formatting for file and console needs.
        """

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
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
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
            # self.logger.debug(f"Starting {func.__qualname__} from module:\t{func.__module__}.{func.__name__}")
            self.logger.debug("Starting:\t%s.%s", func.__module__, func.__name__)
            try:
                rtn_data = func(*args, **kwargs)
            except Exception as err:
                if self.new_exception == 0:
                    self.new_exception = 1
                    # self.logger.debug(pprint.pformat(err))
                    self.logger.debug("A %s exception has occurred within %s.%s",
                                    type(err).__name__,
                                    func.__module__,
                                    func.__name__
                                    )
                    self.logger.warning("%s:\t%s", type(err).__name__, str(err))
                    self.disable_console_logging()
                    self.logger.error("\n%s", traceback.format_exc())
                    self.enable_console_logging()
                    self.logger.critical("Log review needed!\nBe sure to check your logs:\n%s",
                                        next(iter([handler.baseFilename
                                                for handler in self.logger.handlers
                                                if isinstance(handler, logging.FileHandler)
                                                ])
                                        )
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


    def sol_wrapper(self, func):
        """
        Wrapper function to provide start and end logging
        for entire solution - meant to only run ONCE.
        """
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
                self.logger.info("%s exception forced script to close ...", type(err).__name__)
            else:
                return rtn_data
            finally:
                self.logger.debug("Ending:\t%s.%s", func.__module__, func.__name__)

        return sol_func_wrapper


# ===========================================================================
# https://docs.python.org/3.12/howto/logging-cookbook.html#how-to-treat-a-logger-like-an-output-stream
# could be used when considering creation of a class instead of a function
# ===========================================================================

# logging levels:  https://docs.python.org/3/library/logging.html#logging-levels
def create_logger(file_name:str="Test_File",
                  file_mode:str="a",
                  file_lvl:int=logging.DEBUG,
                  console_lvl:int=logging.WARNING,
                  log_loc:str=f"{os.getcwd()}/logs") -> ConfiguredLoggingObject:
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

def sol_wrapper(func):
    """
    Wrapper function to provide start and end logging
    for entire solution - meant to only run ONCE.
    """
    @functools.wraps(func)
    def log_func_wrapper(*args, **kwargs):
        """
        Wraps function around DEBUG lines to say start & end
        of a solution / script. If the script fails,
        it will log it then gracefully exit so the logs are
        finalized when closing.
        """

        logger = [arg for arg in args if isinstance(arg, logging.Logger)][0]
        logger.debug(f"{'='*3} Starting of Logs {'='*3}")
        try:
            rtn_data = func(*args, **kwargs)
        except Exception as err:
            # https://stackoverflow.com/a/7787832/10474024
            logger.critical(f"""There has been an ERROR!!! Be sure to check your logs:
            {", ".join([item.baseFilename
                        for item in logger.__dict__['parent'].__dict__['handlers']
                        if item.__class__.__name__ == "FileHandler"])
            }""")
            logger.debug(pprint.pformat(err))
        else:
            return rtn_data
        finally:
            logger.debug(f'{"="*3} Ending of Logs {"="*3}')
    return log_func_wrapper

@sol_wrapper
def main(log_obj:ConfiguredLoggingObject) -> None:
    """
    Takes in a logging object pre-defined for formatting
    then runs a few test functions to confirm use.
    """
    # print("Default choices")
    log_obj.debug("This is a debug test ...")
    log_obj.info("This is a info test ...")
    log_obj.warning("This is a warning test ...")
    # print("initial testing done!")


if __name__ == "__main__":
    logger_obj = create_logger(file_mode="w")   # default
    main(logger_obj)
