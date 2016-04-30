import unittest
from errorpro.core import mean
from errorpro.quantities import *
import numpy as np
from errorpro.dimensions.dimensions import Dimension

class MeanValueTestCase(unittest.TestCase):

    def test_unweighted_mean_value(self):

        a=Quantity("a")
        a.value = np.float_([3,4,5,6,7,8])
        a.dim = Dimension(time=1)

        m = mean(a, name='m', longname="Mittelwert")
        self.assertEqual(m.name, "m")
        self.assertEqual(m.longname, "Mittelwert")
        self.assertAlmostEqual(m.value, 5.5)
        self.assertAlmostEqual(m.error, 0.84876886033)
        self.assertEqual(m.dim, Dimension(time=1))

    def test_weighted_mean_value(self):
        a=Quantity("a")
        b=Quantity("b")
        a.value = np.float_([3,4])
        a.error = np.float_([0.3,0.4])
        a.dim = Dimension(length=1)
        b.value = np.float_(7)
        b.error = np.float_(2)
        b.dim = Dimension(length=1)

        n = mean(a, b, name="n", longname="Mittel")
        self.assertEqual(n.name, "n")
        self.assertEqual(n.longname, "Mittel")
        self.assertAlmostEqual(n.value, 3.41167192429)
        self.assertAlmostEqual(n.error, 0.23829044123)
        self.assertEqual(n.dim, Dimension(length=1))

if __name__ == '__main__':
    unittest.main()
