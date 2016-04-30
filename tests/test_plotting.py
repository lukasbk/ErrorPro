import unittest
from errorpro.core import _find_all_dependencies, assign
import numpy as np
from sympy import sqrt

class plotTestCase(unittest.TestCase):

    def test_dependency_unpacking(self):
        a = assign(1)
        b = assign(1)
        c = assign(a**2)
        d = assign(b**2)
        e = assign(c+d)

        self.assertEqual( _find_all_dependencies(sqrt(e), a),
                          sqrt(a**2+d))

if __name__ == '__main__':
    unittest.main()
