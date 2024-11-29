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
"""Test the Choice display and edit widget (function).
"""
import unittest

from zope.component import provideAdapter
from zope.component.testing import PlacelessSetup
from zope.publisher.browser import TestRequest
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema import Choice
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import IIterableVocabulary

from zope.formlib.interfaces import IDisplayWidget
from zope.formlib.interfaces import IInputWidget
from zope.formlib.widgets import ChoiceDisplayWidget
from zope.formlib.widgets import ChoiceInputWidget
from zope.formlib.widgets import DropdownWidget
from zope.formlib.widgets import ItemDisplayWidget


class ChoiceWidgetTest(PlacelessSetup, unittest.TestCase):

    def test_ChoiceDisplayWidget(self):
        provideAdapter(ItemDisplayWidget,
                       (IChoice, IIterableVocabulary, IBrowserRequest),
                       IDisplayWidget)
        field = Choice(values=[1, 2, 3])
        bound = field.bind(object())
        widget = ChoiceDisplayWidget(bound, TestRequest())
        self.assertIsInstance(widget, ItemDisplayWidget)
        self.assertEqual(widget.context, bound)
        self.assertEqual(widget.vocabulary, bound.vocabulary)

    def test_ChoiceInputWidget(self):
        provideAdapter(DropdownWidget,
                       (IChoice, IIterableVocabulary, IBrowserRequest),
                       IInputWidget)
        field = Choice(values=[1, 2, 3])
        bound = field.bind(object())
        widget = ChoiceInputWidget(bound, TestRequest())
        self.assertIsInstance(widget, DropdownWidget)
        self.assertEqual(widget.context, bound)
        self.assertEqual(widget.vocabulary, bound.vocabulary)


def test_suite():
    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromTestCase(ChoiceWidgetTest),
    ))
