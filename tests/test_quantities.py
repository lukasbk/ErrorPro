import unittest
from errorpro.quantities import *
from errorpro.dimensions.dimensions import Dimension
from errorpro.si import system as si
import numpy as np
import sympy as sp

class QuantitiesTestCase(unittest.TestCase):

    def test_parse_expr(self):
        q1 = Quantity("q1")
        q2 = Quantity("q2")
        data = {"q1":q1, "q2":q2}
        term = parse_expr("q1+q2**2", data)
        self.assertEqual(term, q1+q2**2)

    def test_get_dimension(self):
        q1 = Quantity("q1")
        q2 = Quantity("q2")
        q1.dim = Dimension(length=1)
        q2.dim = Dimension(time=1)
        self.assertEqual( get_dimension(q1*q2**2), Dimension(length=1, time=2) )

    def test_adjust_to_unit_default(self):
        q1 = Quantity()
        q1.value = np.float_(0.3)
        q1.error = np.float_(0.1)
        q1.dim = Dimension(length=1,time=-1)
        out = adjust_to_unit(q1)
        self.assertAlmostEqual(out[0], np.float_(0.3))
        self.assertAlmostEqual(out[1], np.float_(0.1))
        self.assertEqual(out[2], si['m']/si['s'])

    def test_adjust_to_unit_specified(self):
        q1 = Quantity()
        q1.value = np.float_(0.3)
        q1.error = np.float_(0.1)
        q1.dim = Dimension(length=1,time=-1)
        out = adjust_to_unit(q1, si['mm']/si['s'])
        self.assertAlmostEqual(out[0], np.float_(300))
        self.assertAlmostEqual(out[1], np.float_(100))
        self.assertEqual(out[2], si['mm']/si['s'])

    def test_get_value(self):
        q1 = Quantity()
        q1.value = np.float_(0.3)
        q2 = Quantity()
        q2.value = np.float_(0.5)
        self.assertAlmostEqual(get_value(q1+q2), 0.8)

    def test_get_error(self):
            q1 = Quantity()
            q1.name = 'q1'
            q1.value = np.float_(0.3)
            q1.error = np.float_(0.1)
            q2 = Quantity()
            q2.name = 'q2'
            q2.value = np.float_(0.5)
            q2.error = np.float_(0.1)
            out = get_error(q1*q2)
            self.assertAlmostEqual(out[0], np.sqrt(0.3**2*0.1**2+0.5**2*0.1**2))
            self.assertEqual(out[1], sp.sqrt(q1**2*sp.Symbol('q2_err', positive=True)**2 + q2**2*sp.Symbol('q1_err', positive=True)**2))

if __name__ == '__main__':
    unittest.main()
