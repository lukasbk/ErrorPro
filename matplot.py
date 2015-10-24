import matplotlib.pyplot as plt
import numpy as np
from sympy.utilities.lambdify import lambdify


def plot(data_sets, functions, show=True, x_label="", y_label=""):
    """
    'data_sets' and 'functions' must be lists of dictionaries:
     data_set: {x_values, x_uncerts, y_values, y_uncerts, title}
     function: {x, term, title} -> must be adjusted to unit choice already
    """

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # plot data sets
    legend = False
    min = None
    max = None
    for data_set in data_sets:

        # find min and max for function plotting
        min_here = np.amin(data_set["x_values"])
        if min is None or min_here < min:
            min = min_here
        max_here = np.amax(data_set["x_values"])
        if max is None or max_here > max:
            max = max_here

        # plot
        ax.errorbar(data_set["x_values"],
                    data_set["y_values"],
                    xerr = data_set["x_uncerts"],
                    yerr = data_set["y_uncerts"],
                    c='r',
                    marker="o",
                    linestyle="None",
                    label=data_set["title"])
        if data_set["title"]:
            legend = True

    if min is None or max is None:
        # standard min/max if there is no dataset to plot
        min = 0
        max = 10

    # plot functions
    for f in functions:
        term = f["term"]

        # replace all other symbols by their value
        for var in term.free_symbols:
            if not var == f["x"]:
                term = term.subs(var, var.value)

        numpy_func = lambdify((f["x"]), f["term"], "numpy")
        x = np.linspace(min,max,100)
        y = numpy_func(x)
        ax.plot(x,y,label=f["title"])
        if f["title"]:
            legend = True

    if legend:
        plt.legend(loc='upper left')
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    if show:
        plt.show()
