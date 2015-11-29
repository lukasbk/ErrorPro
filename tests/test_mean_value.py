import unittest
from errorpro.commands import *
from errorpro.quantities import *
import numpy as np
from errorpro.dimensions.dimensions import Dimension
from errorpro.project import Project

class MeanValueTestCase(unittest.TestCase):

    def test_MeanValue(self):

        p = Project()

        # test unweighted mean value
        p.data["a"]=Quantity("a")
        p.data["a"].value = np.float_([3,4,5,6,7,8])
        p.data["a"].dim = Dimension()

        p.mean_value("m","a",longname="Mittelwert")
        self.assertEqual(p.data["m"].name, "m")
        self.assertEqual(p.data["m"].longname, "Mittelwert")
        self.assertTrue(np.fabs(p.data["m"].value - 5.5)<0.000001)
        self.assertTrue(np.fabs(p.data["m"].uncert - 0.84876886033) < 0.000001)
        self.assertEqual(p.data["m"].value_depend, "standard mean value")
        self.assertEqual(p.data["m"].dim, Dimension())


        # test weighted mean value
        p = Project()
        p.data["a"]=Quantity("a")
        p.data["b"]=Quantity("b")
        p.data["a"].value = np.float_([3,4])
        p.data["a"].uncert = np.float_([0.3,0.4])
        p.data["a"].dim = Dimension(length=1)
        p.data["b"].value = np.float_(7)
        p.data["b"].uncert = np.float_(2)
        p.data["b"].dim = Dimension(length=1)

        p.mean_value("n","a","b",longname="Mittel")
        self.assertEqual(p.data["n"].name, "n")
        self.assertEqual(p.data["n"].longname, "Mittel")
        self.assertTrue(np.fabs(p.data["n"].value - 3.41167192429)<0.000001)
        self.assertTrue(np.fabs(p.data["n"].uncert - 0.23829044123) < 0.000001)
        self.assertEqual(p.data["n"].value_depend, "standard weighted mean value")
        self.assertEqual(p.data["n"].dim, Dimension(length=1))

if __name__ == '__main__':
    unittest.main()
