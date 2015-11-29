import unittest
import errorpro.fit_scipy as sc
from errorpro.quantities import Quantity
import numpy as np
from errorpro.project import Project
from errorpro import commands

#TODO Test for start parameters and weighting y-uncertainties

class fitTestCase(unittest.TestCase):

    def test_fit(self):
        # test fit_scipy on its own
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


        # test fit command

        small = 0.001

        p = Project()

        g = commands.Assignment("x")
        g.value = ["1","2","3"]
        g.value_unit = "A"
        g.execute(p)

        g = commands.Assignment("y")
        g.value = ["6","3","2.1"]
        g.value_unit = "C"
        g.uncert = ["1","1","2"]
        g.uncert_unit = "1e-1*C"
        g.execute(p)

        h = commands.Assignment("m")
        h.value = "1"
        h.value_unit = "s"
        h.execute(p)

        i = commands.Assignment("b")
        i.value = "1"
        i.value_unit = "C"
        i.execute(p)

        p.fit("m*x+b",("x","y"),["m","b"])
        self.assertTrue(abs(p.data["m"].value - (-2.3)) < small)
        self.assertTrue(abs(p.data["m"].uncert - 0.7) < small)
        self.assertTrue(abs(p.data["b"].value - 8.06667) < small)
        self.assertTrue(abs(p.data["b"].uncert - 1.257) < small)

        p.fit("m*x+b",("x","y"),["m","b"],weighted=False)
        self.assertTrue(abs(p.data["m"].value - (-1.95)) < small)
        self.assertTrue(abs(p.data["m"].uncert - 0.6062) < small)
        self.assertTrue(abs(p.data["b"].value - 7.6) < small)
        self.assertTrue(abs(p.data["b"].uncert - 1.31) < small)

        p.data["y"].uncert = None
        self.assertRaises(RuntimeError,p.fit,"m*x+b",("x","y"),["m","b"],weighted=True)

if __name__ == '__main__':
    unittest.main()
