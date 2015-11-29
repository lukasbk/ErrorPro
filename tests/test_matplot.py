import errorpro.plot_mat as matplot
import numpy as np
from errorpro.dimensions.dimensions import Dimension
from errorpro.si import system as si
from errorpro.quantities import Quantity


# not suitable for automated testing, so must be tested manually

if __name__ == '__main__':


    # single data set

    data = {
            "t": Quantity("t","Zeit"),
            "v": Quantity("v","Geschwindigkeit"),
            "t0": Quantity("t0","Startzeit"),
            "e": Quantity("e","Bremsdings"),
            "s": Quantity("s","Startgeschwindigkeit")
            }

    data["t"].value = np.float_([0,1,2,3,4,5])
    data["t"].dim = Dimension(time=1)

    data["v"].value = np.float_([33,23,14,10,7,3])
    data["v"].uncert = np.float_([1,2,1.3,2.1,0.5,0.6])
    data["v"].value_prefUnit = si["km"]/si["h"]
    data["v"].dim = Dimension(length=1,time=-1)



    matplot.plot([(data["t"],data["v"])], [], si, show=True)
