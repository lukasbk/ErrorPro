import unittest
import scipy_fit as sc
from quantities import Quantity
import numpy as np

class UnitsTestCase(unittest.TestCase):

    def test_scipy_fit(self):
        a = Quantity("a")
        a.value = np.float_([1,3,5,6,7,9])
        b = Quantity("b")
        b.value = np.float_([2.3,4,5.5,6,9.2,10.5])
        c = Quantity("c")
        c.value = np.float_(1)
        d = Quantity("d")
        d.value = np.float_(1)
        f = a*c+d

        popt,perr = (sc.fit(a,b,f,[c,d]))

        small = 0.0001
        self.assertTrue(abs(popt[0] - 1.05184) < small)
        self.assertTrue(abs(perr[0] - 0.1328) < small)
        self.assertTrue(abs(popt[1] - 0.81551) < small)
        self.assertTrue(abs(perr[1] - 0.7684) < small)


if __name__ == '__main__':
    unittest.main()
