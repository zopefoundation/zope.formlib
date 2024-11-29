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
"""TextArea Functional Tests
"""
import unittest

import zope.schema.interfaces
from zope.interface import Interface
from zope.interface import implementer
from zope.publisher.browser import TestRequest
from zope.schema import Text

from zope.formlib import form
from zope.formlib.tests.functionalsupport import FunctionalWidgetTestCase
from zope.formlib.tests.support import patternExists
from zope.formlib.widgets import TextAreaWidget


class ITextTest(Interface):
    s1 = Text(
        required=True,
        min_length=2,
        max_length=10)

    s2 = Text(
        required=False,
        missing_value='')

    s3 = Text(
        required=False)


@implementer(ITextTest)
class TextTest:

    def __init__(self):
        self.s1 = ''
        self.s2 = 'foo'
        self.s3 = None


class Form(form.EditForm):
    form_fields = form.fields(ITextTest)


class Test(FunctionalWidgetTestCase):
    widgets = [
        (zope.schema.interfaces.IText, TextAreaWidget),
    ]

    def test_display_editform(self):
        foo = TextTest()
        request = TestRequest()

        html = Form(foo, request)()

        # all fields should be displayed in text fields
        self.assertTrue(patternExists(
            '<textarea .* name="form.s1".*></textarea>',
            html))
        self.assertTrue(patternExists(
            '<textarea .* name="form.s2".*>foo</textarea>',
            html))
        self.assertTrue(patternExists(
            '<textarea .* name="form.s3".*></textarea>',
            html))

    def test_submit_editform(self):
        foo = TextTest()
        request = TestRequest()

        request.form['form.s1'] = 'foo'
        request.form['form.s2'] = 'bar'
        request.form['form.s3'] = 'baz'
        request.form['form.actions.apply'] = ''

        Form(foo, request)()

        # check new values in object
        self.assertEqual(foo.s1, 'foo')
        self.assertEqual(foo.s2, 'bar')
        self.assertEqual(foo.s3, 'baz')

    def test_invalid_type(self):
        """Tests textarea widget's handling of invalid unicode input.

        The text widget will succeed in converting any form input into
        unicode.
        """
        foo = TextTest()
        request = TestRequest()

        # submit invalid type for text
        request.form['form.s1'] = 123  # not unicode
        request.form['form.actions.apply'] = ''

        html = Form(foo, request)()

        # Note: We don't have a invalid field value
        # since we convert the value to unicode
        self.assertNotIn('Object is of wrong type', html)

    def test_missing_value(self):
        foo = TextTest()
        request = TestRequest()

        # submit missing values for s2 and s3
        request.form['form.s1'] = 'foo'
        request.form['form.s2'] = ''
        request.form['form.s3'] = ''
        request.form['form.actions.apply'] = ''

        Form(foo, request)()

        # check new value in object
        self.assertEqual(foo.s1, 'foo')
        self.assertEqual(foo.s2, '')   # default missing_value
        self.assertEqual(foo.s3, None)  # None is s3's missing_value

    def test_required_validation(self):
        foo = TextTest()
        request = TestRequest()

        # submit missing values for required field s1
        request.form['form.s1'] = ''
        request.form['form.s2'] = ''
        request.form['form.s3'] = ''
        request.form['form.actions.apply'] = ''

        html = Form(foo, request)()

        # confirm error msgs
        s1_index = html.find('form.s1')
        s2_index = html.find('form.s2')
        missing_index = html.find('missing')
        self.assertTrue(s1_index < missing_index < s2_index)

    def test_length_validation(self):
        foo = TextTest()
        request = TestRequest()

        # submit value for s1 that is too short
        request.form['form.s1'] = 'a'
        request.form['form.actions.apply'] = ''

        html = Form(foo, request)()

        self.assertIn('Value is too short', html)

        # submit value for s1 that is too long
        request.form['form.s1'] = '12345678901'
        request.form['form.actions.apply'] = ''
        html = Form(foo, request)()

        self.assertIn('Value is too long', html)

    def test_omitted_value(self):
        foo = TextTest()
        request = TestRequest()

        # confirm default values
        self.assertEqual(foo.s1, '')
        self.assertEqual(foo.s2, 'foo')
        self.assertIsNone(foo.s3)

        # submit change with only s2 present -- note that required
        # field s1 is omitted, which should not cause a validation error
        request.form['form.s2'] = 'bar'
        request.form['form.actions.apply'] = ''

        Form(foo, request)()

        # check new values in object
        self.assertEqual(foo.s1, '')
        self.assertEqual(foo.s2, 'bar')
        self.assertIsNone(foo.s3)

    def test_conversion(self):
        foo = TextTest()
        request = TestRequest()

        # confirm that line terminators are converted correctly on post
        request.form['form.s2'] = 'line1\r\nline2'  # CRLF per RFC 822
        request.form['form.actions.apply'] = ''
        html = Form(foo, request)()

        self.assertEqual(foo.s2, 'line1\nline2')

        # confirm conversion to HTML

        request = TestRequest()
        html = Form(foo, request)()
        self.assertTrue(patternExists('line1\r\nline2', html))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test))
    return suite
