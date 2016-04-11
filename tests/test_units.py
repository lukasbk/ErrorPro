import unittest
from errorpro import units
from errorpro.si import system as si
from errorpro.dimensions.dimensions import Dimension
from sympy import S

class UnitsTestCase(unittest.TestCase):

    def test_parse_unit(self):
        factor, dim, unit = units.parse_unit("13e4*W*s")
        self.assertEqual(factor,130000)
        self.assertEqual(dim,Dimension(mass=1,length=2,time=-2))
        self.assertEqual(unit,13e4*si["W"]*si["s"])

    def test_parse_empty_unit(self):
        factor, dim, unit = units.parse_unit("")
        self.assertEqual(factor,1)
        self.assertEqual(dim,Dimension())
        self.assertEqual(unit,S.One)

    def test_parse_invalid_unit(self):
        self.assertRaises(ValueError, units.parse_unit, "N*m/z")

    def test_convert_to_unit(self):
        dim=Dimension(mass=1,length=1,time=-2)
        factor, unit = units.convert_to_unit(dim)
        self.assertEqual(factor,1)
        self.assertEqual(str(unit),"N")

    def test_convert_to_unit_with_only_base(self):
        dim=Dimension(mass=1,length=1,time=-2)
        factor, unit = units.convert_to_unit(dim,only_base=True)
        self.assertEqual(factor,1)
        self.assertEqual(str(unit),"kg*m/s**2")

    def test_convert_to_unit_with_output_unit(self):
        dim=Dimension(mass=1,length=1,time=-2)
        factor, unit = units.convert_to_unit(dim,output_unit="g*m/s**2")
        self.assertEqual(factor,1e-3)
        self.assertEqual(str(unit),"g*m/s**2")

    def test_convert_to_unit_dimension_mismatch(self):
        dim=Dimension(mass=1,length=1,time=-2)
        self.assertRaises(RuntimeError, units.convert_to_unit, dim, output_unit="J")

if __name__ == '__main__':
    unittest.main()
