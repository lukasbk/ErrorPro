import unittest
from errorpro.quantities import Quantity
from errorpro.dimensions.dimensions import Dimension
import numpy as np
from errorpro.core import *
from sympy import exp

class FitTestCase(unittest.TestCase):

    # TODO: test multidimensional fits!!

    def _set_up(self):
        x = Quantity("x")
        x.value = np.float_([1,2,3])
        x.dim = Dimension()

        y = Quantity("y")
        y.value = np.float_([6,3,2.1])
        y.error = np.float_([0.1,0.1,0.2])
        y.dim = Dimension()

        m = Quantity("m")
        m.value = 1
        b = Quantity("b")
        b.value = 1

        return (x, y, m, b)

    def test_weighted_fit(self):
        x, y, m , b = self._set_up()
        fit(m*x+b, x, y, [m, b])
        self.assertAlmostEqual(m.value, -2.3, places=2)
        self.assertAlmostEqual(m.error, 0.7, places=2)
        self.assertAlmostEqual(b.value, 8.06667, places=2)
        self.assertAlmostEqual(b.error, 1.257, places=2)

    def test_unweighted_fit(self):
        x, y, m , b = self._set_up()
        fit(m*x+b, x, y, [m, b], weighted=False)
        self.assertAlmostEqual(m.value , -1.95, places=2)
        self.assertAlmostEqual(m.error, 0.6062, places=2)
        self.assertAlmostEqual(b.value, 7.6, places=2)
        self.assertAlmostEqual(b.error, 1.31, places=2)

    def test_weighted_error(self):
        x, y, m , b = self._set_up()
        y.error = None
        self.assertRaises(RuntimeError, fit, m*x+b, x, y, [m, b], weighted=True)

    def test_dimension_lookup(self):
        x, y, m , b = self._set_up()
        x.dim = Dimension(time=1)
        y.dim = Dimension(current=2)
        fit(m**2*exp(x/b), x, y, [m, b])
        self.assertEqual(m.dim, Dimension(current=1))
        self.assertEqual(b.dim, Dimension(time=1))

if __name__ == '__main__':
    unittest.main()
