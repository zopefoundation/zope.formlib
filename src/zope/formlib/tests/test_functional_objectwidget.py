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
"""Test object widget
"""
import os
import unittest

import zope.schema.interfaces
import zope.traversing.interfaces
from zope.component import provideAdapter
from zope.component.testing import PlacelessSetup
from zope.configuration import xmlconfig
from zope.interface import Interface
from zope.interface import implementer
from zope.pagetemplate.pagetemplate import PageTemplate
from zope.publisher.browser import TestRequest
from zope.schema import Object
from zope.schema import TextLine
from zope.traversing.adapters import DefaultTraversable
from zope.traversing.testing import setUp as traversingSetUp

import zope.formlib
from zope.formlib import form
from zope.formlib.tests.support import VerifyResults
from zope.formlib.widgets import ObjectWidget


class ITestContact(Interface):
    name = TextLine()
    email = TextLine()


@implementer(ITestContact)
class TestContact:
    pass


class Form(form.EditForm):
    form_fields = form.fields(ITestContact)


class Test(PlacelessSetup, unittest.TestCase, VerifyResults):

    def setUp(self):
        super().setUp()
        traversingSetUp()
        # XXX this whole test setup is rather involved. Is there a
        # simpler way to publish widget_macros.pt? Probably.

        # load the registrations for formlib
        xmlconfig.file("configure.zcml",
                       zope.formlib)

        # set up the widget_macros macro
        macro_template = PageTemplate()
        widget_macros = os.path.join(os.path.dirname(zope.formlib.__file__),
                                     'widget_macros.pt')

        f = open(widget_macros)
        data = f.read()
        f.close()
        macro_template.write(data)

        @zope.component.adapter(None, None)
        @implementer(zope.traversing.interfaces.ITraversable)
        class view:
            def __init__(self, ob, r=None):
                pass

            def traverse(*args):
                return macro_template.macros
        provideAdapter(view, name='view')
        provideAdapter(DefaultTraversable, [None])

    def test_new(self):
        request = TestRequest()
        field = Object(ITestContact, __name__='foo')

        widget = ObjectWidget(field, request, TestContact)

        self.assertEqual(int(widget.hasInput()), 0)
        check_list = (
            'input', 'name="field.foo.name"',
            'input', 'name="field.foo.email"'
        )
        self.verifyResult(widget(), check_list)

    def test_edit(self):
        request = TestRequest(form={
            'field.foo.name': 'fred',
            'field.foo.email': 'fred@fred.com'
        })
        field = Object(ITestContact, __name__='foo')
        widget = ObjectWidget(field, request, TestContact)
        self.assertEqual(int(widget.hasInput()), 1)
        o = widget.getInputValue()
        self.assertEqual(hasattr(o, 'name'), 1)
        self.assertEqual(o.name, 'fred')
        self.assertEqual(o.email, 'fred@fred.com')
        check_list = (
            'input', 'name="field.foo.name"', 'value="fred"',
            'input', 'name="field.foo.email"', 'value="fred@fred.com"',
        )
        self.verifyResult(widget(), check_list)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test))
    return suite
