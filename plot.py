from quantities import get_value,get_uncertainty,adjust_to_unit, Quantity
from units import convert_to_unit

def plot(data_pairs, function_pairs, dims, config, show=True, save=False):

    if len(data_pairs) + len(function_pairs) > 1:
        single_plot = False
    else:
        single_plot = True

    unit_system = __import__(config["unit_system"]).system

    x_unit = None
    y_unit = None

    data_sets = []
    functions = []

    for data_pair in data_pairs:
        data_set = {}

        i = 0
        quants = []
        for expr in data_pair:
            # calculate expression if necessary
            if isinstance(data_pair[i], Quantity):
                quants.append(data_pair[i])
            else:
                # dummy quantity for calculation
                quants.append(Quantity(""))
                quants[i].value = get_value(data_pair[i])
                quants[i].uncert = get_uncertainty(data_pair[i])[0]
                quants[i].dim = dims[i]
            i += 1

        # get values and uncertainties all in one unit
        data_set["x_values"], data_set["x_uncerts"], x_unit = adjust_to_unit(quants[0], unit_system, prefUnit = x_unit)
        data_set["y_values"], data_set["y_uncerts"], y_unit = adjust_to_unit(quants[1], unit_system, prefUnit = y_unit)

        # create title
        y_title = ""
        if quants[1].longname:
            y_title += quants[1].longname
        y_title += str(data_pair[1])
        y_title += " ["+str(y_unit)+"]"

        # write titel to axes or legend
        if single_plot:
            # create xlabel
            x_title = ""
            if quants[0].longname:
                x_title += quants[0].longname
            x_title += str(data_pair[0])
            x_title += " ["+str(x_unit)+"]"

            x_label = x_title
            y_label = y_title
        else:
            data_set["title"] = y_title
        data_sets.append(data_set)

    for function_pair in function_pairs:
        # adjust functions to unit
        x = function_pair[0]
        term = function_pair[1]

        # get factors
        x_factor, x_unit = convert_to_unit(dims[0], unit_system, outputUnit=x_unit)
        y_factor, y_unit = convert_to_unit(dims[1], unit_system, outputUnit=y_unit)

        # scale function to units
        term = term.subs(x,x*x_factor) / y_factor

        # replace all other symbols by their value
        for var in term.free_symbols:
            if not var == x:
                term = term.subs(var, var.value)

        # TODO function titles

        functions.append({"x":x,"term":term})

    # plot
    if config["plot_module"] == "matplotlib":
        import matplot
        matplot.plot(data_sets, functions, unit_system, show=show)
    else:
        raise ValueError("There is not plot module called '%s'" % config["plot_module"])
