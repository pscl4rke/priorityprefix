

import logging
import unittest

import priorityprefix


class TestLevelConversion(unittest.TestCase):

    def test_debug(self):
        self.assertEqual(priorityprefix.level_to_priority(logging.DEBUG), 7)

    def test_info(self):
        self.assertEqual(priorityprefix.level_to_priority(logging.INFO), 6)

    def test_warning(self):
        self.assertEqual(priorityprefix.level_to_priority(logging.WARNING), 4)

    def test_error(self):
        self.assertEqual(priorityprefix.level_to_priority(logging.ERROR), 3)

    def test_critical(self):
        self.assertEqual(priorityprefix.level_to_priority(logging.CRITICAL), 2)

    def test_custom_level(self):
        VERY_LOW_LEVEL = 5
        self.assertEqual(priorityprefix.level_to_priority(VERY_LOW_LEVEL), 7)


class TestFormatter(unittest.TestCase):

    def setUp(self):
        self.fmtr = priorityprefix.FormattingWrapper(logging.Formatter())

    def test_info_message(self):
        record = logging.makeLogRecord({"msg": "Hello World", "levelno": logging.INFO})
        expected = "<6>Hello World"
        self.assertEqual(self.fmtr.format(record), expected)

    def test_warning_message(self):
        record = logging.makeLogRecord({"msg": "Oh Dear", "levelno": logging.WARNING})
        expected = "<4>Oh Dear"
        self.assertEqual(self.fmtr.format(record), expected)

    def test_multiline_message(self):
        message = "Error\n  Was\nHere"
        record = logging.makeLogRecord({"msg": message, "levelno": logging.ERROR})
        expected = "<3>Error\n<3>  Was\n<3>Here"
        self.assertEqual(self.fmtr.format(record), expected)


class TestPrefixAdding(unittest.TestCase):

    def test_single_line(self):
        output = priorityprefix.prefix_all_lines(1, "Hello World")
        self.assertEqual(output, "<1>Hello World")

    def test_trailing_new_line(self):
        output = priorityprefix.prefix_all_lines(3, "Hello World\n")
        self.assertEqual(output, "<3>Hello World\n")

    def test_multiline(self):
        output = priorityprefix.prefix_all_lines(6, "Hello\nWorld\n")
        self.assertEqual(output, "<6>Hello\n<6>World\n")


class TestInstall(unittest.TestCase):

    def test_on_a_logger(self):
        logger = logging.getLogger("testingexample")
        logger.addHandler(logging.NullHandler())
        self.assertGreater(len(logger.handlers), 0)
        priorityprefix.install(logger)
        self.assertEqual(type(logger.handlers[0].formatter),
                        priorityprefix.FormattingWrapper)
