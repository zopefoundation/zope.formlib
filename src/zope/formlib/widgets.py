##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
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
"""Browser widgets
"""
# Widgets for boolean fields
from zope.formlib.boolwidgets import BooleanDisplayWidget
from zope.formlib.boolwidgets import BooleanDropdownWidget
from zope.formlib.boolwidgets import BooleanRadioWidget
from zope.formlib.boolwidgets import BooleanSelectWidget
from zope.formlib.boolwidgets import CheckBoxWidget
# Widgets that let you choose several items from a list
# These widgets are multi-views on (field, vocabulary)
# Widgets that let you choose a single item from a list
# These widgets are multi-views on (field, vocabulary)
# Widgets for fields with vocabularies.
# Note that these are only dispatchers for the widgets below.
# Choice and Sequence Display Widgets
from zope.formlib.itemswidgets import ChoiceCollectionDisplayWidget
from zope.formlib.itemswidgets import ChoiceCollectionInputWidget
from zope.formlib.itemswidgets import ChoiceDisplayWidget
from zope.formlib.itemswidgets import ChoiceInputWidget
from zope.formlib.itemswidgets import CollectionDisplayWidget
from zope.formlib.itemswidgets import CollectionInputWidget
from zope.formlib.itemswidgets import DropdownWidget
from zope.formlib.itemswidgets import ItemDisplayWidget
from zope.formlib.itemswidgets import ItemsMultiDisplayWidget
from zope.formlib.itemswidgets import ListDisplayWidget
from zope.formlib.itemswidgets import MultiCheckBoxWidget
from zope.formlib.itemswidgets import MultiSelectFrozenSetWidget
from zope.formlib.itemswidgets import MultiSelectSetWidget
from zope.formlib.itemswidgets import MultiSelectWidget
from zope.formlib.itemswidgets import OrderedMultiSelectWidget
from zope.formlib.itemswidgets import RadioWidget
from zope.formlib.itemswidgets import SelectWidget
from zope.formlib.itemswidgets import SetDisplayWidget
from zope.formlib.objectwidget import ObjectWidget
# Widgets that let you enter several items in a sequence
# These widgets are multi-views on (sequence type, value type)
from zope.formlib.sequencewidget import ListSequenceWidget
from zope.formlib.sequencewidget import SequenceDisplayWidget
from zope.formlib.sequencewidget import SequenceWidget
from zope.formlib.sequencewidget import TupleSequenceWidget
from zope.formlib.textwidgets import ASCIIAreaWidget
from zope.formlib.textwidgets import ASCIIDisplayWidget
from zope.formlib.textwidgets import ASCIIWidget
from zope.formlib.textwidgets import BytesAreaWidget
from zope.formlib.textwidgets import BytesDisplayWidget
from zope.formlib.textwidgets import BytesWidget
from zope.formlib.textwidgets import DateDisplayWidget
from zope.formlib.textwidgets import DateI18nWidget
from zope.formlib.textwidgets import DatetimeDisplayWidget
from zope.formlib.textwidgets import DatetimeI18nWidget
from zope.formlib.textwidgets import DatetimeWidget
from zope.formlib.textwidgets import DateWidget
from zope.formlib.textwidgets import DecimalWidget
from zope.formlib.textwidgets import FileWidget
from zope.formlib.textwidgets import FloatWidget
from zope.formlib.textwidgets import IntWidget
from zope.formlib.textwidgets import PasswordWidget
from zope.formlib.textwidgets import TextAreaWidget
from zope.formlib.textwidgets import TextWidget
from zope.formlib.textwidgets import URIDisplayWidget
from zope.formlib.widget import BrowserWidget
from zope.formlib.widget import DisplayWidget
from zope.formlib.widget import UnicodeDisplayWidget
