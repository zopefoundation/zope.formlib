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
"""Browser widgets for items
"""
__docformat__ = 'restructuredtext'

from zope.schema.vocabulary import SimpleVocabulary

from zope.formlib.i18n import _
from zope.formlib.itemswidgets import DropdownWidget
from zope.formlib.itemswidgets import RadioWidget
from zope.formlib.itemswidgets import SelectWidget
from zope.formlib.widget import DisplayWidget
from zope.formlib.widget import SimpleInputWidget
from zope.formlib.widget import renderElement


class CheckBoxWidget(SimpleInputWidget):
    """A checkbox widget used to display Bool fields.

    For more detailed documentation, including sample code, see
    ``tests/test_checkboxwidget.py``.
    """
    type = 'checkbox'
    default = 0
    extra = ''

    def __init__(self, context, request):
        super().__init__(context, request)
        self.required = False

    def __call__(self):
        """Render the widget to HTML."""
        value = self._getFormValue()
        if value == 'on':
            kw = {'checked': 'checked'}
        else:
            kw = {}
        return "{} {}".format(
            renderElement(self.tag,
                          type='hidden',
                          name=self.name + ".used",
                          id=self.name + ".used",
                          value=""
                          ),
            renderElement(self.tag,
                          type=self.type,
                          name=self.name,
                          id=self.name,
                          cssClass=self.cssClass,
                          extra=self.extra,
                          value="on",
                          **kw),
        )

    def _toFieldValue(self, input):
        """Convert from HTML presentation to Python bool."""
        return input == 'on'

    def _toFormValue(self, value):
        """Convert from Python bool to HTML representation."""
        return value and 'on' or ''

    def hasInput(self):
        """Check whether the field is represented in the form."""
        return self.name + ".used" in self.request.form or \
            super().hasInput()

    def _getFormInput(self):
        """Returns the form input used by `_toFieldValue`.

        Return values:

          ``'on'``  checkbox is checked
          ``''``    checkbox is not checked
          ``None``  form input was not provided

        """
        if self.request.get(self.name) == 'on':
            return 'on'
        elif self.name + '.used' in self.request:
            return ''
        else:
            return None


def BooleanRadioWidget(field, request, true=_('on'), false=_('off')):
    vocabulary = SimpleVocabulary.fromItems(((true, True), (false, False)))
    widget = RadioWidget(field, vocabulary, request)
    widget.required = False
    return widget


def BooleanSelectWidget(field, request, true=_('on'), false=_('off')):
    vocabulary = SimpleVocabulary.fromItems(((true, True), (false, False)))
    widget = SelectWidget(field, vocabulary, request)
    widget.size = 2
    widget.required = False
    return widget


def BooleanDropdownWidget(field, request, true=_('on'), false=_('off')):
    vocabulary = SimpleVocabulary.fromItems(((true, True), (false, False)))
    widget = DropdownWidget(field, vocabulary, request)
    widget.required = False
    return widget


class BooleanDisplayWidget(DisplayWidget):

    _msg_true = _("True")
    _msg_false = _("False")

    def __call__(self):
        if self._renderedValueSet():
            value = self._data
        else:
            value = self.context.default
        if value:
            return self._msg_true
        else:
            return self._msg_false
