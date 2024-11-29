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
"""Test the choice collections widgets (function).
"""
import unittest

from zope.component import provideAdapter
from zope.component.testing import PlacelessSetup
from zope.publisher.browser import TestRequest
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema import Choice
from zope.schema import List
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import IIterableVocabulary
from zope.schema.interfaces import IList

from zope.formlib.interfaces import IDisplayWidget
from zope.formlib.interfaces import IInputWidget
from zope.formlib.widgets import ChoiceCollectionDisplayWidget
from zope.formlib.widgets import ChoiceCollectionInputWidget
from zope.formlib.widgets import CollectionDisplayWidget
from zope.formlib.widgets import CollectionInputWidget
from zope.formlib.widgets import ItemsMultiDisplayWidget
from zope.formlib.widgets import SelectWidget


class ListOfChoicesWidgetTest(PlacelessSetup, unittest.TestCase):

    def test_ListOfChoicesDisplayWidget(self):
        provideAdapter(ChoiceCollectionDisplayWidget,
                       (IList, IChoice, IBrowserRequest),
                       IDisplayWidget)
        provideAdapter(ItemsMultiDisplayWidget,
                       (IList, IIterableVocabulary, IBrowserRequest),
                       IDisplayWidget)
        field = List(value_type=Choice(values=[1, 2, 3]))
        bound = field.bind(object())
        widget = CollectionDisplayWidget(bound, TestRequest())
        self.assertIsInstance(widget, ItemsMultiDisplayWidget)
        self.assertEqual(widget.context, bound)
        self.assertEqual(widget.vocabulary, bound.value_type.vocabulary)

    def test_ChoiceSequenceEditWidget(self):
        provideAdapter(ChoiceCollectionInputWidget,
                       (IList, IChoice, IBrowserRequest),
                       IInputWidget)
        provideAdapter(SelectWidget,
                       (IList, IIterableVocabulary, IBrowserRequest),
                       IInputWidget)
        field = List(value_type=Choice(values=[1, 2, 3]))
        bound = field.bind(object())
        widget = CollectionInputWidget(bound, TestRequest())
        self.assertIsInstance(widget, SelectWidget)
        self.assertEqual(widget.context, bound)
        self.assertEqual(widget.vocabulary, bound.value_type.vocabulary)
