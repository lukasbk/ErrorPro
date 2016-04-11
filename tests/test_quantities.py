import unittest
from errorpro.quantities import *
from errorpro.dimensions.dimensions import Dimension
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

    # TODO: more tests...

if __name__ == '__main__':
    unittest.main()
