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
"""Select Widget Tests
"""
import unittest

from zope.publisher.browser import TestRequest
from zope.schema import Choice
from zope.schema import List

from zope.formlib.widgets import SelectWidget


select_html = '''<div>
<div class="value">
<select id="field.terms" name="field.terms" size="5" >
<option value="&lt; foo">&lt; foo</option>
<option value="bar/&gt;">bar/&gt;</option>
<option value="&amp;blah&amp;">&amp;blah&amp;</option>
</select>
</div>
<input name="field.terms-empty-marker" type="hidden" value="1" />
</div>'''


class SelectWidgetHTMLEncodingTest(unittest.TestCase):

    def testOptionEncoding(self):
        choice = Choice(
            title="Number",
            description="The Number",
            values=['< foo', 'bar/>', '&blah&'])

        sequence = List(
            __name__="terms",
            title="Numbers",
            description="The Numbers",
            value_type=choice)

        request = TestRequest()
        sequence = sequence.bind(object())
        widget = SelectWidget(sequence, choice.vocabulary, request)
        self.assertEqual(widget(), select_html)
