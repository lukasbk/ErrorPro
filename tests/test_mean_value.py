import unittest
from commands import *
from quantities import *
from output import Output
import numpy as np
from sympy.physics.unitsystems.dimensions import Dimension

class MeanValueTestCase(unittest.TestCase):

    def test_MeanValue(self):

        config = {}
        output = Output()

        # test unweighted mean value
        data = {
            "a":Quantity("a")
            }
        data["a"].value = np.float_([3,4,5,6,7,8])
        data["a"].dim = Dimension()

        a = MeanValue("m")
        a.quantities.append("a")
        a.longname = "Mittelwert"
        a.execute(data, config, output)
        self.assertEqual(data["m"].name, "m")
        self.assertEqual(data["m"].longname, "Mittelwert")
        self.assertTrue(np.fabs(data["m"].value - 5.5)<0.000001)
        self.assertTrue(np.fabs(data["m"].uncert - 0.84876886033) < 0.000001)
        self.assertEqual(data["m"].value_depend, "standard mean value")
        self.assertEqual(data["m"].dim, Dimension())


        # test weighted mean value
        data = {
            "a":Quantity("a"),
            "b":Quantity("b")
            }
        data["a"].value = np.float_([3,4])
        data["a"].uncert = np.float_([0.3,0.4])
        data["a"].dim = Dimension(length=1)
        data["b"].value = np.float_(7)
        data["b"].uncert = np.float_(2)
        data["b"].dim = Dimension(length=1)

        a = MeanValue("n")
        a.quantities.extend(["a","b"])
        a.longname = "Mittel"
        a.execute(data, config, output)
        self.assertEqual(data["n"].name, "n")
        self.assertEqual(data["n"].longname, "Mittel")
        self.assertTrue(np.fabs(data["n"].value - 3.41167192429)<0.000001)
        self.assertTrue(np.fabs(data["n"].uncert - 0.23829044123) < 0.000001)
        self.assertEqual(data["n"].value_depend, "standard weighted mean value")
        self.assertEqual(data["n"].dim, Dimension(length=1))

if __name__ == '__main__':
    unittest.main()
