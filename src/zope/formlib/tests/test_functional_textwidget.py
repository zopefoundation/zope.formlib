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
"""TextWidget Tests
"""
import unittest

import zope.schema.interfaces
from zope.interface import Interface
from zope.interface import implementer
from zope.publisher.browser import TestRequest
from zope.schema import Choice
from zope.schema import TextLine

from zope.formlib import form
from zope.formlib.tests.functionalsupport import FunctionalWidgetTestCase
from zope.formlib.tests.support import patternExists
from zope.formlib.widgets import ChoiceInputWidget
from zope.formlib.widgets import DropdownWidget
from zope.formlib.widgets import TextWidget


class ITextLineTest(Interface):
    s1 = TextLine(
        required=True,
        min_length=2,
        max_length=10)

    s2 = TextLine(
        required=False,
        missing_value='')

    s3 = Choice(
        required=False,
        values=('Bob', 'is', 'Your', 'Uncle'))


@implementer(ITextLineTest)
class TextLineTest:

    def __init__(self):
        self.s1 = ''
        self.s2 = 'foo'
        self.s3 = None


class Form(form.EditForm):
    form_fields = form.fields(ITextLineTest)


class Test(FunctionalWidgetTestCase):
    widgets = [
        (zope.schema.interfaces.ITextLine, TextWidget),
        (zope.schema.interfaces.IChoice, ChoiceInputWidget),
        ((zope.schema.interfaces.IChoice,
          zope.schema.interfaces.IVocabularyTokenized), DropdownWidget)]

    def test_display_editform(self):
        foo = TextLineTest()
        request = TestRequest()

        # display edit view

        html = Form(foo, request)()

        # s1 and s2 should be displayed in text fields
        self.assertTrue(patternExists(
            '<input .* name="form.s1".* value="".*>', html))
        self.assertTrue(patternExists(
            '<input .* name="form.s2".* value="foo".*>', html))

        # s3 should be in a dropdown
        self.assertTrue(patternExists(
            '<select .*name="form.s3".*>', html))
        self.assertTrue(patternExists(
            '<option selected="selected" value="">.*</option>',
            html))

    def test_submit_editform(self):
        foo = TextLineTest()
        request = TestRequest()

        # submit edit view
        request.form['form.s1'] = 'foo'
        request.form['form.s2'] = 'bar'
        request.form['form.s3'] = 'Uncle'
        request.form['form.actions.apply'] = ''
        Form(foo, request)()

        # check new values in object
        self.assertEqual(foo.s1, 'foo')
        self.assertEqual(foo.s2, 'bar')
        self.assertEqual(foo.s3, 'Uncle')

    def test_invalid_type(self):
        """Tests text widget's handling of invalid unicode input.

        The text widget will succeed in converting any form input into
        unicode.
        """
        foo = TextLineTest()
        request = TestRequest()

        # submit invalid type for text line
        request.form['form.s1'] = ''
        request.form['form.actions.apply'] = ''
        html = Form(foo, request)()

        # We don't have a invalid field value
        # since we convert the value to unicode
        self.assertNotIn('Object is of wrong type.', html)

    def test_missing_value(self):
        foo = TextLineTest()
        request = TestRequest()

        request.form['form.s1'] = 'foo'
        request.form['form.s2'] = ''
        request.form['form.s3'] = ''
        request.form['form.actions.apply'] = ''
        Form(foo, request)()

        # check new values in object
        self.assertEqual(foo.s1, 'foo')
        self.assertEqual(foo.s2, '')   # default missing_value
        self.assertEqual(foo.s3, None)  # None is s3's missing_value

    def test_required_validation(self):
        foo = TextLineTest()
        request = TestRequest()

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
        self.assertEqual(html.find('missing', s2_index), -1)

    def test_invalid_value(self):
        foo = TextLineTest()
        request = TestRequest()

        # submit a value for s3 that isn't allowed
        request.form['form.s3'] = 'Bob is *Not* My Uncle'
        request.form['form.actions.apply'] = ''
        html = Form(foo, request)()

        s3_index = html.find('form.s3')
        invalid_index = html.find('Invalid')
        self.assertNotEqual(invalid_index, -1)
        self.assertGreater(invalid_index, s3_index)

    def test_length_validation(self):
        foo = TextLineTest()
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
        foo = TextLineTest()
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

        # check new value in object
        self.assertEqual(foo.s1, '')
        self.assertEqual(foo.s2, 'bar')
        self.assertIsNone(foo.s3)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test))
    return suite
