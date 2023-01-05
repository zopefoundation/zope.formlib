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
"""Widget name prefix tests
"""
import unittest

from zope.publisher.browser import TestRequest
from zope.schema import Text

from zope.formlib.tests import support
from zope.formlib.widgets import TextWidget


class Test(support.VerifyResults, unittest.TestCase):

    def setUp(self):
        field = Text(__name__='foo')
        request = TestRequest()
        request.form['spam.foo'] = 'Foo Value'
        self._widget = TextWidget(field, request)
        self._widget.setPrefix('spam')

    def testGetData(self):
        self.assertEqual(self._widget.getInputValue(), 'Foo Value')

    def testRender(self):
        value = 'Foo Value 2'
        check_list = ('type="text"', 'id="spam.foo"', 'name="spam.foo"',
                      'value="Foo Value 2"', 'size="20"')
        self._widget.setRenderedValue(value)
        self.verifyResult(self._widget(), check_list)
        check_list = ('type="hidden"',) + check_list[1:-1]
        self.verifyResult(self._widget.hidden(), check_list)
        check_list = ('style="color: red"',) + check_list
        self._widget.extra = 'style="color: red"'
        self.verifyResult(self._widget.hidden(), check_list)


class TestEmpty(support.VerifyResults, unittest.TestCase):

    def setUp(self):
        field = Text(__name__='foo')
        request = TestRequest()
        request.form['foo'] = 'Foo Value'
        self._widget = TextWidget(field, request)
        self._widget.setPrefix('')

    def testGetData(self):
        self.assertEqual(self._widget.getInputValue(), 'Foo Value')

    def testRender(self):
        check_list = ('id="foo"', 'name="foo"')
        self.verifyResult(self._widget(), check_list)
        self.verifyResult(self._widget.hidden(), check_list)


def test_suite():
    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromTestCase(Test),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestEmpty),
    ))
