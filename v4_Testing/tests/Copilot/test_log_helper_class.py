'Module to test logging wrapper class'
import traceback
import unittest
from v4_Testing.log_helper_class import ConfiguredLogger

class TestFunctionDecorator(unittest.TestCase):
    """Unit tests for the function decorator of the ConfiguredLogger class."""

    # https://stackoverflow.com/a/14493895/10474024
    maxDiff = None

    def setUp(self):
        self.logger = ConfiguredLogger(file_name_in="Test_Helper_As_Class_Test_File",
                                       file_mode="w",
                                       init_console_setup=1)

    def tearDown(self):
        self.logger.disable_all_logging()
        # self.logger.__exit__(None, None, None)

        # Close the file handler
        self.logger.file_handler.close()

    def test_green(self):
        """
        Test the func_wrapper method if no error is raised.
        It should wrap the given function with logging statements.
        """
        @self.logger.func_wrapper
        def test_function():
            # self.logger.logger.info("MODULE.NAME")
            pass

        internal_debug = "DEBUG:v4_Testing.log_helper_class:"

        # Assert that the function is wrapped with logging statements
        self.assertIsNotNone(test_function.__wrapped__)

        # Assert that the wrapped logging statements are executed
        # https://monicagranbois.com/blog/python/til-how-to-unit-test-a-log-statement-in-python/
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertLogs
        with self.assertLogs(self.logger.logger, level="DEBUG") as log:
            test_function()
        self.assertEqual(log.output,
                         [f"{internal_debug}Starting:\t__main__.test_function",
                          f"{internal_debug}Ending:\t__main__.test_function"]
                        )

    def test_red(self):
        """
        Test the func_wrapper method if an error is raised.
        It should wrap the given function with logging statements.
        """
        @self.logger.func_wrapper
        def test_function():
            raise ValueError("Just testing failure!")

        if self.logger.file_handler not in self.logger.logger.handlers:
            self.logger.enable_file_logging()
        # Assert that the wrapped logging statements are executed
        with self.assertLogs(self.logger.logger, level="DEBUG") as log:
            with self.assertRaises(ValueError):
                test_function()

        internal_debug = "DEBUG:v4_Testing.log_helper_class:"
        internal_err = "ERROR:v4_Testing.log_helper_class:"
        internal_crit = "CRITICAL:v4_Testing.log_helper_class:"

        # Extract and assert that the traceback is present in the captured log records
        # https://docs.python.org/3/library/logging.html#logging.LogRecord
        traceback_obj = [log_record.exc_info
                         for log_record in log.records
                         if log_record.levelname == 'ERROR'
                         and log_record.exc_info is not None][0]
        traceback_msg = ''.join(traceback.format_exception(*traceback_obj)).strip()

        module_name = f"{test_function.__module__}.{test_function.__name__}"
        self.assertTrue(f"{internal_debug}Starting:\t{module_name}",
                        log.output[0])
        # self.assertTrue(f"{internal_debug}Starting:\t__main__.test_function", log.output[1])

        self.assertEqual(log.output,
                         [f"{internal_debug}Starting:\t{module_name}",
                          # disenable console logging - not checked here
                          f"""{internal_err}ValueError within {module_name}:\tJust testing failure!
{traceback_msg}""",
                          # enable console logging
                          # should not be here if console logging disabled from the start
                          # TODO: create a test for this when console logging is disabled - will require update to setup to provide 3 different options
                          f"{internal_debug}Console logging enabled",
                          f"""{internal_crit}Log review needed!
Be sure to check your logs:\n{self.logger.file_name_out}""",
                          f"{internal_debug}Ending:\t{module_name}"]
                        )


    def test_sol_wrapper(self):
        """
        Test the sol_wrapper method.
        It should wrap the given function with logging statements and handle exceptions.
        """
        @self.logger.sol_wrapper(using_exit=False)
        def test_function():
            pass

        # Assert that the function is wrapped with logging statements and exception handling
        self.assertIsNotNone(test_function.__wrapped__)
        # TODO: Add test implementation here

class TestConfiguredLogger(unittest.TestCase):
    """Unit tests for the ConfiguredLogger class."""

    maxDiff = None

    def setUp(self):
        self.logger = ConfiguredLogger(file_name_in="Test_Helper_As_Class_Test_File",
                                       file_mode="w",
                                       init_console_setup=1)

    def tearDown(self):
        self.logger.disable_all_logging()
        # self.logger.__exit__(None, None, None)

        # Close the file handler
        self.logger.file_handler.close()

    def test_setup_console_logging(self):
        """
        Test the setup_console_logging method.
        It should configure the console logging settings.
        """
        self.logger.setup_console_logging()
        console_handler = self.logger.console_handler
        # Assert that console logging is enabled
        self.assertTrue(console_handler in self.logger.logger.handlers)
        # Assert that console logging is set to the correct level
        self.assertEqual(console_handler.level, self.logger.console_lvl)
        # Assert that console logging is set to the correct format
        self.assertEqual(console_handler.formatter._fmt, self.logger.console_format._fmt)

    def test_setup_file_logging(self):
        """
        Test the setup_file_logging method.
        It should configure the file logging settings.
        """
        self.logger.setup_file_logging()
        self.assertTrue(self.logger.file_handler in self.logger.logger.handlers)
        self.assertEqual(self.logger.file_handler.level, self.logger.file_lvl)
        self.assertEqual(self.logger.file_handler.formatter._fmt, self.logger.log_file_format._fmt)

    def test_enable_console_logging(self):
        """
        Test the enable_console_logging method.
        It should enable console logging.
        """
        self.logger.enable_console_logging()
        self.assertTrue(self.logger.console_handler in self.logger.logger.handlers)
        self.assertEqual(self.logger.console_handler.level, self.logger.console_lvl)
        self.assertEqual(self.logger.console_handler.formatter._fmt, self.logger.console_format._fmt)

    def test_enable_file_logging(self):
        """
        Test the enable_file_logging method.
        It should enable file logging.
        """
        self.logger.enable_file_logging()
        self.assertTrue(self.logger.file_handler in self.logger.logger.handlers)
        self.assertEqual(self.logger.file_handler.level, self.logger.file_lvl)
        self.assertEqual(self.logger.file_handler.formatter._fmt, self.logger.log_file_format._fmt)
        self.assertEqual(self.logger.file_handler.mode, self.logger.file_mode)

    def test_disable_console_logging(self):
        """
        Test the disable_console_logging method.
        It should disable console logging.
        """
        self.logger.disable_console_logging()
        self.assertFalse(self.logger.console_handler in self.logger.logger.handlers)

    def test_disable_file_logging(self):
        """
        Test the disable_file_logging method.
        It should disable file logging.
        """
        self.logger.disable_file_logging()
        self.assertFalse(self.logger.file_handler in self.logger.logger.handlers)

    def test_disable_all_logging(self):
        """
        Test the disable_all_logging method.
        It should disable both console and file logging.
        """
        self.logger.disable_all_logging()
        self.assertFalse(self.logger.logger.handlers)

    def test_main(self):
        """Test the main function."""
        # TODO: Add test implementation here
        pass


if __name__ == "__main__":
    unittest.main()
