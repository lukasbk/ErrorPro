import unittest
from errorpro.project import Project
from errorpro.quantities import Quantity
import numpy as np

class concatTestCase(unittest.TestCase):

    def test_concat(self):
        p = Project()

        p.data["a"] = Quantity("a")
        p.data["a"].value = np.float_([1,2,3])
        p.data["b"] = Quantity("b")
        p.data["b"].value = np.float_(4)
        p.concat("c","a","b")

        self.assertTrue((p.data["c"].value == np.float_([1,2,3,4])).all())

if __name__ == '__main__':
    unittest.main()
