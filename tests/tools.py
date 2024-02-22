# encoding=UTF-8

# Copyright © 2024 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

import unittest

def testcase(f):
    class TestCase(unittest.TestCase):  # pylint: disable=redefined-outer-name
        @staticmethod
        def test():
            return f()
        def __str__(self):
            return f'{f.__module__}.{f.__name__}'
    return TestCase

tc = unittest.TestCase('__hash__')

assert_equal = tc.assertEqual
assert_is_none = tc.assertIsNone

del tc

class TestCase(unittest.TestCase):
    def __str__(self):
        cls = unittest.util.strclass(self.__class__)
        name = self._testMethodName
        return f'{cls}.{name}'

__all__ = [
    'testcase',
    'TestCase',
    # nose-compatible:
    'assert_equal',
    'assert_is_none',
]

# vim:ts=4 sts=4 sw=4 et
