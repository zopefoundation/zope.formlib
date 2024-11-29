##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
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
"""General test support.
"""
import re


class VerifyResults:
    """Mix-in for test classes with helpers for checking string data."""

    def verifyResult(self, result, check_list, inorder=False):
        start = 0
        for check in check_list:
            pos = result.find(check, start)
            self.assertGreaterEqual(
                pos,
                0,
                "{!r} not found in {!r}".format(
                    check, result[start:])
            )
            if inorder:
                start = pos + len(check)


def patternExists(pattern, source, flags=0):
    return re.search(pattern, source, flags) is not None
