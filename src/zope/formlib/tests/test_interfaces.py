from .. interfaces import reConstraint
import unittest
import zope.interface


class TestReConstraint(unittest.TestCase):
    """Testing ..interfaces.reConstraint()."""

    def test__interfaces__reConstraint__1(self):
        """It returns a function returning True if the pattern is matched."""
        func = reConstraint('^[A-Z]+$', 'only capital letters allowed')
        self.assertTrue(func('ABC'))

    def test__interfaces__reConstraint__2(self):
        """It returns a function raising Invalid if pattern is not matched."""
        func = reConstraint('^[A-Z]+$', 'only capital letters allowed')
        with self.assertRaises(zope.interface.Invalid) as err:
            func('ABc')
        self.assertEqual(
            "('ABc', 'only capital letters allowed')", str(err.exception))

    def test__interfaces__reConstraint__3(self):
        """It returns a function raising Invalid for empty values."""
        func = reConstraint('^[A-Z]+$', 'only capital letters allowed')
        with self.assertRaises(zope.interface.Invalid) as err:
            func('')
        self.assertEqual(
            "('', 'only capital letters allowed')", str(err.exception))

    def test__interfaces__reConstraint__4(self):
        """It returns a function allowing empty values if configured."""
        func = reConstraint(
            '^[A-Z]+$', 'only capital letters or empty', can_be_empty=True)
        self.assertTrue(func(''))
