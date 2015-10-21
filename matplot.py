import matplotlib.pyplot as plt
import numpy as np
from units import convert_to_unit
from quantities import get_dimension
from sympy.utilities.lambdify import lambdify

def plot(quantity_pairs, sym_functions, unit_system, show=True):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # find units and factors
    if len(quantity_pairs)>0:
        x_factor, x_unit = convert_to_unit(quantity_pairs[0][0].dim, unit_system, outputUnit=quantity_pairs[0][0].value_prefUnit)
        y_factor, y_unit = convert_to_unit(quantity_pairs[0][1].dim, unit_system, outputUnit=quantity_pairs[0][1].value_prefUnit)
    else:
        x_factor, x_unit = convert_to_unit(get_dimension(sym_functions[0]), unit_system)
        y_factor, y_unit = convert_to_unit(get_dimension(sym_functions[1]), unit_system)

    x_factor = np.float_(x_factor)
    y_factor = np.float_(y_factor)

    # create arrays to plot
    data_sets = []
    functions = []

    # data to plot
    for qpair in quantity_pairs:
        data_set = {}
        data_set["x_value"] = None if qpair[0].value is None else qpair[0].value / x_factor
        data_set["y_value"] = None if qpair[1].value is None else qpair[1].value / y_factor
        data_set["x_uncert"] = None if qpair[0].uncert is None else qpair[0].uncert / x_factor
        data_set["y_uncert"] = None if qpair[1].uncert is None else qpair[1].uncert / y_factor
        data_set["x_label"] = (qpair[0].longname+" " if qpair[0].longname else "") + qpair[0].name
        data_set["y_label"] = (qpair[1].longname+" " if qpair[1].longname else "") + qpair[1].name
        data_sets.append(data_set)

    # functions to plot
    # TODO doesn't work like this... rethink it!
    for f in sym_functions:
        # check which x-quantity appears in function
        for qpair in quantity_pairs:
            if qpair[0] in f.free_symbols:
                x_quantity = qpair[0]
                break
        else:
            x_quantity = f.free_symbols[0]

        # replace all other quantities by their value
        actual_func = f
        for q in f.free_symbols:
            if not q == x_quantity:
                actual_func = actual_func.subs(q,q.value)

        # create numpy-function
        functions.append(lambdify((x_quantity), actual_func, "numpy"))


    # multiple datasets on one plot
    if len(data_sets) > 1:
        for data_set in data_sets:
            ax.errorbar(data_set["x_value"],
                        data_set["y_value"],
                        xerr = data_set["x_uncert"],
                        yerr = data_set["y_uncert"],
                        c='r',
                        marker="o",
                        linestyle="None",
                        label=data_set["y_label"])
            plt.legend(loc='upper left')
            plt.xlabel("["+str(x_unit)+"]")
            plt.ylabel("["+str(y_unit)+"]")

    # one dataset
    elif len(data_sets)==1:
        ax.errorbar(data_sets[0]["x_value"],
                    data_sets[0]["y_value"],
                    xerr = data_sets[0]["x_uncert"],
                    yerr = data_sets[0]["y_uncert"],
                    c='r',
                    marker="o",
                    linestyle="None")
        plt.xlabel(data_sets[0]["x_label"] + " ["+str(x_unit)+"]")
        plt.ylabel(data_sets[0]["y_label"] + " ["+str(y_unit)+"]")

    if show:
        plt.show()
