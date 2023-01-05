##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Float Widget tests
"""
import doctest
import unittest

from zope.interface.verify import verifyClass
from zope.schema import Float

from zope.formlib.interfaces import ConversionError
from zope.formlib.interfaces import IInputWidget
from zope.formlib.interfaces import WidgetInputError
from zope.formlib.tests.test_browserwidget import SimpleInputWidgetTest
from zope.formlib.widgets import FloatWidget


class FloatWidgetTest(SimpleInputWidgetTest):
    """Documents and tests the float widget.

        >>> verifyClass(IInputWidget, FloatWidget)
        True
    """

    _FieldFactory = Float
    _WidgetFactory = FloatWidget

    def test_hasInput(self):
        del self._widget.request.form['field.foo']
        self.assertFalse(self._widget.hasInput())
        # widget has input, even if input is an empty string
        self._widget.request.form['field.foo'] = ''
        self.assertTrue(self._widget.hasInput())
        self._widget.request.form['field.foo'] = '123'
        self.assertTrue(self._widget.hasInput())

    def test_getInputValue(self):
        self._widget.request.form['field.foo'] = ''
        self.assertRaises(WidgetInputError, self._widget.getInputValue)
        self._widget.request.form['field.foo'] = '123.45'
        self.assertEqual(self._widget.getInputValue(), 123.45)
        self._widget.request.form['field.foo'] = 'abc'
        self.assertRaises(ConversionError, self._widget.getInputValue)


def test_suite():
    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromTestCase(FloatWidgetTest),
        doctest.DocTestSuite(),
    ))
