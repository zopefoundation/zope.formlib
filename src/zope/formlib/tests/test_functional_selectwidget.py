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
"""RadioWidget Tests
"""
import unittest

import zope.schema.interfaces
from zope.interface import Interface
from zope.interface import implementer
from zope.publisher.browser import TestRequest
from zope.schema import Choice

from zope.formlib import form
from zope.formlib.tests.functionalsupport import FunctionalWidgetTestCase
from zope.formlib.tests.support import patternExists
from zope.formlib.widgets import ChoiceInputWidget
from zope.formlib.widgets import DropdownWidget
from zope.formlib.widgets import TextWidget


class IRadioTest(Interface):

    s3 = Choice(
        required=False,
        values=('Bob', 'is', 'Your', 'Uncle'))

    s4 = Choice(
        required=True,
        values=('1', '2', '3'))


@implementer(IRadioTest)
class RadioTest:

    def __init__(self):
        self.s3 = None
        self.s4 = '1'


class Form(form.EditForm):
    form_fields = form.fields(IRadioTest)


class Test(FunctionalWidgetTestCase):
    widgets = [
        (zope.schema.interfaces.ITextLine, TextWidget),
        (zope.schema.interfaces.IChoice, ChoiceInputWidget),
        ((zope.schema.interfaces.IChoice,
          zope.schema.interfaces.IVocabularyTokenized), DropdownWidget)]

    def test_display_editform(self):
        foo = RadioTest()
        request = TestRequest()

        # display edit view
        html = Form(foo, request)()

        # S3
        self.assertTrue(patternExists(
            '<select .* name="form.s3".*>',
            html))
        self.assertTrue(patternExists(
            '<option selected="selected" value="">',
            html))
        self.assertTrue(patternExists(
            '<option value="Bob">',
            html))
        self.assertTrue(patternExists(
            '<option value="is">',
            html))
        self.assertTrue(patternExists(
            '<option value="Your">',
            html))
        self.assertTrue(patternExists(
            '<option value="Uncle">',
            html))

        # S4
        joined_body = "".join(html.split("\n"))
        self.assertFalse(patternExists(
            '<select.*name="form.s4".*>.*<option.*value="".*>',
            joined_body))
        self.assertTrue(patternExists(
            '<select .* name="form.s4".*>',
            html))
        self.assertTrue(patternExists(
            '<option selected="selected" value="1">',
            html))
        self.assertTrue(patternExists(
            '<option value="2">',
            html))
        self.assertTrue(patternExists(
            '<option value="3">',
            html))

        request = TestRequest()
        request.form['form.s3'] = 'Bob'
        request.form['form.s4'] = '2'
        request.form['form.actions.apply'] = ''

        # display edit view
        html = Form(foo, request)()

        self.assertTrue(patternExists(
            '<option selected="selected" value="Bob">',
            html))
        self.assertTrue(patternExists(
            '<option selected="selected" value="2">',
            html))

        html = Form(foo, request)()
        self.assertTrue(patternExists(
            '<option selected="selected" value="Bob">',
            html))
        self.assertTrue(patternExists(
            '<option selected="selected" value="2">',
            html))

        request = TestRequest()
        request.form['form.s3'] = ''
        request.form['form.actions.apply'] = ''

        html = Form(foo, request)()
        self.assertTrue(patternExists(
            '<option selected="selected" value="">',
            html))
        self.assertTrue(patternExists(
            '<option selected="selected" value="2">',
            html))

        request = TestRequest()
        html = Form(foo, request)()

        self.assertTrue(patternExists(
            '<option selected="selected" value="">',
            html))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test))
    return suite
