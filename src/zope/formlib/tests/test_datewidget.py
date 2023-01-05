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
"""Date Widget tests
"""
import datetime
import doctest
import unittest

from zope.interface.verify import verifyClass
from zope.schema import Date

from zope.formlib.interfaces import ConversionError
from zope.formlib.interfaces import IInputWidget
from zope.formlib.interfaces import WidgetInputError
from zope.formlib.tests.test_browserwidget import SimpleInputWidgetTest
from zope.formlib.widgets import DateI18nWidget
from zope.formlib.widgets import DateWidget


class DateWidgetTest(SimpleInputWidgetTest):
    """Documents and tests the date widget.

        >>> verifyClass(IInputWidget, DateWidget)
        True
    """

    _FieldFactory = Date
    _WidgetFactory = DateWidget

    def testRender(self):
        super().testRender(
            datetime.date(2003, 3, 26),
            ('type="text"', 'id="field.foo"', 'name="field.foo"',
                'value="2003-03-26"'))

    def test_hasInput(self):
        del self._widget.request.form['field.foo']
        self.assertFalse(self._widget.hasInput())
        self._widget.request.form['field.foo'] = ''
        self.assertTrue(self._widget.hasInput())
        self._widget.request.form['field.foo'] = '2003-03-26'
        self.assertTrue(self._widget.hasInput())

    def test_getInputValue(self,
                           value='2004-03-26',
                           check_value=datetime.date(2004, 3, 26)):
        self._widget.request.form['field.foo'] = ''
        self.assertRaises(WidgetInputError, self._widget.getInputValue)
        self._widget.request.form['field.foo'] = value
        self.assertEqual(self._widget.getInputValue(), check_value)
        self._widget.request.form['field.foo'] = 'abc'
        self.assertRaises(ConversionError, self._widget.getInputValue)


class DateI18nWidgetTest(SimpleInputWidgetTest):
    """Documents and tests the i18n date widget.

        >>> verifyClass(IInputWidget, DateI18nWidget)
        True
    """

    _FieldFactory = Date
    _WidgetFactory = DateI18nWidget

    def testDefaultDisplayStyle(self):
        self.assertFalse(self._widget.displayStyle)

    def testRender(self):
        super().testRender(
            datetime.date(2003, 3, 26),
            ('type="text"', 'id="field.foo"', 'name="field.foo"',
                'value="26.03.2003"'))

    def testRenderShort(self):
        self._widget.displayStyle = "short"
        super().testRender(
            datetime.datetime(2004, 3, 26, 12, 58, 59),
            ('type="text"', 'id="field.foo"', 'name="field.foo"',
                'value="26.03.04"'))

    def testRenderMedium(self):
        self._widget.displayStyle = "medium"
        super().testRender(
            datetime.datetime(2004, 3, 26, 12, 58, 59),
            ('type="text"', 'id="field.foo"', 'name="field.foo"',
                'value="26.03.2004"'))

    def testRenderLong(self):
        self._widget.displayStyle = "long"
        super().testRender(
            datetime.datetime(2004, 3, 26, 12, 58, 59),
            ('type="text"', 'id="field.foo"', 'name="field.foo"',
                'value="26 \u043c\u0430\u0440\u0442\u0430 2004 \u0433."'))

    def testRenderFull(self):
        self._widget.displayStyle = "full"
        super().testRender(
            datetime.datetime(2004, 3, 26, 12, 58, 59),
            ('type="text"', 'id="field.foo"', 'name="field.foo"',
                'value="26 \u043c\u0430\u0440\u0442\u0430 2004 \u0433."'))

    def test_hasInput(self):
        del self._widget.request.form['field.foo']
        self.assertFalse(self._widget.hasInput())
        self._widget.request.form['field.foo'] = ''
        self.assertTrue(self._widget.hasInput())
        self._widget.request.form['field.foo'] = '26.03.2003'
        self.assertTrue(self._widget.hasInput())

    def test_getDefaultInputValue(self,
                                  value='26.03.2004',
                                  check_value=datetime.date(2004, 3, 26)):
        self._widget.request.form['field.foo'] = ''
        self.assertRaises(WidgetInputError, self._widget.getInputValue)
        self._widget.request.form['field.foo'] = value
        self.assertEqual(self._widget.getInputValue(), check_value)
        self._widget.request.form['field.foo'] = 'abc'
        self.assertRaises(ConversionError, self._widget.getInputValue)

    def test_getShortInputValue(self):
        self._widget.displayStyle = "short"
        self.test_getDefaultInputValue('26.03.04')

    def test_getMediumInputValue(self):
        self._widget.displayStyle = "medium"
        self.test_getDefaultInputValue('26.03.2004')

    def test_getLongInputValue(self):
        self._widget.displayStyle = "long"
        self.test_getDefaultInputValue(
            '26 \u043c\u0430\u0440\u0442\u0430 2004 \u0433.'
        )

    def test_getFullInputValue(self):
        self._widget.displayStyle = "full"
        self.test_getDefaultInputValue(
            '26 \u043c\u0430\u0440\u0442\u0430 2004 \u0433.'
        )


def test_suite():
    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromTestCase(DateWidgetTest),
        unittest.defaultTestLoader.loadTestsFromTestCase(DateI18nWidgetTest),
        doctest.DocTestSuite(),
    ))
