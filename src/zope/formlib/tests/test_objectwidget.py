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
"""Object Widget tests
"""
import doctest
import unittest

from zope.component import provideAdapter
from zope.component import testing
from zope.interface import Interface
from zope.interface import implementer
from zope.publisher.browser import TestRequest
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.schema import Object
from zope.schema import TextLine
from zope.schema.interfaces import ITextLine

from zope.formlib.interfaces import IInputWidget
from zope.formlib.interfaces import IWidgetInputErrorView
from zope.formlib.interfaces import MissingInputError
from zope.formlib.tests.test_browserwidget import BrowserWidgetTest
from zope.formlib.widgets import ObjectWidget
from zope.formlib.widgets import TextWidget


class ITestContact(Interface):
    name = TextLine()
    email = TextLine()


@implementer(ITestContact)
class TestContact:
    pass


@implementer(IWidgetInputErrorView)
class ObjectWidgetInputErrorView:

    def __init__(self, error, request):
        self.error = error
        self.request = request

    def snippet(self):
        return repr(self.error)


class ObjectWidgetTest(BrowserWidgetTest):
    """Documents and tests the object widget.

        >>> from zope.interface.verify import verifyClass
        >>> verifyClass(IInputWidget, ObjectWidget)
        True
    """

    _FieldFactory = Object

    def _WidgetFactory(self, context, request, **kw):
        kw.update({'factory': TestContact})
        return ObjectWidget(context, request, **kw)

    def setUpContent(self, desc='', title='Foo Title'):
        provideAdapter(TextWidget, (ITextLine, IDefaultBrowserLayer),
                       IInputWidget)

        class ITestContent(Interface):
            foo = self._FieldFactory(
                ITestContact,
                title=title,
                description=desc
            )

        @implementer(ITestContent)
        class TestObject:
            pass

        self.content = TestObject()
        self.field = ITestContent['foo']
        self.request = TestRequest(HTTP_ACCEPT_LANGUAGE='pl')
        self.request.form['field.foo'] = 'Foo Value'
        self._widget = self._WidgetFactory(self.field, self.request)

    def setUp(self):
        super().setUp()
        self.field = Object(ITestContact, __name__='foo')
        provideAdapter(TextWidget,
                       (ITextLine, IDefaultBrowserLayer),
                       IInputWidget)

    def test_applyChanges(self):
        self.request.form['field.foo.name'] = 'Foo Name'
        self.request.form['field.foo.email'] = 'foo@foo.test'
        widget = self._WidgetFactory(self.field, self.request)

        self.assertEqual(widget.applyChanges(self.content), True)
        self.assertEqual(hasattr(self.content, 'foo'), True)
        self.assertEqual(isinstance(self.content.foo, TestContact), True)
        self.assertEqual(self.content.foo.name, 'Foo Name')
        self.assertEqual(self.content.foo.email, 'foo@foo.test')

    def test_error(self):
        provideAdapter(
            ObjectWidgetInputErrorView,
            (MissingInputError, TestRequest),
            IWidgetInputErrorView)

        widget = self._WidgetFactory(self.field, self.request)
        self.assertRaises(MissingInputError, widget.getInputValue)
        error_html = widget.error()
        self.assertIn(
            "email: MissingInputError('field.foo.email', '', None)",
            error_html)
        self.assertIn(
            "name: MissingInputError('field.foo.name', '', None)", error_html)

    def test_applyChangesNoChange(self):
        self.content.foo = TestContact()
        self.content.foo.name = 'Foo Name'
        self.content.foo.email = 'foo@foo.test'

        self.request.form['field.foo.name'] = 'Foo Name'
        self.request.form['field.foo.email'] = 'foo@foo.test'
        widget = self._WidgetFactory(self.field, self.request)
        widget.setRenderedValue(self.content.foo)

        self.assertEqual(widget.applyChanges(self.content), False)
        self.assertEqual(hasattr(self.content, 'foo'), True)
        self.assertEqual(isinstance(self.content.foo, TestContact), True)
        self.assertEqual(self.content.foo.name, 'Foo Name')
        self.assertEqual(self.content.foo.email, 'foo@foo.test')


def test_suite():
    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromTestCase(ObjectWidgetTest),
        doctest.DocFileSuite(
            '../objectwidget.rst',
            setUp=testing.setUp, tearDown=testing.tearDown),
        doctest.DocTestSuite(),
    ))
