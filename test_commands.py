import unittest
import commands
import sympy
from si import system as si
from sympy.physics.unitsystems.dimensions import Dimension
from sympy import Symbol, S
import numpy as np

class CommandsTestCase(unittest.TestCase):

    def test_single_assignments(self):
        config={"unit_system":si}

        a = commands.Assignment("r","Radius")
        a.value = "12"
        a.value_unit = "mm"
        a.uncert = "1/1000"
        a.uncert_unit = "m"

        b = commands.Assignment("h","Höhe")
        b.value = "3"
        b.value_unit = "dm"
        b.uncert = "4"
        b.uncert_unit = "cm"

        c = commands.Assignment("V","Volumen")
        c.value = "pi*r**2*h"

        d = commands.Assignment("V","Vol2")
        d.value = "50"
        d.value_unit = "s"

        e = commands.Assignment("V","Vol3")
        e.value = "50"
        e.value_unit = "s"
        e.uncert = "3"
        e.uncert_unit = "s"

        data = {}
        small=0.0000001
        a.execute(data,config)
        self.assertEqual(data["r"].name, "r")
        self.assertEqual(data["r"].longname, "Radius")
        self.assertTrue(abs(data["r"].value - 0.012) < small)
        self.assertEqual(data["r"].value_prefUnit, si["mm"])
        self.assertEqual(data["r"].value_depend, None)
        self.assertEqual(data["r"].dim, Dimension(length=1))
        self.assertTrue(abs(data["r"].uncert - 0.001) < small)
        self.assertEqual(data["r"].uncert_prefUnit, si["m"])
        self.assertEqual(data["r"].uncert_depend, None)
        b.execute(data,config)
        self.assertEqual(data["h"].name, "h")
        self.assertEqual(data["h"].longname, "Höhe")
        self.assertTrue(abs(data["h"].value - 0.3) < small)
        self.assertEqual(data["h"].value_prefUnit, si["dm"])
        self.assertEqual(data["h"].value_depend, None)
        self.assertEqual(data["h"].dim, Dimension(length=1))
        self.assertTrue(abs(data["h"].uncert - 0.04) < small)
        self.assertEqual(data["h"].uncert_prefUnit, si["cm"])
        self.assertEqual(data["h"].uncert_depend, None)
        c.execute(data,config)
        self.assertEqual(data["V"].name, "V")
        self.assertEqual(data["V"].longname, "Volumen")
        self.assertTrue(abs(data["V"].value - 0.0001357168) < small)
        self.assertEqual(data["V"].value_prefUnit, None)
        self.assertEqual(data["V"].value_depend, sympy.pi*data["r"]**2*data["h"])
        self.assertEqual(data["V"].dim, Dimension(length=3))
        self.assertTrue(abs(data["V"].uncert - 0.00002896705) < small)
        self.assertEqual(data["V"].uncert_prefUnit, None)
        self.assertEqual(data["V"].uncert_depend, sympy.sqrt((Symbol("r_err",positive=True)*sympy.pi*2*data["r"]*data["h"])**2 + (sympy.pi*Symbol("h_err",positive=True)*data["r"]**2)**2))

        self.assertRaises(RuntimeError, d.execute, data, config)

        e.execute(data,config)
        self.assertEqual(data["V"].name, "V")
        self.assertEqual(data["V"].longname, "Vol3")
        self.assertTrue(abs(data["V"].value - 50) < small)
        self.assertEqual(data["V"].value_prefUnit, si["s"])
        self.assertEqual(data["V"].value_depend, None)
        self.assertEqual(data["V"].dim, Dimension(time=1))
        self.assertTrue(abs(data["V"].uncert - 3) < small)
        self.assertEqual(data["V"].uncert_prefUnit, si["s"])
        self.assertEqual(data["V"].uncert_depend, None)

    def test_multi_assignments(self):
        data = {}
        config = {"unit_system":si}
        small=0.0000001
        a = commands.Assignment("a")
        a.value = ["12","13","14"]
        a.uncert = ["1","0.4","1e-1"]
        a.execute(data, config)

        self.assertEqual(data["a"].name, "a")
        self.assertEqual(data["a"].longname, "")
        self.assertTrue((np.fabs(data["a"].value - np.float_([12,13,14])).all() < small).all())
        self.assertEqual(data["a"].value_prefUnit, None)
        self.assertEqual(data["a"].value_depend, None)
        self.assertEqual(data["a"].dim, Dimension())
        self.assertTrue((np.fabs(data["a"].uncert - np.float_([1,0.4,0.1])) < small).all())
        self.assertEqual(data["a"].uncert_prefUnit, None)
        self.assertEqual(data["a"].uncert_depend, None)

if __name__ == '__main__':
    unittest.main()
