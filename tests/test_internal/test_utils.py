#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from pyhermes.utils import retry


class PublisherDecoratorTestCase(unittest.TestCase):
    def test_retry_without_any_exceptions(self):
        logger_mock = mock.MagicMock()

        @retry(max_attempts=3, logger=logger_mock)
        def test_func(a):
            return a

        result = test_func('ok')
        self.assertEqual(result, 'ok')
        self.assertEqual(logger_mock.warning.call_count, 0)

    def test_retry_with_exception_in_the_middle(self):
        tries = [0]
        logger_mock = mock.MagicMock()

        @retry(max_attempts=3, logger=logger_mock)
        def test_func(a):
            tries[0] += 1
            if tries[0] <= 2:
                raise ValueError()
            return a

        result = test_func('ok')
        self.assertEqual(result, 'ok')
        self.assertEqual(logger_mock.warning.call_count, 2)

    def test_retry_with_exception_after_tries(self):
        logger_mock = mock.MagicMock()

        @retry(max_attempts=3, logger=logger_mock)
        def test_func(a):
            raise ValueError()

        with self.assertRaises(ValueError):
            test_func('ok')

        self.assertEqual(logger_mock.warning.call_count, 2)

    def test_retry_with_custom_exception_no_retry_on_wrong_exception(self):
        logger_mock = mock.MagicMock()

        @retry(logger=logger_mock, retry_exceptions=(IndexError,))
        def test_func(a):
            raise ValueError()

        with self.assertRaises(ValueError):
            test_func('ok')

        self.assertEqual(logger_mock.warning.call_count, 0)

    def test_retry_with_custom_exception_retry_on_proper_exception(self):
        logger_mock = mock.MagicMock()

        @retry(logger=logger_mock, retry_exceptions=(IndexError,))
        def test_func(a):
            raise IndexError()

        with self.assertRaises(IndexError):
            test_func('ok')

        self.assertEqual(logger_mock.warning.call_count, 0)
