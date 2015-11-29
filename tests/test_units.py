import unittest
from errorpro import units
from errorpro.si import system as si
from errorpro.dimensions.dimensions import Dimension
from errorpro.exceptions import DimensionError
from sympy import S

class UnitsTestCase(unittest.TestCase):

    def test_units(self):
        #parse_unit
        factor, dim, unit = units.parse_unit("13e4*W*s",si)
        self.assertEqual(factor,130000)
        self.assertEqual(dim,Dimension(mass=1,length=2,time=-2))
        self.assertEqual(unit,13e4*si["W"]*si["s"])

        factor, dim, unit = units.parse_unit("",si)
        self.assertEqual(factor,1)
        self.assertEqual(dim,Dimension())
        self.assertEqual(unit,S.One)

        self.assertRaises(ValueError, units.parse_unit, "N*m/z", si)

        #convert_to_unit
        dim=Dimension(mass=1,length=1,time=-2)
        factor, unit = units.convert_to_unit(dim,si)
        self.assertEqual(factor,1)
        self.assertEqual(str(unit),"N")

        factor, unit = units.convert_to_unit(dim,si,onlyBase=True)
        self.assertEqual(factor,1)
        self.assertEqual(str(unit),"kg*m/s**2")

        factor, unit = units.convert_to_unit(dim,si,outputUnit="g*m/s**2")
        self.assertEqual(factor,1e-3)
        self.assertEqual(str(unit),"g*m/s**2")

        self.assertRaises(DimensionError, units.convert_to_unit, dim, si, outputUnit="J")

if __name__ == '__main__':
    unittest.main()
