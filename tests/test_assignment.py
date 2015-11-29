import unittest
from errorpro import commands
import sympy
from errorpro.dimensions.dimensions import Dimension
from errorpro.exceptions import DimensionError
from sympy import Symbol, S
from errorpro.si import system as si
import numpy as np
from errorpro import fit_scipy
from errorpro.project import Project

class AssignmentTestCase(unittest.TestCase):

    def test_assignment(self):
        p = Project()
        small=0.0000001

        # test single Assignments

        a = commands.Assignment("r","Radius")
        a.value = "12"
        a.value_unit = "mm"
        a.uncert = "1/1000"
        a.uncert_unit = "m"

        a.execute(p)
        self.assertEqual(p.data["r"].name, "r")
        self.assertEqual(p.data["r"].longname, "Radius")
        self.assertTrue(abs(p.data["r"].value - 0.012) < small)
        self.assertEqual(p.data["r"].value_prefUnit, si["mm"])
        self.assertEqual(p.data["r"].value_depend, None)
        self.assertEqual(p.data["r"].dim, Dimension(length=1))
        self.assertTrue(abs(p.data["r"].uncert - 0.001) < small)
        self.assertEqual(p.data["r"].uncert_prefUnit, si["m"])
        self.assertEqual(p.data["r"].uncert_depend, None)


        b = commands.Assignment("h","Höhe")
        b.value = "3"
        b.value_unit = "dm"
        b.uncert = "4"
        b.uncert_unit = "cm"

        b.execute(p)
        self.assertEqual(p.data["h"].name, "h")
        self.assertEqual(p.data["h"].longname, "Höhe")
        self.assertTrue(abs(p.data["h"].value - 0.3) < small)
        self.assertEqual(p.data["h"].value_prefUnit, si["dm"])
        self.assertEqual(p.data["h"].value_depend, None)
        self.assertEqual(p.data["h"].dim, Dimension(length=1))
        self.assertTrue(abs(p.data["h"].uncert - 0.04) < small)
        self.assertEqual(p.data["h"].uncert_prefUnit, si["cm"])
        self.assertEqual(p.data["h"].uncert_depend, None)

        # test calculation

        c = commands.Assignment("V","Volumen")
        c.value = "pi*r**2*h"

        c.execute(p)
        self.assertEqual(p.data["V"].name, "V")
        self.assertEqual(p.data["V"].longname, "Volumen")
        self.assertTrue(abs(p.data["V"].value - 0.0001357168) < small)
        self.assertEqual(p.data["V"].value_prefUnit, None)
        self.assertEqual(p.data["V"].value_depend, sympy.pi*p.data["r"]**2*p.data["h"])
        self.assertEqual(p.data["V"].dim, Dimension(length=3))
        self.assertTrue(abs(p.data["V"].uncert - 0.00002896705) < small)
        self.assertEqual(p.data["V"].uncert_prefUnit, None)
        self.assertEqual(p.data["V"].uncert_depend, sympy.sqrt((Symbol("r_err",positive=True)*sympy.pi*2*p.data["r"]*p.data["h"])**2 + (sympy.pi*Symbol("h_err",positive=True)*p.data["r"]**2)**2))

        # test dimension mismatch

        d = commands.Assignment("V","Vol2")
        d.value = "50"
        d.value_unit = "s"
        d.uncert = "50"
        d.uncert_unit = "A*s"

        self.assertRaises(DimensionError, d.execute, p)

        # test replacing quantity

        e = commands.Assignment("V","Vol3")
        e.value = "50"
        e.value_unit = "s"

        e.execute(p)
        self.assertEqual(p.data["V"].name, "V")
        self.assertEqual(p.data["V"].longname, "Vol3")
        self.assertTrue(abs(p.data["V"].value - 50) < small)
        self.assertEqual(p.data["V"].value_prefUnit, si["s"])
        self.assertEqual(p.data["V"].value_depend, None)
        self.assertEqual(p.data["V"].dim, Dimension(time=1))
        self.assertTrue(p.data["V"].uncert is None)
        self.assertTrue(p.data["V"].uncert_prefUnit is None)
        self.assertTrue(p.data["V"].uncert_depend is None)


        # test p.data set

        f = commands.Assignment("y","Werte")
        f.value = ["12","13","14"]
        f.value_unit = "C"
        f.uncert = ["0.5","0.4","1e-1"]
        f.uncert_unit = "C"
        f.execute(p)

        self.assertEqual(p.data["y"].name, "y")
        self.assertEqual(p.data["y"].longname, "Werte")
        self.assertTrue((np.fabs(p.data["y"].value - np.float_([12,13,14])).all() < small).all())
        self.assertEqual(p.data["y"].value_prefUnit, si["C"])
        self.assertEqual(p.data["y"].value_depend, None)
        self.assertEqual(p.data["y"].dim, Dimension(current=1,time=1))
        self.assertTrue((np.fabs(p.data["y"].uncert - np.float_([0.5,0.4,0.1])) < small).all())
        self.assertEqual(p.data["y"].uncert_prefUnit, si["C"])
        self.assertEqual(p.data["y"].uncert_depend, None)



if __name__ == '__main__':
    unittest.main()
