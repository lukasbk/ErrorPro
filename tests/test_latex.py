import unittest
import latex
from quantities import Quantity
from sympy import Symbol

class LatexTestCase(unittest.TestCase):

    def test_latex(self):
        u = Quantity("U_I")
        i = Quantity("I_I")
        u_err = Symbol("U_I_err", positive=True)
        i_err = Symbol("I_I_err", positive=True)

        z = Quantity("Z_I", "Impedanz")
        z.uncert_depend = u_err * i_err + u * i**2

        self.assertEqual(latex.uncert_formula(z,True), r"\sigma{\left (Z_{I} \right )} = I_{I}^{2} U_{I} + \sigma{\left (I_{I} \right )} \sigma{\left (U_{I} \right )}")


if __name__ == '__main__':
    unittest.main()
