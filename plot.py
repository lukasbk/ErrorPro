from quantities import get_value, get_uncertainty, adjust_to_unit, get_dimension, Quantity
from units import convert_to_unit
from sympy import Dummy, S
from exceptions import *

def plot(expr_pairs, config, show=True, save=False):

    # one or multiple things to plot
    if len(expr_pairs) > 1:
        single_plot = False
    else:
        single_plot = True

    unit_system = __import__(config["unit_system"]).system

    x_dim = None
    y_dim = None

    x_unit = None
    y_unit = None

    data_sets = []
    functions = []

    for expr_pair in expr_pairs:
        x = expr_pair[0]
        y = expr_pair[1]

        # check dimensions
        if x_dim is None:
            x_dim = get_dimension(x)
        else:
            if not x_dim == get_dimension(x):
                raise DimensionError("dimension mismatch\n%s != %s" % (x_dim, get_dimension(x)))
        if y_dim is None:
            y_dim = get_dimension(y)
        else:
            if not y_dim == get_dimension(y):
                raise DimensionError("dimension mismatch\n%s != %s" % (y_dim, get_dimension(y)))

    	# if y contains x, it must be a function
        dummy = Dummy("x")
        rep_y = y.subs(x,dummy)
        if rep_y.has(dummy):
            # get titles
            if isinstance(x, Quantity):
                x_title = ((x.longname + " ") if x.longname else "") + str(x)
            else:
                x_title = str(x)
            y_title = str(y)

    		# check if x not only quantity but more complicated expression
            if not isinstance(x,Quantity):
    			# replace by Dummy
                y = rep_y
                x = dummy

            # get factors
            x_factor, x_unit = convert_to_unit(x_dim, unit_system, outputUnit=x_unit)
            y_factor, y_unit = convert_to_unit(y_dim, unit_system, outputUnit=y_unit)

            # scale function to units
            y = y.subs(x,x*x_factor) / y_factor

            # replace all other symbols by their value
            for var in y.free_symbols:
                if not var == x:
                    y = y.subs(var, var.value)

            # if only one thing on plot, write labels to x-axis and y-axis
            if single_plot:
                title = None
                x_label = x_title + ("" if x_unit == S.One else " [" + str(x_unit) + "]")
                y_label = y_title + ("" if y_unit == S.One else " [" + str(y_unit) + "]")
            # if more than one thing, use legend for title
            else:
                title = y_title

            functions.append({"x":x,"term":y,"title":title})

    	# if y doesn't contain x, it must be a data set
        else:

            # calculate expressions first if necessary
            if isinstance(expr_pair[0], Quantity):
                x = expr_pair[0]
                x_title = ((x.longname + " ") if x.longname else "") + str(x)
            else:
                # dummy quantity for calculation
                x = Quantity("")
                x.value = get_value(expr_pair[0])
                x.uncert = get_uncertainty(expr_pair[0])[0]
                x.dim = x_dim
                x_title = str(expr_pair[0])
            if isinstance(expr_pair[1], Quantity):
                y = expr_pair[1]
                y_title = ((y.longname + " ") if y.longname else "") + str(y)
            else:
                # dummy quantity for calculation
                y = Quantity("")
                y.value = get_value(expr_pair[1])
                y.uncert = get_uncertainty(expr_pair[1])[0]
                y.dim = y_dim
                y_title = str(expr_pair[1])


            # get values and uncertainties all in one unit
            x_values, x_uncerts, x_unit = adjust_to_unit(x, unit_system, prefUnit = x_unit)
            y_values, y_uncerts, y_unit = adjust_to_unit(y, unit_system, prefUnit = y_unit)


            # if only one thing on plot, write labels to x-axis and y-axis
            if single_plot:
                title = None
                x_label = x_title + ("" if x_unit == S.One else " [" + str(x_unit) + "]")
                y_label = y_title + ("" if y_unit == S.One else " [" + str(y_unit) + "]")
            # if more than one thing, use legend for title
            else:
                title = y_title

            data_sets.append({"x_values": x_values, "y_values": y_values, "x_uncerts": x_uncerts, "y_uncerts":y_uncerts, "title": title})




    # if more than one thing on plot, write only units to axes
    if not single_plot:
        x_label = ("" if x_unit == S.One else " [" + str(x_unit) + "]")
        y_label = ("" if y_unit == S.One else " [" + str(y_unit) + "]")

    # plot
    if config["plot_module"] == "matplotlib":
        import matplot
        matplot.plot(data_sets, functions, unit_system, show=show, x_label=x_label, y_label=y_label)
    else:
        raise ValueError("There is not plot module called '%s'" % config["plot_module"])
