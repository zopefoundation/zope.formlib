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
"""Browser widgets with text-based input
"""
import decimal
from xml.sax import saxutils

from zope.datetime import DateTimeError
from zope.datetime import parseDatetimetz
from zope.i18n.format import DateTimeParseError
from zope.interface import implementer

from zope.formlib._compat import toStr
from zope.formlib.i18n import _
from zope.formlib.interfaces import ConversionError
from zope.formlib.interfaces import ITextBrowserWidget
from zope.formlib.widget import DisplayWidget
from zope.formlib.widget import SimpleInputWidget
from zope.formlib.widget import renderElement


def escape(str):
    if str is not None:
        str = saxutils.escape(str)
    return str


@implementer(ITextBrowserWidget)
class TextWidget(SimpleInputWidget):
    """Text widget.

    Single-line text input

    >>> from zope.publisher.browser import TestRequest
    >>> from zope.schema import TextLine
    >>> field = TextLine(__name__='foo', title='on')
    >>> request = TestRequest(form={'field.foo': 'Bob'})
    >>> widget = TextWidget(field, request)
    >>> widget.hasInput()
    True
    >>> widget.getInputValue()
    'Bob'

    >>> def normalize(s):
    ...   return '\\n  '.join(filter(None, s.split(' ')))

    >>> print(normalize( widget() ))
    <input
      class="textType"
      id="field.foo"
      name="field.foo"
      size="20"
      type="text"
      value="Bob"
      />

    >>> print(normalize( widget.hidden() ))
    <input
      class="hiddenType"
      id="field.foo"
      name="field.foo"
      type="hidden"
      value="Bob"
      />

    Calling `setRenderedValue` will change what gets output:

    >>> widget.setRenderedValue("Barry")
    >>> print(normalize( widget() ))
    <input
      class="textType"
      id="field.foo"
      name="field.foo"
      size="20"
      type="text"
      value="Barry"
      />

    Check that HTML is correctly encoded and decoded:

    >>> request = TestRequest(
    ...     form={'field.foo': '<h1>&copy;</h1>'})
    >>> widget = TextWidget(field, request)
    >>> widget.getInputValue()
    '<h1>&copy;</h1>'

    >>> print(normalize( widget() ))
    <input
      class="textType"
      id="field.foo"
      name="field.foo"
      size="20"
      type="text"
      value="&lt;h1&gt;&amp;copy;&lt;/h1&gt;"
      />
    """

    default = ''
    displayWidth = 20
    displayMaxWidth = ""
    extra = ''
    style = ''
    convert_missing_value = True

    def __init__(self, *args):
        super().__init__(*args)

    def __call__(self):
        value = self._getFormValue()
        if value is None or value == self.context.missing_value:
            value = ''

        kwargs = {'type': self.type,
                  'name': self.name,
                  'id': self.name,
                  'value': value,
                  'cssClass': self.cssClass,
                  'style': self.style,
                  'size': self.displayWidth,
                  'extra': self.extra}
        if self.displayMaxWidth:
            # TODO This is untested.
            kwargs['maxlength'] = self.displayMaxWidth

        return renderElement(self.tag, **kwargs)

    def _toFieldValue(self, input):
        if self.convert_missing_value and input == self._missing:
            value = self.context.missing_value
        else:
            # We convert everything to str. This might seem a bit crude,
            # but anything contained in a TextWidget should be representable
            # as a string. Note that you always have the choice of overriding
            # the method.
            try:
                value = toStr(input)
            except ValueError as v:
                raise ConversionError(_("Invalid text data"), v)
        return value


class Text(SimpleInputWidget):

    def _toFieldValue(self, input):
        return super()._toFieldValue(input)


class Bytes(SimpleInputWidget):

    def _toFieldValue(self, input):
        value = super()._toFieldValue(input)
        if isinstance(value, str):
            try:
                value = value.encode('ascii')
            except UnicodeError as v:
                raise ConversionError(_("Invalid textual data"), v)
        return value


class BytesWidget(Bytes, TextWidget):
    """Bytes widget.

    Single-line data (string) input

    >>> from zope.publisher.browser import TestRequest
    >>> from zope.schema import BytesLine
    >>> field = BytesLine(__name__='foo', title='on')
    >>> request = TestRequest(form={'field.foo': 'Bob'})
    >>> widget = BytesWidget(field, request)
    >>> widget.hasInput()
    True
    >>> widget.getInputValue()
    b'Bob'
    """


