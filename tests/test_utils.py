#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" """

from unittest import TestCase
from utils import *

class UtilsTest(TestCase):

    def test_make_window(self):
        """Make sure that pagination windows work."""
        self.assertEqual(make_window(17, 4), [16, 17, 18, 19])
        self.assertEqual(make_window(6, 5), [4, 5, 6, 7, 8])

    def test_page_context(self):
        """Test page context's for pagination displays."""
        self.assertEqual(page_context(1, total=5), [1, 2, 3, 4, 5])
        self.assertEqual(page_context(4, window=10, total=15),
            [1, 2, 3, 4, 5, 6, 7, 8, '...', 14, 15])
        self.assertEqual(page_context(9, window=9, total=15),
            [1, 2, '...', 7, 8, 9, 10, 11, '...', 14, 15])
        self.assertEqual(page_context(9, window=9, total=15, inter='..'),
            [1, 2, '..', 7, 8, 9, 10, 11, '..', 14, 15])
        self.assertEqual(page_context(11, total=14),
            [1, 2, '...', 9, 10, 11, 12, 13, 14])
        self.assertEqual(page_context(4, total=35),
            [1, 2, 3, 4, 5, 6, '...', 34, 35])

    def test_page_object(self):
        """Test a page object for proper behavior."""
        p = Page(1, per_page=10, total_objects=101, window=5)
        self.assertEqual(p.context(), [1, 2, 3, '...', 10, 11])
        p = Page(19, per_page=10, total_objects=1001, window=10)
        self.assertEqual(p.context(),
            [1, 2, '...', 17, 18, 19, 20, 21, 22, '...', 100, 101])
        p = Page(20, per_page=10, total_objects=1001, window=10)
        self.assertEqual(p.context(),
            [1, 2, '...', 18, 19, 20, 21, 22, 23, '...', 100, 101])
