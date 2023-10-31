"'Solution' for testing import of logging helper."
import logging
from log_helper import create_logger
from log_helper import sol_wrapper, func_wrapper

Configured_Logging_Object = logging.Logger

@func_wrapper
def debug_test(log_obj:Configured_Logging_Object) -> None:
    """
    Function to show usage for DEBUG logging.
    """
    log_obj.debug("TEST:\tDebug function")

@func_wrapper
def info_test(log_obj:Configured_Logging_Object) -> None:
    """
    Function to show usage for INFO logging.
    """
    log_obj.info("TEST:\tInfo function")

@func_wrapper
def warning_test(log_obj:Configured_Logging_Object) -> None:
    """
    Function to show usage for WARNING logging.
    """
    log_obj.warning("TEST:\tWarning function")

@func_wrapper
def crit_test(log_obj:Configured_Logging_Object) -> None:
    """
    Function to show usage for CRITICAL logging.
    """
    log_obj.critical("TEST:\tCritical function")

@sol_wrapper
def main(log_obj:Configured_Logging_Object) -> None:
    """
    Main function to kick off the solution
    when run as a script.
    """
    log_obj.info("Here we gooooooo!!!!!!!!!!")
    debug_test(log_obj)
    log_obj.debug("Just an debug item")
    info_test(log_obj)
    log_obj.info("Just an info item")
    warning_test(log_obj)
    log_obj.debug("Just an debug item")
    crit_test(log_obj)

    log_obj.info("Final test - a failure!")
    assert True is False, "Just testing failure! Does it still finish solution wrap?"


if __name__ == "__main__":
    main(create_logger("Ext_Test", "a"))
