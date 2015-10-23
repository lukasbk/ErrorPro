from commands import *
import numpy as np
from quantities import Quantity
from sympy.physics.unitsystems.dimensions import Dimension

# most not suitable for automated testing, so must be tested manually
if __name__ == '__main__':

    data = {
            "x":Quantity("x"),
            "y":Quantity("y")
            }
    config = {
                "plot_module":"matplotlib",
                "unit_system":"si"
            }
    output = None

    data["x"].value = np.float_([0,1,2,3,4,5])
    data["x"].dim = Dimension(length=1)
    data["y"].value = np.float_([1,2.3,1.8,3.4,4.5,8])
    data["y"].dim = Dimension(length=1)

    a = Plot()
    a.expr_pairs.append(("x","y"))
    a.expr_pairs.append(("x","3*x"))
    a.execute(data,config,output)
