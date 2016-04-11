import unittest
from errorpro.core import assign
from errorpro.dimensions.dimensions import Dimension
from errorpro.si import system as si
from sympy import *
import numpy as np

class AssignTestCase(unittest.TestCase):

    def test_simple_assign(self):

        q = assign(12, 1/1000, "mm", "r", "Radius")

        self.assertEqual(q.name, "r")
        self.assertEqual(q.longname, "Radius")
        self.assertAlmostEqual(q.value, 0.012)
        self.assertEqual(q.prefer_unit, si["mm"])
        self.assertEqual(q.value_formula, None)
        self.assertEqual(q.dim, Dimension(length=1))
        self.assertAlmostEqual(q.error, 1e-6)
        self.assertEqual(q.error_formula, None)

    def test_no_error(self):
        q = assign(3, None, "s")

        self.assertAlmostEqual(q.value, 3)
        self.assertEqual(q.prefer_unit, si["s"])
        self.assertEqual(q.value_formula, None)
        self.assertEqual(q.dim, Dimension(time=1))
        self.assertEqual(q.error, None)
        self.assertEqual(q.error_formula, None)

    def test_different_units(self):

        q = assign(14, 23, None, "r", "Radius", "dm", "cm")

        self.assertEqual(q.name, "r")
        self.assertEqual(q.longname, "Radius")
        self.assertAlmostEqual(q.value, 1.4)
        self.assertEqual(q.prefer_unit, si["dm"])
        self.assertEqual(q.value_formula, None)
        self.assertEqual(q.dim, Dimension(length=1))
        self.assertAlmostEqual(q.error, 0.23)
        self.assertEqual(q.error_formula, None)

    def test_simple_calculation(self):

        r = assign(4,1,"m","r")

        q = assign(2*pi*r**3, None, None, "V", "Volumen")

        self.assertEqual(q.name, "V")
        self.assertEqual(q.longname, "Volumen")
        self.assertAlmostEqual(q.value, 2*np.pi*4**3)
        self.assertEqual(q.prefer_unit, None)
        self.assertEqual(q.value_formula, 2*pi*r**3)
        self.assertEqual(q.dim, Dimension(length=3))
        self.assertAlmostEqual(q.error, 2*np.pi*3*4**2*1)

    def test_calculataion_two_variables(self):

        r = assign(4,1,"m","r")
        h = assign(3,2,"m","h")

        q = assign(2*pi*r**2*h, None, None, "V", "Volumen")

        self.assertEqual(q.name, "V")
        self.assertEqual(q.longname, "Volumen")
        self.assertAlmostEqual(q.value, 2*np.pi*4**2*3)
        self.assertEqual(q.prefer_unit, None)
        self.assertEqual(q.value_formula, 2*pi*r**2*h)
        self.assertEqual(q.dim, Dimension(length=3))
        self.assertAlmostEqual(q.error, 2*np.pi*np.sqrt((2*4*3*1)**2+(4**2*2)**2))

    def test_dimension_mismatch(self):

        self.assertRaises(RuntimeError, assign, 2, 1, value_unit="m", error_unit="m*s")

    def test_dimension_mismatch_to_calculated_dimension(self):

        a = assign(3,1,"m")
        self.assertRaises(RuntimeError, assign, a**2, None, unit="s")

    def test_duplicating_error(self):

        q = assign([4,5,6], 0.5)

        self.assertEqual(len(q.error), 3)
        self.assertTrue(np.allclose(q.error,[0.5,0.5,0.5]))

    def test_multi_dimensional_error_duplication(self):
        q = assign([[[1,2],[3,4]],[[5,6],[7,8]]], [5,4])
        self.assertTrue(np.allclose(q.error, [[[5,4],[5,4]],[[5,4],[5,4]]]))

    def test_ignore_dim(self):

        a = assign(3,1,"m")
        q = assign(a**2, None, "s", ignore_dim=True)

        self.assertEqual(q.prefer_unit, si["s"])
        self.assertEqual(q.dim, Dimension(time=1))

    def test_ignore_dim_factor(self):
        a = assign(3,1,None,"m")
        q = assign(a**2, None, "ms", ignore_dim=True)
        self.assertAlmostEqual(q.value, 0.009)
        self.assertAlmostEqual(q.error, 0.006)

if __name__ == '__main__':
    unittest.main()
