##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
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
"""Setup for zope.formlib package

$Id$
"""

import os

from setuptools import setup, find_packages

setup(name='zope.formlib',
      version='3.4dev',
      url='http://svn.zope.org/zope.formlib',
      license='ZPL 2.1',
      description='Zope formlib',
      author='Zope Corporation and Contributors',
      author_email='zope3-dev@zope.org',
      long_description="Forms are web components that use widgets"
                       "to display and input data.  Typically a template"
                       "displays the widgets by accessing an attribute or"
                       "method on an underlying class.",

      packages=find_packages('src'),
      package_dir = {'': 'src'},

      namespace_packages=['zope',],
      tests_require = ['zope.testing'],
      install_requires=['setuptools',
                        'zope.interface',
                        'zope.schema',
                        'zope.component',
                        'zope.publisher',
                        'zope.event',
                        'zope.i18n',
                        'zope.security',
                        'zope.app',
                        'zope.i18nmessageid',],
      include_package_data = True,
      zip_safe = False,
      extras_require = dict(
        )
      )
