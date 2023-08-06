import os
import shutil
from datetime import datetime
from unittest import TestCase

from rkt_lib_toolkit.logger import Logger
from rkt_lib_toolkit.exception import InvalidLogLevelError, LogIsNotDirError
from rkt_lib_toolkit.tool import Singleton, Tool

tool = Tool()


class TestLogger(TestCase):

    def test_logger_when_log_is_not_directory(self):
        log = f"{tool.formatted_from_os(tool.get_cwd())}log_misstake"
        if os.path.exists(log):
            if os.path.isdir(log):
                shutil.rmtree(log)
            else:
                os.remove(log)

        open(log, "x").close()
        Singleton._instances = {}
        with self.assertRaises(LogIsNotDirError) as context:
            logger = Logger("coverage", "log_misstake")

        assert str(context.exception) == "\"log\" isn't a directory"
        os.remove(log)

    def test_add_without_exiting_log_level(self):
        logger = Logger("coverage", "log")
        logger.set_logger(caller_class="coverage", output="stream")
        with self.assertRaises(InvalidLogLevelError):
            logger.add("coverage", "tests coverage", 42)

    def test_add_with_exiting_log_level(self):
        logger = Logger("coverage", "log")
        logger.set_logger(caller_class="coverage", output="stream")
        assert logger.add("coverage", "tests coverage", 20) is None

    def test_set_logger(self):
        logger = Logger("coverage", "log")
        logger.set_logger(caller_class="coverage", output="both", out_file="coverage")
        logger.add("coverage", "test", 20)
        excepted = f"{logger._tool.get_dir(folder='log')}coverage_{datetime.today().date()}.log"
        obtained = logger.get_logger_file('coverage')
        assert obtained == excepted, print(f"Expected: {excepted}\nObtained: {obtained}")

    def test_no_logger_file(self):
        logger = Logger("coverage", "log")
        logger.set_logger(caller_class="coverage", output="both", out_file="coverage")
        assert logger.get_logger_file('not_exist') is None
