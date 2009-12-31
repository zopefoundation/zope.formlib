##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
"""Radio Widget Functional Tests

$Id$
"""
import unittest

from zope.interface import Interface, implements
from zope.schema import Bool
from zope.formlib import form
from zope.publisher.browser import TestRequest
from zope.formlib.tests.support import patternExists
from zope.formlib.widgets import BooleanRadioWidget
from zope.component.testing import setUp, tearDown
from zope.component import provideAdapter
from zope.i18n.testing import setUp as i18nSetUp
from zope.publisher.interfaces.browser import IBrowserRequest
import zope.formlib
from zope.formlib.tests.test_formlib import requestToTZInfo
from zope.formlib.exception import WidgetInputErrorView
from zope.formlib.interfaces import IWidgetInputError, IWidgetInputErrorView
import zope.interface
from zope.formlib.errors import InvalidErrorView
import zope.schema.interfaces
from zope.formlib.interfaces import IInputWidget, IForm
from zope.interface import Invalid
from zope.browserpage.namedtemplate import NamedTemplateImplementation
from zope.component import adapter
import zope.i18n

@adapter(IForm)
@NamedTemplateImplementation
def TestTemplate(self):
    status = self.status
    if status:
        status = zope.i18n.translate(status,
                                     context=self.request,
                                     default=self.status)
        if getattr(status, 'mapping', 0):
            status = zope.i18n.interpolate(status, status.mapping)

    result = []

    if self.errors:
        for error in self.errors:
            result.append("%s: %s" % (error.__class__.__name__, error))

    for w in self.widgets:
        result.append(w())
        error = w.error()
        if error:
            result.append(str(error))

    for action in self.availableActions():
        result.append(action.render())

    return '\n'.join(result)

def formSetUp(test):
    setUp(test)
    i18nSetUp(test)
    provideAdapter(
        BooleanRadioWidget,
        (zope.schema.interfaces.IBool,
         IBrowserRequest),
        IInputWidget)
    
    provideAdapter(
       WidgetInputErrorView,
        (IWidgetInputError,
         IBrowserRequest),
        IWidgetInputErrorView,
        )
    provideAdapter(
        InvalidErrorView,
        (Invalid,
         IBrowserRequest),
        IWidgetInputErrorView,
        )

    provideAdapter(TestTemplate, name='default')
    provideAdapter(requestToTZInfo)
    provideAdapter(
        zope.formlib.form.render_submit_button, name='render')
    
class IFoo(Interface):

    bar = Bool(title=u'Bar')

class Foo(object):

    implements(IFoo)

    def __init__(self):
        self.bar = True

class Form(form.EditForm):
    form_fields = form.fields(IFoo)
    form_fields['bar'].custom_widget = BooleanRadioWidget

    
class Test(unittest.TestCase):
    def setUp(self):
        formSetUp(self)

    def tearDown(self):
        tearDown(self)
    
    def test_display_editform(self):
        foo = Foo()
        request = TestRequest()
        html = Form(foo, request)()

        # bar field should be displayed as two radio buttons
        self.assert_(patternExists(
            '<input .*checked="checked".*name="form.bar".*type="radio".*'
            'value="on".* />',
            html))
        self.assert_(patternExists(
            '<input .*name="form.bar".*type="radio".*value="off".* />',
            html))

        # a hidden element is used to note that the field is present
        self.assert_(patternExists(
            '<input name="form.bar-empty-marker" type="hidden" value="1".* />',
            html))


    def test_submit_editform(self):
        foo = Foo()
        request = TestRequest()
        request.form['form.bar'] = 'off'
        request.form['form.actions.apply'] = u''
        html = Form(foo, request)()

        self.assertEqual(foo.bar, False)

    def test_missing_value(self):
        foo = Foo()
        request = TestRequest()
        
        # temporarily make bar field not required
        IFoo['bar'].required = False

        # submit missing value for bar
        request.form['form.bar-empty-marker'] = ''
        request.form['form.actions.apply'] = u''

        html = Form(foo, request)()
 
        # confirm use of missing_value as new object value
        self.assert_(IFoo['bar'].missing_value is None)
        self.assert_(foo.bar is None)

        # restore bar required state
        IFoo['bar'].required = True


    def test_required_validation(self):
        foo = Foo()
        request = TestRequest()

        self.assert_(IFoo['bar'].required)

        # submit missing value for bar
        request.form['form.bar-empty-marker'] = ''
        request.form['form.actions.apply'] = u''

        html = Form(foo, request)()
        
        # confirm error msgs
        self.assert_('Required input is missing' in html)
        

    def test_invalid_allowed_value(self):
        foo = Foo()
        request = TestRequest()

        # submit a value for bar isn't allowed
        request.form['form.bar'] = 'bogus'
        request.form['form.actions.apply'] = u''
        html = Form(foo, request)()

        self.assert_('Invalid value' in html)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')
