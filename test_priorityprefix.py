

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
