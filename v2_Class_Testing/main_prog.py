"'Solution' for testing import of logging helper."
# import logging
from v2_Class_Testing.log_helper_class import ConfiguredLogger


if __name__ == "__main__":
    with ConfiguredLogger(file_name_in="Test_File_As_Class",
                            file_mode="w",
                            init_console_setup=1) as conf_logger:

        log_obj = conf_logger.logger
        func_wrapper = conf_logger.func_wrapper
        sol_wrapper = conf_logger.sol_wrapper

        @func_wrapper
        def debug_test() -> None:
            """
            Function to show usage for DEBUG logging.
            """
            log_obj.debug("TEST:\tDebug function")

        @func_wrapper
        def info_test() -> None:
            """
            Function to show usage for INFO logging.
            """
            log_obj.info("TEST:\tInfo function")
            log_obj.warning("Testing warning message ...")

        @func_wrapper
        def crit_test() -> None:
            """
            Function to show usage for CRITICAL logging.
            """
            log_obj.info("Final test - a failure!")
            log_obj.critical("TEST:\tCritical function - about to fail ...")

            assert True is False, "Just testing failure! Does it still finish solution wrap?"

        @sol_wrapper
        @func_wrapper
        def main() -> None:
            """
            Main function to kick off the solution
            when run as a script.
            """
            log_obj.info("Here we gooooooo!!!!!!!!!!")
            debug_test()
            info_test()
            crit_test()


        main()
