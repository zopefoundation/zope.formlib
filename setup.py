##############################################################################
#
# Copyright (c) 2006-2009 Zope Foundation and Contributors.
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
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.formlib package
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '4.2.0dev'

setup(name='zope.formlib',
      version=version,
      url='http://pypi.python.org/pypi/zope.formlib',
      license='ZPL 2.1',
      description='Form generation and validation library for Zope',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Zope3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'License :: OSI Approved',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        ],
      long_description=(read('README.txt')
                        + '\n\n' +
                        read('src', 'zope', 'formlib', 'form.txt')
                        + '\n\n' +
                        read('src', 'zope', 'formlib', 'widgets.txt')
                        + '\n\n' +
                        read('src', 'zope', 'formlib', 'errors.txt')
                        + '\n\n' +
                        read('CHANGES.txt')
                        ),
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope',],
      extras_require=dict(
          test=['zope.configuration',
                'zope.testing',
               ]
          ),
      install_requires=['setuptools',
                        'pytz',
                        'zope.browser>=1.1',
                        'zope.browserpage>=3.11.0',
                        'zope.component',
                        'zope.event',
                        'zope.i18n',
                        'zope.i18nmessageid',
                        'zope.interface',
                        'zope.lifecycleevent',
                        'zope.publisher',
                        'zope.schema>=3.5.1',
                        'zope.security',
                        'zope.traversing',
                        "zope.datetime",
                        ],
      include_package_data = True,
      zip_safe = False,
      )
