import unittest
from errorpro.project import Project
import numpy as np
from errorpro.quantities import Quantity
from errorpro.dimensions.dimensions import Dimension
from errorpro.si import system as si
from matplotlib.figure import Figure

class PlotTestCase(unittest.TestCase):

    def test_plot(self):
        p = Project()
        p.data["x"]=Quantity("x")
        p.data["y"]=Quantity("y")

        p.data["y"].value_prefUnit = si["ms"]
        p.data["x"].value = np.float_([0,1,2,3,4,5])
        p.data["x"].uncert = np.float_([0.1,0.1,0.2,0.3,0.4,0.3])
        p.data["x"].dim = Dimension(time=1)
        p.data["y"].value = np.float_([1,2.3,1.8,3.4,4.5,8])
        p.data["y"].dim = Dimension(time=1)

        self.assertTrue(isinstance(p.plot(("x","y")), Figure))

if __name__ == '__main__':
    unittest.main()