class BytesDisplayWidget(DisplayWidget):
    """Bytes display widget"""

    def __call__(self):
        if self._renderedValueSet():
            content = self._data
        else:
            content = self.context.default
        return renderElement("pre", contents=escape(content))


class ASCII(Text):
    """ASCII"""


class ASCIIWidget(TextWidget):
    """ASCII widget.

    Single-line data (string) input
    """


class ASCIIDisplayWidget(DisplayWidget):
    """ASCII display widget"""


class URIDisplayWidget(DisplayWidget):
    """URI display widget.

    :ivar linkTarget:
      The value of the ``target`` attribute for the generated hyperlink.
      If this is not set, no ``target`` attribute is generated.

    """

    linkTarget = None

    def __call__(self):
        if self._renderedValueSet():
            content = self._data
        else:
            content = self.context.default
        if not content:
            # If there is no content it is not useful to render an anchor.
            return ''
        content = escape(content)
        kw = dict(contents=content, href=content)
        if self.linkTarget:
            kw["target"] = self.linkTarget
        return renderElement("a", **kw)


class TextAreaWidget(SimpleInputWidget):
    """TextArea widget.

    Multi-line text input.

    >>> from zope.publisher.browser import TestRequest
    >>> from zope.schema import Text
    >>> field = Text(__name__='foo', title='on')
    >>> request = TestRequest(form={'field.foo': 'Hello\\r\\nworld!'})
    >>> widget = TextAreaWidget(field, request)
    >>> widget.hasInput()
    True
    >>> widget.getInputValue()
    'Hello\\nworld!'

    >>> def normalize(s):
    ...   return '\\n  '.join(filter(None, s.split(' ')))

    >>> print(normalize( widget() ))
    <textarea
      cols="60"
      id="field.foo"
      name="field.foo"
      rows="15"
      >Hello\r
    world!</textarea>

    >>> print(normalize( widget.hidden() ))
    <input
      class="hiddenType"
      id="field.foo"
      name="field.foo"
      type="hidden"
      value="Hello&#13;&#10;world!"
      />

    Calling `setRenderedValue` will change what gets output:

    >>> widget.setRenderedValue("Hey\\ndude!")
    >>> print(normalize( widget() ))
    <textarea
      cols="60"
      id="field.foo"
      name="field.foo"
      rows="15"
      >Hey\r
    dude!</textarea>

    Check that HTML is correctly encoded and decoded:

    >>> request = TestRequest(
    ...     form={'field.foo': '<h1>&copy;</h1>'})
    >>> widget = TextAreaWidget(field, request)
    >>> widget.getInputValue()
    '<h1>&copy;</h1>'

    >>> print(normalize( widget() ))
    <textarea
      cols="60"
      id="field.foo"
      name="field.foo"
      rows="15"
      >&lt;h1&gt;&amp;copy;&lt;/h1&gt;</textarea>

    There was a but which caused the content of <textarea> tags not to be
    rendered correctly when there was a conversion error. Make sure the quoting
    works correctly::

    >>> from zope.schema import Text
    >>> field = Text(__name__='description', title='Description')

    >>> from zope.formlib.interfaces import ConversionError
    >>> class TestTextAreaWidget(TextAreaWidget):
    ...     def _toFieldValue(self, input):
    ...         if 'foo' in input:
    ...             raise ConversionError("I don't like foo.")
    ...         return input
    ...

    >>> request = TestRequest(form={'field.description': '<p>bar</p>'})
    >>> widget = TestTextAreaWidget(field, request)
    >>> widget.getInputValue()
    '<p>bar</p>'
    >>> print(normalize( widget() ))
    <textarea
      cols="60"
      id="field.description"
      name="field.description"
      rows="15"
      >&lt;p&gt;bar&lt;/p&gt;</textarea>

    >>> request = TestRequest(form={'field.description': '<p>foo</p>'})
    >>> widget = TestTextAreaWidget(field, request)
    >>> try:
    ...     widget.getInputValue()
    ... except ConversionError as error:
    ...     print(error.doc())
    I don't like foo.
    >>> print(normalize( widget() ))
    <textarea
      cols="60"
      id="field.description"
      name="field.description"
      rows="15"
      >&lt;p&gt;foo&lt;/p&gt;</textarea>
    """

    default = ""
    width = 60
    height = 15
    extra = ""
    style = ''

    def _toFieldValue(self, value):
        value = super()._toFieldValue(value)
        if value:
            try:
                value = toStr(value)
            except ValueError as v:
                raise ConversionError(_("Invalid test data"), v)
            else:
                value = value.replace("\r\n", "\n")
        return value

    def _toFormValue(self, value):
        value = super()._toFormValue(value)
        if value:
            value = value.replace("\n", "\r\n")
        else:
            value = ''

        return value

    def __call__(self):
        return renderElement("textarea",
                             name=self.name,
                             id=self.name,
                             cssClass=self.cssClass,
                             rows=self.height,
                             cols=self.width,
                             style=self.style,
                             contents=escape(self._getFormValue()),
                             extra=self.extra)


