##############################################################################
#
# Copyright (c) 2005 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""

import unittest
import pytz
from zope import component, interface
import zope.interface.common.idatetime
import zope.i18n
import zope.publisher.interfaces
import zope.publisher.interfaces.browser
import zope.schema.interfaces
import zope.app.form.browser
import zope.app.form.browser.exception
import zope.app.form.browser.interfaces
import zope.app.form.interfaces
from zope.app.testing import placelesssetup
import zope.app.traversing.adapters

from zope.formlib import interfaces, namedtemplate, form

@interface.implementer(zope.interface.common.idatetime.ITZInfo)
@component.adapter(zope.publisher.interfaces.IRequest)
def requestToTZInfo(request):
    return pytz.timezone('US/Hawaii')

def pageSetUp(test):
    placelesssetup.setUp(test)
    component.provideAdapter(
        zope.app.traversing.adapters.DefaultTraversable,
        [None],
        )

@component.adapter(interfaces.IForm)
@namedtemplate.NamedTemplateImplementation
def TestTemplate(self):
    status = self.status
    if status:
        status = zope.i18n.translate(status,
                                     context=self.request,
                                     default=self.status)
        if getattr(status, 'mapping', 0):
            status = zope.i18n.interpolate(status, status.mapping)
        print status
        
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
    placelesssetup.setUp(test)
    component.provideAdapter(
        zope.app.form.browser.TextWidget,
        [zope.schema.interfaces.ITextLine,
         zope.publisher.interfaces.browser.IBrowserRequest,
         ],
        zope.app.form.interfaces.IInputWidget,
        )
    component.provideAdapter(
        zope.app.form.browser.FloatWidget,
        [zope.schema.interfaces.IFloat,
         zope.publisher.interfaces.browser.IBrowserRequest,
         ],
        zope.app.form.interfaces.IInputWidget,
        )
    component.provideAdapter(
        zope.app.form.browser.UnicodeDisplayWidget,
        [zope.schema.interfaces.IInt,
         zope.publisher.interfaces.browser.IBrowserRequest,
         ],
        zope.app.form.interfaces.IDisplayWidget,
        )
    component.provideAdapter(
        zope.app.form.browser.IntWidget,
        [zope.schema.interfaces.IInt,
         zope.publisher.interfaces.browser.IBrowserRequest,
         ],
        zope.app.form.interfaces.IInputWidget,
        )
    component.provideAdapter(
        zope.app.form.browser.UnicodeDisplayWidget,
        [zope.schema.interfaces.IFloat,
         zope.publisher.interfaces.browser.IBrowserRequest,
         ],
        zope.app.form.interfaces.IDisplayWidget,
        )
    component.provideAdapter(
        zope.app.form.browser.UnicodeDisplayWidget,
        [zope.schema.interfaces.ITextLine,
         zope.publisher.interfaces.browser.IBrowserRequest,
         ],
        zope.app.form.interfaces.IDisplayWidget,
        )
    component.provideAdapter(
        zope.app.form.browser.DatetimeDisplayWidget,
        [zope.schema.interfaces.IDatetime,
         zope.publisher.interfaces.browser.IBrowserRequest,
         ],
        zope.app.form.interfaces.IDisplayWidget,
        )
    component.provideAdapter(
        zope.app.form.browser.exception.WidgetInputErrorView,
        [zope.app.form.interfaces.IWidgetInputError,
         zope.publisher.interfaces.browser.IBrowserRequest,
         ],
        zope.app.form.browser.interfaces.IWidgetInputErrorView,
        )
    component.provideAdapter(TestTemplate, name='default')
    component.provideAdapter(requestToTZInfo)
    component.provideAdapter(form.render_submit_button, name='render')

def makeSureRenderCanBeCalledWithoutCallingUpdate():
    """\

    >>> from zope.formlib import form
    >>> from zope import interface, schema
    >>> class IOrder(interface.Interface):
    ...     identifier = schema.Int(title=u"Identifier", readonly=True)
    ...     name = schema.TextLine(title=u"Name")
    ...     min_size = schema.Float(title=u"Minimum size")
    ...     max_size = schema.Float(title=u"Maximum size")
    ...     now = schema.Datetime(title=u"Now", readonly=True)

    >>> class MyForm(form.EditForm):
    ...     form_fields = form.fields(IOrder, keep_readonly=['identifier'])

    >>> class Order:
    ...     interface.implements(IOrder)
    ...     identifier = 1
    ...     name = 'unknown'
    ...     min_size = 1.0
    ...     max_size = 10.0

    >>> from zope.publisher.browser import TestRequest

    >>> myform = MyForm(Order(), TestRequest())
    >>> print myform.render() # doctest: +NORMALIZE_WHITESPACE
    1
    <input class="textType" id="form.name" name="form.name"
           size="20" type="text" value="unknown"  />
    <input class="textType" id="form.min_size" name="form.min_size"
           size="10" type="text" value="1.0"  />
    <input class="textType" id="form.max_size" name="form.max_size"
           size="10" type="text" value="10.0"  />
    <input type="submit" id="form.actions.apply" name="form.actions.apply"
           value="Apply" class="button" />


"""

def test_suite():
    from zope.testing import doctest
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'page.txt',
            setUp=pageSetUp, tearDown=placelesssetup.tearDown,
            ),
        doctest.DocFileSuite(
            'form.txt',
            setUp=formSetUp, tearDown=placelesssetup.tearDown,
            ),
        doctest.DocTestSuite(
            setUp=formSetUp, tearDown=placelesssetup.tearDown,
            ),
        doctest.DocFileSuite(
            'namedtemplate.txt',
            setUp=pageSetUp, tearDown=placelesssetup.tearDown,
            ),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

