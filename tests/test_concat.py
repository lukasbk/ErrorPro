import unittest
from errorpro.quantities import Quantity
from errorpro.core import *
import numpy as np

class concatTestCase(unittest.TestCase):

    def test_concat(self):
        a = Quantity("a")
        a.value = np.float_([1,2,3])
        b = Quantity("b")
        b.value = np.float_(4)
        c = concat(a,b, name='c')

        self.assertTrue((c.value == np.float_([1,2,3,4])).all())

if __name__ == '__main__':
    unittest.main()