class BytesAreaWidget(Bytes, TextAreaWidget):
    """BytesArea widget.

    Multi-line string input.

    >>> from zope.publisher.browser import TestRequest
    >>> from zope.schema import Bytes
    >>> field = Bytes(__name__='foo', title='on')
    >>> request = TestRequest(form={'field.foo': 'Hello\\r\\nworld!'})
    >>> widget = BytesAreaWidget(field, request)
    >>> widget.hasInput()
    True
    >>> widget.getInputValue()
    b'Hello\\nworld!'
    """


class ASCIIAreaWidget(Text, TextAreaWidget):
    """ASCIIArea widget.

    Multi-line string input.

    >>> from zope.publisher.browser import TestRequest
    >>> from zope.schema import ASCII
    >>> field = ASCII(__name__='foo', title='on')
    >>> request = TestRequest(form={'field.foo': 'Hello\\r\\nworld!'})
    >>> widget = ASCIIAreaWidget(field, request)
    >>> widget.hasInput()
    True
    >>> widget.getInputValue()
    'Hello\\nworld!'
    """


class PasswordWidget(TextWidget):
    """Password Widget"""

    type = 'password'

    def __call__(self):
        displayMaxWidth = self.displayMaxWidth or 0
        if displayMaxWidth > 0:
            return renderElement(self.tag,
                                 type=self.type,
                                 name=self.name,
                                 id=self.name,
                                 value='',
                                 cssClass=self.cssClass,
                                 style=self.style,
                                 size=self.displayWidth,
                                 maxlength=displayMaxWidth,
                                 extra=self.extra)
        else:
            return renderElement(self.tag,
                                 type=self.type,
                                 name=self.name,
                                 id=self.name,
                                 value='',
                                 cssClass=self.cssClass,
                                 style=self.style,
                                 size=self.displayWidth,
                                 extra=self.extra)

    def _toFieldValue(self, input):
        try:
            existing = self.context.get(self.context.context)
        except AttributeError:
            existing = False
        if (not input) and existing:
            return self.context.UNCHANGED_PASSWORD
        return super()._toFieldValue(input)

    def hidden(self):
        raise NotImplementedError(
            'Cannot get a hidden tag for a password field')


class FileWidget(TextWidget):
    """File Widget"""

    type = 'file'

    def __call__(self):
        displayMaxWidth = self.displayMaxWidth or 0
        hidden = renderElement(self.tag,
                               type='hidden',
                               name=self.name + ".used",
                               id=self.name + ".used",
                               value="")
        if displayMaxWidth > 0:
            elem = renderElement(self.tag,
                                 type=self.type,
                                 name=self.name,
                                 id=self.name,
                                 cssClass=self.cssClass,
                                 size=self.displayWidth,
                                 maxlength=displayMaxWidth,
                                 extra=self.extra)
        else:
            elem = renderElement(self.tag,
                                 type=self.type,
                                 name=self.name,
                                 id=self.name,
                                 cssClass=self.cssClass,
                                 size=self.displayWidth,
                                 extra=self.extra)
        return f"{hidden} {elem}"

    def _toFieldValue(self, input):
        if input is None or input == '':
            return self.context.missing_value
        try:
            seek = input.seek
            read = input.read
        except AttributeError as e:
            raise ConversionError(_('Form input is not a file object'), e)
        else:
            seek(0)
            data = read()
            if data or getattr(input, 'filename', ''):
                return data
            else:
                return self.context.missing_value

    def hasInput(self):
        return ((self.name + ".used" in self.request.form)
                or
                (self.name in self.request.form)
                )


