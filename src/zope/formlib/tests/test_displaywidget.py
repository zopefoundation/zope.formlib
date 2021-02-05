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
"""Generic Text Widgets tests
"""
import unittest
from doctest import DocTestSuite

from zope.formlib.widget import DisplayWidget, UnicodeDisplayWidget
from .support import checker


def test_implemented_interfaces():
    """Make sure that the display widget implements the correct interfaces.

    Like all browser-used widgets, DisplayWidget must implement
    `IBrowserWidget`.

    >>> from zope.formlib.interfaces import IBrowserWidget
    >>> from zope.interface import implementedBy
    >>> from zope.interface.verify import verifyClass
    >>> IBrowserWidget in implementedBy(DisplayWidget)
    True
    >>> verifyClass(IBrowserWidget, DisplayWidget)
    True

    But unlike most other widgets in this package, the display widget is *not*
    an `IInputWidget`.


    >>> from zope.formlib.interfaces import IInputWidget
    >>> IInputWidget in implementedBy(DisplayWidget)
    False
    """


def test_not_required():
    """Make sure that display widgets are not required

    >>> from zope.publisher.browser import TestRequest
    >>> from zope.schema import TextLine
    >>> field = TextLine(title = u'Title',
    ...                  __name__ = u'title',
    ...                  default = u'<My Title>')
    >>> widget = DisplayWidget(field, TestRequest())
    >>> widget.required
    False

    """


def test_value_escaping():
    """Make sure that the returned values are correctly escaped.

    First we need to create a field that is the context of the display widget.

    >>> from zope.schema import TextLine
    >>> field = TextLine(title = u'Title',
    ...                  __name__ = u'title',
    ...                  default = u'<My Title>')

    >>> field = field.bind(None)

    Now we are ready to instantiate our widget.

    >>> from zope.publisher.browser import TestRequest
    >>> widget = DisplayWidget(field, TestRequest())

    If no data was specified in the widget, the field's default value will be
    chosen.

    >>> widget()
    u'&lt;My Title&gt;'

    Now let's set a value and make sure that, when output, it is also
    correctly escaped.

    >>> widget.setRenderedValue(u'<Another Title>')
    >>> widget()
    u'&lt;Another Title&gt;'

    When the value is the missing_value, the empty string should be
    displayed::

    >>> from zope.publisher.browser import TestRequest
    >>> field = TextLine(title = u'Title',
    ...                  __name__ = u'title',
    ...                  required = False)

    >>> field = field.bind(None)
    >>> widget = DisplayWidget(field, TestRequest())
    >>> widget.setRenderedValue(field.missing_value)

    >>> widget()
    ''

    If there's no default for the field and the value is missing on
    the bound object, the empty string should still be displayed::

    >>> field = TextLine(title=u'Title',
    ...                  __name__=u'title',
    ...                  required=False)

    >>> class Thing:
    ...    title = field.missing_value

    >>> field = field.bind(Thing())
    >>> widget = DisplayWidget(field, TestRequest())

    >>> widget()
    ''

    """


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(DocTestSuite(
        checker=checker,
        extraglobs={"DisplayWidget": DisplayWidget}))
    suite.addTest(DocTestSuite(
        checker=checker,
        extraglobs={"DisplayWidget": UnicodeDisplayWidget}))
    return suite
