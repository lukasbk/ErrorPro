from commands import *
import numpy as np
from quantities import Quantity
from sympy.physics.unitsystems.dimensions import Dimension
from si import system as si

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

    data["y"].value_prefUnit = si["ms"]
    data["x"].value = np.float_([0,1,2,3,4,5])
    data["x"].uncert = np.float_([0.1,0.1,0.2,0.3,0.4,0.3])
    data["x"].dim = Dimension(time=1)
    data["y"].value = np.float_([1,2.3,1.8,3.4,4.5,8])
    data["y"].dim = Dimension(time=1)

    a = Plot()
    a.expr_pairs.append(("x**2","y**2"))
    a.expr_pairs.append(("x**2","3*x**2"))
    a.execute(data,config,output)
