import unittest
import commands
import sympy
from sympy.physics.unitsystems.dimensions import Dimension
from exceptions import DimensionError
from sympy import Symbol, S
from si import system as si
import numpy as np
import fit_scipy
from output import Output

class CommandsTestCase(unittest.TestCase):

    def test_commands(self):
        output = Output()
        config = {"unit_system":"si",
                  "fit_module":"scipy",
                  "plot_module":"matplotlib"}
        data = {}
        small=0.0000001

        # test single Assignments

        a = commands.Assignment("r","Radius")
        a.value = "12"
        a.value_unit = "mm"
        a.uncert = "1/1000"
        a.uncert_unit = "m"

        a.execute(data,config,output)
        self.assertEqual(data["r"].name, "r")
        self.assertEqual(data["r"].longname, "Radius")
        self.assertTrue(abs(data["r"].value - 0.012) < small)
        self.assertEqual(data["r"].value_prefUnit, si["mm"])
        self.assertEqual(data["r"].value_depend, None)
        self.assertEqual(data["r"].dim, Dimension(length=1))
        self.assertTrue(abs(data["r"].uncert - 0.001) < small)
        self.assertEqual(data["r"].uncert_prefUnit, si["m"])
        self.assertEqual(data["r"].uncert_depend, None)


        b = commands.Assignment("h","Höhe")
        b.value = "3"
        b.value_unit = "dm"
        b.uncert = "4"
        b.uncert_unit = "cm"

        b.execute(data,config,output)
        self.assertEqual(data["h"].name, "h")
        self.assertEqual(data["h"].longname, "Höhe")
        self.assertTrue(abs(data["h"].value - 0.3) < small)
        self.assertEqual(data["h"].value_prefUnit, si["dm"])
        self.assertEqual(data["h"].value_depend, None)
        self.assertEqual(data["h"].dim, Dimension(length=1))
        self.assertTrue(abs(data["h"].uncert - 0.04) < small)
        self.assertEqual(data["h"].uncert_prefUnit, si["cm"])
        self.assertEqual(data["h"].uncert_depend, None)

        # test calculation

        c = commands.Assignment("V","Volumen")
        c.value = "pi*r**2*h"

        c.execute(data,config,output)
        self.assertEqual(data["V"].name, "V")
        self.assertEqual(data["V"].longname, "Volumen")
        self.assertTrue(abs(data["V"].value - 0.0001357168) < small)
        self.assertEqual(data["V"].value_prefUnit, None)
        self.assertEqual(data["V"].value_depend, sympy.pi*data["r"]**2*data["h"])
        self.assertEqual(data["V"].dim, Dimension(length=3))
        self.assertTrue(abs(data["V"].uncert - 0.00002896705) < small)
        self.assertEqual(data["V"].uncert_prefUnit, None)
        self.assertEqual(data["V"].uncert_depend, sympy.sqrt((Symbol("r_err",positive=True)*sympy.pi*2*data["r"]*data["h"])**2 + (sympy.pi*Symbol("h_err",positive=True)*data["r"]**2)**2))

        # test dimension mismatch

        d = commands.Assignment("V","Vol2")
        d.value = "50"
        d.value_unit = "s"

        self.assertRaises(DimensionError, d.execute, data, config, output)

        # test replacing quantity

        e = commands.Assignment("V","Vol3")
        e.value = "50"
        e.value_unit = "s"
        e.uncert = "3"
        e.uncert_unit = "s"

        e.execute(data,config,output)
        self.assertEqual(data["V"].name, "V")
        self.assertEqual(data["V"].longname, "Vol3")
        self.assertTrue(abs(data["V"].value - 50) < small)
        self.assertEqual(data["V"].value_prefUnit, si["s"])
        self.assertEqual(data["V"].value_depend, None)
        self.assertEqual(data["V"].dim, Dimension(time=1))
        self.assertTrue(abs(data["V"].uncert - 3) < small)
        self.assertEqual(data["V"].uncert_prefUnit, si["s"])
        self.assertEqual(data["V"].uncert_depend, None)


        # test data set

        f = commands.Assignment("y","Werte")
        f.value = ["12","13","14"]
        f.value_unit = "C"
        f.uncert = ["0.5","0.4","1e-1"]
        f.uncert_unit = "C"
        f.execute(data, config,output)

        self.assertEqual(data["y"].name, "y")
        self.assertEqual(data["y"].longname, "Werte")
        self.assertTrue((np.fabs(data["y"].value - np.float_([12,13,14])).all() < small).all())
        self.assertEqual(data["y"].value_prefUnit, si["C"])
        self.assertEqual(data["y"].value_depend, None)
        self.assertEqual(data["y"].dim, Dimension(current=1,time=1))
        self.assertTrue((np.fabs(data["y"].uncert - np.float_([0.5,0.4,0.1])) < small).all())
        self.assertEqual(data["y"].uncert_prefUnit, si["C"])
        self.assertEqual(data["y"].uncert_depend, None)

        # test fit

        g = commands.Assignment("x")
        g.value = ["1","2","3.124987"]
        g.value_unit = "A"
        g.uncert = ["1","1","0.056"]
        g.uncert_unit = "1e-1*A"
        g.execute(data, config,output)

        h = commands.Assignment("m")
        h.value = "1"
        h.value_unit = "s"
        h.execute(data, config,output)

        i = commands.Assignment("b")
        i.value = "1"
        i.value_unit = "C"
        i.execute(data, config, output)

        j = commands.Fit("m*x+b","x","y",["m","b"])
        j.execute(data,config,output)

        # TODO fit-Assertions



if __name__ == '__main__':
    unittest.main()
