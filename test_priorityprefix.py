

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
