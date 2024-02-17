"'Solution' for testing import of logging helper."
# import logging
from v3_Class_Fix.log_helper_class import ConfiguredLogger


logger_obj = ConfiguredLogger(file_name_in="Test_File_As_Class",
                              file_mode="w",
                              init_console_setup=1)

logger = logger_obj.logger
func_wrapper = logger_obj.func_wrapper
sol_wrapper = logger_obj.sol_wrapper

@func_wrapper
def debug_test() -> None:
    """
    Function to show usage for DEBUG logging.
    """
    logger.debug("TEST:\tDebug function")

@func_wrapper
def info_test() -> None:
    """
    Function to show usage for INFO logging.
    """
    logger.info("TEST:\tInfo function")
    logger.warning("Testing warning message ...")

@func_wrapper
def crit_test() -> None:
    """
    Function to show usage for CRITICAL logging.
    """
    logger.info("Final test - a failure!")
    logger.critical("TEST:\tCritical function - about to fail ...")

    assert True is False, "Just testing failure! Does it still finish solution wrap?"

@sol_wrapper(using_exit=False)
@func_wrapper
def main() -> None:
    """
    Main function to kick off the solution
    when run as a script.
    """
    logger.info("Here we gooooooo!!!!!!!!!!")
    debug_test()
    info_test()
    crit_test()

if __name__ == "__main__":

    main()
