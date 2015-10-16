import unittest
import commands
import sympy
from si import system as si
from sympy.physics.unitsystems.dimensions import Dimension

class CommandsTestCase(unittest.TestCase):

    def test_commands(self):
        config={"unitSystem":si}

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

        data = {}
        small=0.0000001
        a.execute(data,config)
        self.assertTrue(data["r"].value - 0.012 < small)
        self.assertEqual(data["r"].value_prefUnit, si["mm"])
        self.assertEqual(data["r"].value_depend, None)
        self.assertEqual(data["r"].dim, Dimension(length=1))
        self.assertTrue(data["r"].uncert - 0.001 < small)
        self.assertEqual(data["r"].uncert_prefUnit, si["m"])
        self.assertEqual(data["r"].uncert_depend, None)
        b.execute(data,config)
        self.assertTrue(data["h"].value - 0.3 < small)
        self.assertEqual(data["h"].value_prefUnit, si["dm"])
        self.assertEqual(data["h"].value_depend, None)
        self.assertEqual(data["h"].dim, Dimension(length=1))
        self.assertTrue(data["h"].uncert - 0.04 < small)
        self.assertEqual(data["h"].uncert_prefUnit, si["cm"])
        self.assertEqual(data["h"].uncert_depend, None)
        c.execute(data,config)
        self.assertTrue(data["V"].value - 0.0001357168 < small)
        self.assertEqual(data["V"].value_prefUnit, None)
        self.assertEqual(data["V"].value_depend, sympy.pi*data["r"]**2*data["h"])
        self.assertEqual(data["V"].dim, Dimension(length=3))
        self.assertTrue(data["V"].uncert - 0.00002896705 < small)
        self.assertEqual(data["V"].uncert_prefUnit, None)
        #self.assertEqual(data["V"].uncert_depend, )
        print(data["V"].uncert)

if __name__ == '__main__':
    unittest.main()
