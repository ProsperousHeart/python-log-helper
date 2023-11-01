"'Solution' for testing import of logging helper."
import logging
# from log_helper import create_logger
# from log_helper import sol_wrapper, func_wrapper
from Class_Testing.log_helper_as_class import ConfiguredLogger

ConfiguredLoggingObject = logging.Logger

configured_logger_obj = ConfiguredLogger(
                            file_name="Ext_Test_With_Class",
                            file_mode="w"
                        )
func_wrapper = configured_logger_obj.func_wrapper
sol_wrapper = configured_logger_obj.sol_wrapper

@func_wrapper
def debug_test(log_obj:ConfiguredLoggingObject) -> None:
    """
    Function to show usage for DEBUG logging.
    """
    log_obj.debug("TEST:\tDebug function")

@func_wrapper
def info_test(log_obj:ConfiguredLoggingObject) -> None:
    """
    Function to show usage for INFO logging.
    """
    log_obj.info("TEST:\tInfo function")

@func_wrapper
def warning_test(log_obj:ConfiguredLoggingObject) -> None:
    """
    Function to show usage for WARNING logging.
    """
    print(log_obj.handlers)
    log_obj.warning("TEST:\tWarning function\n" +
                    "\tAbout to force a failure ...")

@func_wrapper
def crit_test(log_obj:ConfiguredLoggingObject) -> None:
    """
    Function to show usage for CRITICAL logging.
    """
    # log_obj.critical("TEST:\tCritical function")

    log_obj.info("""Finished calling functions.
Final test - will be a failure!""")
    assert True is False, "Just testing failure! Does it still finish solution wrap?"

    log_obj.info("*** Should never get here ***")

@sol_wrapper
def main(logging_helper_obj:ConfiguredLogger) -> None:
    """
    Main function to kick off the solution
    when run as a script.
    """
    logger_obj = logging_helper_obj.logger_obj
    logger_obj.info("Here we gooooooo!!!!!!!!!!")
    debug_test(logger_obj)
    info_test(logger_obj)
    warning_test(logger_obj)
    crit_test(logger_obj)


if __name__ == "__main__":
    # main(create_logger("Ext_Test", "a"))
    main(configured_logger_obj)
