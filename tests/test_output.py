import unittest
from output import Output, format_quantity
from quantities import Quantity
import numpy as np
from sympy.physics.unitsystems.dimensions import Dimension
from si import system as si

# most not suitable for automated testing, so must be tested manually
if __name__ == '__main__':

    config = {"unit_system":"si",
              "directory":"results",
              "auto_results":"results.csv",
              "rounding":True}
    output=Output()

    data = {}

    output.save(data, config)




class OutputTestCase(unittest.TestCase):

    def test_output(self):

        # test function 'format_quantity'
        q = Quantity("C", "Kapazität")
        q.value = np.float_(0.0023534)
        q.uncert = np.float_(0.0002786)
        q.dim = Dimension(mass=-1,length=-2,time=4,current=2)

        description, value_str, uncert_str, unit = format_quantity(q, si, True)

        self.assertEqual(description, "Kapazität C")
        self.assertEqual(value_str, "0.00235")
        self.assertEqual(uncert_str, "0.00028")
        self.assertEqual(unit,"F")