class IntWidget(TextWidget):
    """Integer number widget.

    Let's make sure that zeroes are rendered properly:

    >>> from zope.schema import Int
    >>> field = Int(__name__='foo', title='on')
    >>> widget = IntWidget(field, None)
    >>> widget.setRenderedValue(0)

    >>> 'value="0"' in widget()
    True

    """

    displayWidth = 10

    def _toFieldValue(self, input):
        if input == self._missing:
            return self.context.missing_value
        else:
            try:
                return int(input)
            except ValueError as v:
                raise ConversionError(_("Invalid integer data"), v)


class FloatWidget(TextWidget):
    displayWidth = 10

    def _toFieldValue(self, input):
        if input == self._missing:
            return self.context.missing_value
        else:
            try:
                return float(input)
            except ValueError as v:
                raise ConversionError(_("Invalid floating point data"), v)


class DecimalWidget(TextWidget):
    displayWidth = 10

    def _toFieldValue(self, input):
        if input == self._missing:
            return self.context.missing_value
        else:
            try:
                return decimal.Decimal(input)
            except decimal.InvalidOperation as v:
                raise ConversionError(_("Invalid decimal data"), v)

    def _toFormValue(self, value):
        if value == self.context.missing_value:
            value = self._missing
        else:
            return toStr(value)


class DatetimeWidget(TextWidget):
    """Datetime entry widget."""

    displayWidth = 20

    def _toFieldValue(self, input):
        if input == self._missing:
            return self.context.missing_value
        else:
            try:
                # TODO: Currently datetimes return in local (server)
                # time zone if no time zone information was given.
                # Maybe offset-naive datetimes should be returned in
                # this case? (DV)
                return parseDatetimetz(input)
            except (DateTimeError, ValueError, IndexError) as v:
                raise ConversionError(_("Invalid datetime data"), v)


class DateWidget(DatetimeWidget):
    """Date entry widget.
    """

    def _toFieldValue(self, input):
        v = super()._toFieldValue(input)
        if v != self.context.missing_value:
            v = v.date()
        return v


class DateI18nWidget(TextWidget):
    """I18n date entry widget.

    The `displayStyle` attribute may be set to control the formatting of the
    value.

    `displayStyle` must be one of 'full', 'long', 'medium', 'short',
    or None ('' is accepted an an alternative to None to support
    provision of a value from ZCML).
    """

    _category = "date"

    displayWidth = 20

    displayStyle = None

    def _toFieldValue(self, input):
        if input == self._missing:
            return self.context.missing_value
        else:
            try:
                formatter = self.request.locale.dates.getFormatter(
                    self._category, (self.displayStyle or None))
                return formatter.parse(input)
            except (DateTimeParseError, ValueError) as v:
                raise ConversionError(_("Invalid datetime data"),
                                      f"{v} ({input!r})")

    def _toFormValue(self, value):
        value = super()._toFormValue(value)
        if value:
            formatter = self.request.locale.dates.getFormatter(
                self._category, (self.displayStyle or None))
            value = formatter.format(value)
        return value


class DatetimeI18nWidget(DateI18nWidget):
    """I18n datetime entry widget.

    The `displayStyle` attribute may be set to control the formatting of the
    value.

    `displayStyle` must be one of 'full', 'long', 'medium', 'short',
    or None ('' is accepted an an alternative to None to support
    provision of a value from ZCML).

    NOTE: If you need timezone information you need to set `displayStyle`
    to either 'long' or 'full' since other display styles just ignore it.
    """

    _category = "dateTime"


class DateDisplayWidget(DisplayWidget):
    """Date display widget.

    The `cssClass` and `displayStyle` attributes may be set to control
    the formatting of the value.

    `displayStyle` must be one of 'full', 'long', 'medium', 'short',
    or None ('' is accepted an an alternative to None to support
    provision of a value from ZCML).
    """

    cssClass = "date"
    displayStyle = None

    _category = "date"

    def __call__(self):
        if self._renderedValueSet():
            content = self._data
        else:
            content = self.context.default
        if content == self.context.missing_value:
            return ""
        formatter = self.request.locale.dates.getFormatter(
            self._category, (self.displayStyle or None))
        content = formatter.format(content)
        return renderElement("span", contents=escape(content),
                             cssClass=self.cssClass)


class DatetimeDisplayWidget(DateDisplayWidget):
    """Datetime display widget.

    The `cssClass` and `displayStyle` attributes may be set to control
    the formatting of the value.

    `displayStyle` must be one of 'full', 'long', 'medium', 'short',
    or None ('' is accepted an an alternative to None to support
    provision of a value from ZCML).
    """

    cssClass = "dateTime"

    _category = "dateTime"
