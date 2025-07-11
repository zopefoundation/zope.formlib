=========
 Changes
=========

6.2 (unreleased)
================

- Drop support for Python 3.8.


6.1 (2024-11-29)
================

- Extract widgets to own ZCML file to ease overriding them all.

- Add support for Python 3.12, 3.13.

- Drop support for Python 3.7.

6.0 (2023-03-27)
================

- Add support for Python 3.11.

- Drop support for Python 2.7, 3.5, 3.6.


5.0.1 (2021-10-25)
==================

- Add support for Python 3.10.


5.0.0 (2021-10-25)
==================

Possibly breaking changes
-------------------------

- Fix checking of constraints on field contents. The ``prefix`` of an
  ``IFormField`` can still be empty and now officially allows dots.
  See `pull request 35
  <https://github.com/zopefoundation/zope.formlib/pull/35>`_.

Features
--------

- Add support for Python 3.9.

Other changes
-------------

- Remove unused non-BBB imports.

- Adjust checkbox widget test to new default for ``required`` on boolean
  fields.


4.7.1 (2020-03-31)
==================

- Ensure all objects have consistent interface resolution orders.
  See `issue 30
  <https://github.com/zopefoundation/zope.formlib/issues/30>`_.

- Remove support for deprecated ``python setup.py test`` command.

4.7.0 (2020-02-27)
==================

- Move inline javascript function definitions containing "<", ">" or "&"
  into external files to follow the XHTML recommendation concerning
  XML/HTML compatibility
  (`#25 <https://github.com/zopefoundation/zope.formlib/issues/25>`_)

- Add support for Python 3.8.

- Drop support for Python 3.4.


4.6.0 (2019-02-12)
==================

- Add support for Python 3.7.

- Make the tests compatible with ``zope.i18n >= 4.5``.


4.5.0 (2018-09-27)
==================

- Fix IE issue in /@@user-information?user_id=TestUser for
  orderedSelectionList (GH#17)

- Move documentation to https://zopeformlib.readthedocs.io


4.4.0 (2017-08-15)
==================

- Add support for Python 3.5, and 3.6.

- Drop support for Python 2.6 and 3.3.

- Use ``UTF-8`` as default encoding when casting bytes to unicode for Python 2
  *and* 3.


4.3.0 (2014-12-24)
==================

- Add support for PyPy.  (PyPy3 is pending release of a fix for:
  https://bitbucket.org/pypy/pypy/issue/1946)

- Add support for Python 3.4.

- Add support for testing on Travis.

- Explicitly hide span in ``orderedSelectionList.pt``.  This only
  contains hidden inputs, but Internet Explorer 10 was showing them
  anyway.

- Support for CSRF protection.

- Added support for restricting the acceptable request method for the
  form submit.


4.3.0a1 (2013-02-27)
====================

- Added support for Python 3.3.


4.2.1 (2013-02-22)
==================

- Moved default values for the ``BooleanDisplayWidget`` from module to class
  definition to make them changeable in instance.


4.2.0 (2012-11-27)
==================

- LP #1017884:  Add redirect status codes (303, 307) to the set which prevent
  form rendering.

- Replaced deprecated ``zope.component.adapts`` usage with equivalent
  ``zope.component.adapter`` decorator.

- Replaced deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Dropped support for Python 2.5.

- Make separator of ``SourceSequenceDisplayWidget`` configurable.


4.1.1 (2012-03-16)
==================

- Added `ignoreContext` attribute to form classes to control whether
  `checkInvariants` takes the context of the form into account when
  checking interface invariants.

  By default `ignoreContext` is set to ``False``.  On the `AddForm` it is
  ``True`` by default because the context of this form is naturally not
  suitable as context for the interface invariant.


4.1.0 (2012-03-15)
==================

- `checkInvariants` now takes the context of the form into account when
  checking interface invariants.

- Tests are no longer compatible with Python 2.4.


4.0.6 (2011-08-20)
==================

- Fixed bug in ``orderedSelectionList.pt`` template.

4.0.5 (2010-09-16)
==================

- Fixed Action name parameter handling, since 4.0.3 all passed names were
  lowercased.

4.0.4 (2010-07-06)
==================

- Fixed tests to pass under Python 2.7.

- Fix validation of "multiple" attributes in orderedSelectionList.pt.

4.0.3 (2010-05-06)
==================

- Keep Actions from raising exceptions when passed Unicode lables [LP:528468].

- Improve display of the "nothing selected" case for optional Choice fields
  [LP:269782].

- Improve truth testing for ItemDisplayWidget [LP:159232].

- Don't blow up if TypeError raised during token conversion [LP:98491].

4.0.2 (2010-03-07)
==================

- Adapted tests for Python 2.4 (enforce sorting for short pprint output)

4.0.1 (2010-02-21)
==================

- Documentation uploaded to PyPI now contains widget documentation.
- Escape MultiCheckBoxWidget content [LP:302427].

4.0 (2010-01-08)
================

- Widget implementation and all widgets from zope.app.form have been
  moved into zope.formlib, breaking zope.formlib's dependency on
  zope.app.form (instead zope.app.form now depends on zope.formlib).

  Widgets can all be imported from ``zope.formlib.widgets``.

  Widget base classes and render functionality is in
  ``zope.formlib.widget``.

  All relevant widget interfaces are now in ``zope.formlib.interfaces``.

3.10.0 (2009-12-22)
===================

- Use named template from zope.browserpage in favor of zope.app.pagetemplate.

3.9.0 (2009-12-22)
==================

- Use ViewPageTemplateFile from zope.browserpage.

3.8.0 (2009-12-22)
==================

- Adjusted test output to new zope.schema release.

3.7.0 (2009-12-18)
==================

- Rid ourselves from zope.app test dependencies.

- Fix: Button label needs escaping

3.6.0 (2009-05-18)
==================

- Remove deprecated imports.

- Remove dependency on zope.app.container (use ``IAdding`` from
  ``zope.browser.interfaces``) instead.  Depend on
  ``zope.browser>=1.1`` (the version with ``IAdding``).

- Moved ``namedtemplate`` to ``zope.app.pagetemplate``, to cut some
  dependencies on ``zope.formlib`` when using this feature. Left BBB
  imports here.

3.5.2 (2009-02-21)
==================

- Adapt tests for Python 2.5 output.

3.5.1 (2009-01-31)
==================

- Adapt tests to upcoming zope.schema release 3.5.1.

3.5.0 (2009-01-26)
==================

New Features
------------

- Test dependencies are declared in a `test` extra now.

- Introduced ``zope.formlib.form.applyData`` which works like
  ``applyChanges`` but returns a dictionary with information about
  which attribute of which schema changed.  This information is then
  sent along with the ``IObjectModifiedEvent``.

  This fixes https://bugs.launchpad.net/zope3/+bug/98483.

Bugs Fixed
----------

- Actions that cause a redirect (301, 302) do not cause the `render` method to
  be called anymore.

- The zope.formlib.form.Action class didn't fully implement
  zope.formlib.interfaces.IAction.

- zope.formlib.form.setupWidgets and zope.formlib.form.setupEditWidgets did
  not check for write access on the adapter but on context. This fixes
  https://bugs.launchpad.net/zope3/+bug/219948


3.4.0 (2007-09-28)
==================

No further changes since 3.4.0a1.

3.4.0a1 (2007-04-22)
====================

Initial release as a separate project, corresponds to zope.formlib
from Zope 3.4.0a1
