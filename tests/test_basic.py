#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import unittest
# import nose
# import nose.tools

import pyrochess

class TestModule(unittest.TestCase):
    """Nose test class."""

    # @classmethod
    # def setUpClass(self):
    #     pass

    # @classmethod
    # def tearDownClass(self):
    #     pass

    def setUp(self):
        """Sets up the test."""
        self.a = 1
        mainloop.mainloop()

    def tearDown(self):
        """Tears down the test."""
        pass

    def testMain(self):
        """Test call to main."""
        # nose.tools.eq_(self.a, 1)
        assert self.a == 1
