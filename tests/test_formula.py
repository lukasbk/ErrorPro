import unittest
from errorpro.quantities import Quantity
from sympy import Symbol
from errorpro.project import Project

class FormulaTestCase(unittest.TestCase):

    def test_formula(self):
        p = Project()
        p.data["U_I"] = Quantity("U_I")
        p.data["I_I"] = Quantity("I_I")
        u_err = Symbol("U_I_err", positive=True)
        i_err = Symbol("I_I_err", positive=True)

        p.data["Z_I"] = Quantity("Z_I", "Impedanz")
        p.data["Z_I"].uncert_depend = u_err * i_err + p.data["U_I"] * p.data["I_I"]**2

        self.assertEqual(p.formula("Z_I",True), r"\sigma{\left (Z_{I} \right )} = I_{I}^{2} U_{I} + \sigma{\left (I_{I} \right )} \sigma{\left (U_{I} \right )}")


if __name__ == '__main__':
    unittest.main()
