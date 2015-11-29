# maybe from errorpro import * ?
from errorpro.quantities import Quantity, parse_expr, get_dimension
from errorpro.exceptions import DimensionError
import errorpro.plot as plotting
from errorpro.mean_value import mean_value
from errorpro.parsing.parsing import parse_file, parse
from errorpro.quantities import adjust_to_unit, parse_expr, get_value, get_dimension, get_uncertainty, qtable
from errorpro.units import parse_unit
from errorpro.dimensions.dimensions import Dimension
from errorpro.dimensions.solvers import dim_solve
from errorpro import interpreter
from errorpro import output
from sympy import latex, Symbol, Function, Expr, S, sympify
import numpy as np
from IPython.display import Latex as render_latex
from errorpro import pytex
from importlib import import_module

def red_qtable(*quantities, html=True, maxcols=5, u_sys='si'):
    """ Represent quantites in a table.

    Args:
        quantities: List of quantity objects.
        html: If True, output will be formatted to be displayable html.
            Else, LaTeX and html code is returned in a tuple.
        maxcols:
            Maximum number of columns. Table will be split.
        u_sys: String specifying unit system.

    Returns:
        String of html code (html=True) or tuple (LaTeX table, html table).
    """

    if len(quantities) == 0:
        return 'No quantities selected.'

    # this does not look like a neat solution...
    unit_system = import_module("errorpro." + u_sys).system
    cols = []
    if html:
        if not maxcols:
            maxcols = len(quantities)

        def chunks(l):
            for i in range(0, len(quantities), maxcols):
                yield l[i:i+maxcols]

        html = []
        ltx = []
        for chunk in chunks(quantities):
            print(chunk)
            l, h = qtable(*chunk, html=False, maxcols=None)
            html.append(h)
            ltx.append(l)

        htmlb, htmlc = pytex.hide_div('Data', ''.join(html))
        ltxb, ltxc = pytex.hide_div('LaTeX', ''.join(ltx))

        res = 'Displaying: %s<div width=20px/>%s%s<hr/>%s<br>%s' % (
            ', '.join('$%s$' % latex(q) for q in quantities),
            htmlb, ltxb, htmlc, ltxc)

        return res

    for quant in quantities:
        assert isinstance(quant, Quantity)

        value, uncert, unit = adjust_to_unit(quant, unit_system)

        header = quant.longname + ' ' if quant.longname else ''
        header += '$%s \\; \\mathrm{\\left[%s\\right]}$' % (
            latex(quant), latex(unit))

        column = [header]
        if uncert is None:
            if isinstance(value, np.ndarray):
                column.extend(pytex.align_num_list(value))
            else:
                column.append(pytex.align_num(value))
        else:
            if isinstance(value, np.ndarray):
                column.extend(pytex.format_valerr_list(value,uncert))
            else:
                column.append(pytex.format_valerr(value,uncert))
        cols.append(column)

    return (pytex.table_latex(cols), pytex.table_html(cols))


class Project():
    def __init__(self):
        self.data = {}
        # standard configuration
        self.config = {"unit_system":"si",
                       "fit_module":"scipy",
                       "directory":".",
                       "plot_module":"matplotlib",
                       "auto_csv":"results.csv",
                       "rounding":True
                       }

    def save(self):
        unit_system = import_module(
            "errorpro." + self.config["unit_system"]).system
        if not self.config["auto_csv"] is None or self.config["auto_csv"]=="":
            output.save_as_csv(self.data, unit_system, self.config["auto_csv"])

        # TODO automatic uncertainty formulas file

    # rename to config? A little bit more specific...
    def set(self, entry, value):
        """ Change entry of configuration

        Args:
            entry: configuration entry name
            value: new value to assign to entry

        Currently usable entries:
            "plot_module": "gnuplot" or "matplotlib"
            "auto_csv": filename of automatic csv results file,
                None if not wanted

        """
        self.config[entry] = value

    def load(self, filename):
        """ Read and execute file containing data or commands

        Args: filename
        """

        # parse
        syntax_tree = parse_file(filename)

        # interpret
        commands = interpreter.interpret(syntax_tree)

        # execute
        for c in commands:
            c.execute(self)

    def calc(self, calc):
        """ parses and executes calculations

        Args:
            calc: string of calculation(s) like in data file
        """

        # parse
        syntax_tree = parse(calc)

        # interpret
        commands = interpreter.interpret(syntax_tree)

        # execute
        for c in commands:
            c.execute(self)


    def formula(self, quantity, adjust=True):
        """ returns uncertainty formula of quantity as latex code

        Args:
            quantity: name of quantity or Quantity object
            adjust: if True, replaces "_err" suffix by "\sigma" function and adds equals sign in front

        Return:
            latex code string of uncertainty formula
        """

        quantity = parse_expr(quantity, self.data)
        assert isinstance(quantity, Quantity)

        if quantity.uncert_depend is None:
            raise ValueError("quantity '%s' doesn't have an uncertainty formula.")

        formula = quantity.uncert_depend
        if isinstance(formula,str):
            return formula
        else:
            # replace "_err" by sigma function
            if adjust:
                sigma = Function("\sigma")
                for var in formula.free_symbols:
                    if var.name[-4:] == "_err":
                        formula = formula.subs(var, sigma( Symbol(var.name[:-4], **var._assumptions)))
                return latex(sigma(quantity)) + " = " + latex(formula)
            return formula

    def mean_value(self, quantity_to_assign, *quantities, weighted=None, longname=None):
        """ Calculates mean value of quantities and assigns it to new quantity

        Args:
            quantity_to_assign: name or quantity object of new mean value
            quantities: one or more quantities names or objects of which mean value shall be calculated
            weighted: if True, will weight mean value by uncertainties (returns error if not possible)
                      if False, will not weight mean value by uncertainties
                      if None, will try to weight mean value, but if at least one uncertainty is not given, will not weight it
            longname: description for mean value quantity
        """
        # get quantities
        quantities_obj = []
        for q in quantities:
            q_obj = parse_expr(q, self.data)
            assert isinstance(q_obj, Quantity)
            quantities_obj.append(q_obj)

        if isinstance(quantity_to_assign, str):
            name = quantity_to_assign
        elif isinstance(quantity_to_assign, Quantity):
            name = quantity_to_assign.name
        quantity_to_assign = Quantity(name, longname)
        self.data[name] = quantity_to_assign

        # standard behaviour for "weighted"
        if weighted is True:
            force_weighted = True
        else:
            force_weighted = False
        if weighted is None:
            weighted = True

        mean_value(quantity_to_assign, quantities_obj, weighted=weighted, force_weighted=force_weighted)


    def plot(self, *expr_pairs, save=None, xunit=None, yunit=None, ignore_dim=False):
        """ Plots data or functions

        Args:
            expr_pairs_str: one or more pair of quantity on x-axis and on y-axis. e.g. ["p","V"]
                            y-axis can also be a function. e.g. ["t", "7*exp(t/t0)"]
            show: Bool, if plot is supposed to be shown
            save: Bool, if plot is supposed to be saved to file
            xunit: unit on x-axis. if not given, will find unit on its own
            yunit: unit on y-axis. if not given, will find unit on its own
        """

        # TODO x- und y-range angeben

        unit_system = import_module("errorpro." + self.config["unit_system"]).system

        if len(expr_pairs) == 0:#
            raise ValueError("nothing to plot specified.")

        expr_pairs_obj = []

        for expr_pair in expr_pairs:
            # parse expressions
            expr_pairs_obj.append( (parse_expr(expr_pair[0], self.data), parse_expr(expr_pair[1], self.data)) )


        if not xunit is None:
            xunit = parse_unit(xunit, unit_system)[2]
        if not yunit is None:
            yunit = parse_unit(yunit, unit_system)[2]
        return plotting.plot(expr_pairs_obj, self.config, save=save, xunit=xunit, yunit=yunit, ignore_dim=ignore_dim)



    def fit(self, fit_function, xydata, parameters, weighted=None, plot=False, ignore_dim=False):
        """ fits function to data

        Args:
            fit_function_str: function to fit, e.g. "n*t**2 + m*t + b"
            xydata_str: pair of x-quantity and y-quantity of data to fit to, e.g. ["t","U"]
            parameters_str: list of parameters in fit function, e.g. ["n","m","b"]
            weighted: if True, will weight fit by uncertainties (returns error if not possible)
                      if False, will not weight fit by uncertainties
                      if None, will try to weight fit, but if at least one uncertainty is not given, will not weight it
            plot: Bool, if data and fit function should be plotted
        """


        #TODO Support fuer mehr als 1-dimensionale datasets

        if self.config["fit_module"] == "scipy":
            import errorpro.fit_scipy as fit_module
        elif self.config["fit_module"] == "gnuplot":
            import errorpro.gnuplot as fit_module
        else:
            raise ValueError("no fit module called '%s'." % self.config["fit_module"])

        # get parameter quantities
        parameters_obj = []
        for p in parameters:
            if isinstance(p, str):
                if not p in self.data:
                    self.data[p] = Quantity(p)
                    self.data[p].dim = Dimension()
                parameters_obj.append(self.data[p])
            elif isinstance(p, Quantity):
                parameters_obj.append(p)
            else:
                raise TypeError("parameters can only be strings or Quantity objects")

        # parse fit function
        fit_function = parse_expr(fit_function, self.data)

        # get data quantities
        x_data = parse_expr(xydata[0], self.data)
        # if x-data is an expression
        if not isinstance(x_data, Quantity):
            dummy = Quantity()
            fit_function = fit_function.subs(x_data,dummy)
            dummy.value = get_value(x_data)
            dummy.uncert = get_uncertainty(x_data)[0]
            dummy.dim = get_dimension(x_data)
            x_data = dummy
        y_data = parse_expr(xydata[1], self.data)
        # if y-data is an expression
        if not isinstance(y_data, Quantity):
            dummy = Quantity()
            dummy.value = get_value(y_data)
            dummy.uncert = get_uncertainty(y_data)[0]
            dummy.dim = get_dimension(y_data)
            y_data = dummy

        # check if dimension fits
        if not ignore_dim:
            try:
                dim_func = get_dimension(fit_function)
            except ValueError:
                dim_func = None
            if not dim_func == y_data.dim:
                # try to solve for dimensionless parameters
                known_dimensions = {x_data.name: x_data.dim}
                known_dimensions = dim_solve(fit_function, y_data.dim, known_dimensions)
                for q_name in known_dimensions:
                    if q_name in self.data:
                        self.data[q_name].dim = known_dimensions[q_name]
                dim_func = get_dimension(fit_function)
                # if it still doesn't work, raise error
                if not dim_func == y_data.dim:
                    raise DimensionError("dimension of fit function %s doesn't fit dimension of y-data %s" % (dim_func, y_data.dim))

        # fit
        values, uncerts = fit_module.fit(x_data, y_data, fit_function, parameters_obj, weighted)


        # save results
        i = 0
        for p in parameters_obj:
            p.value = values[i]
            p.value_depend = "fit"
            p.uncert = uncerts[i]
            p.uncert_depend = "fit"
            i += 1

        # plot
        if plot:
            return plotting.plot([(x_data, y_data), (x_data, fit_function)], self.config, ignore_dim=ignore_dim)


    def assign(self, name, longname=None, value=None, uncert=None, unit=None, value_unit=None,  uncert_unit=None, replace=False, ignore_dim=False):
        """ Assigns value and/or uncertainty to quantity

        Args:
            name: quantity name
            longname: description of quantity
            value: value to assign, can be expression, string, list or number
            uncert: uncertainty to assign, can be expression, string, list or number, but mustn't depend on other quantities
            unit: unit of both value and uncertainty, replaces 'value_unit' and 'uncert_unit' if given
            value_unit: value unit expression or string
            uncert_unit: uncertainty unit expression or string
            replace: if True, will replace quantity instead of trying to keep data
            ignore_dim: if True, will ignore calculated dimension and use given unit instead
        """

        if not unit is None:
            value_unit = unit
            uncert_unit = unit

        unit_system = import_module("errorpro." + self.config["unit_system"]).system

        if value is None and uncert is None:
            raise ValueError("At least either value or uncertainty must be specified.")

        value_len = None
        value_dim = None
        value_depend = None
        uncert_len = None
        uncert_dim = None
        uncert_depend = None

        # if value is given
        if not value is None:

            # parse unit if given
            if not value_unit is None:
                factor, value_dim, value_unit = parse_unit(value_unit, unit_system)

            # parse value
            if isinstance(value, list) or isinstance(value, tuple):
                # if it's a list, parse each element
                parsed_list = []
                for v in value:
                    parsed_list.append(parse_expr(v, self.data))
            elif isinstance(value, str) or isinstance(value, Expr):
                # if it's not a list, parse once
                value = parse_expr(value, self.data)

            # if it's a calculation
            if isinstance(value, Expr) and not value.is_number:
                # calculate value from dependency
                value_depend = value
                value = get_value(value_depend)

                # calculate dimension from dependency
                if not ignore_dim:
                    calculated_dim = get_dimension(value_depend)
                    if not value_dim is None and not calculated_dim == value_dim:
                        raise DimensionError("dimension mismatch for '%s'\n%s != %s" % (name, value_dim, calculated_dim))
                    elif value_dim is None:
                        value_dim = calculated_dim
                else:
                    # if ignore_dim is True and there's no unit given -> dimensionless
                    if value_dim is None:
                        factor=1
                        value_dim = Dimension()
                        value_unit = S.One
                    # calculated value must be converted to given unit (ignore_dim=True)
                    value = np.float_(factor)*value


            # if it's a number
            else:
                # if no unit given, set dimensionless
                if value_unit is None:
                    factor = 1
                    value_dim = Dimension()
                    value_unit = S.One

                value=np.float_(factor)*np.float_(value)

            # calculate value length
            if isinstance(value,np.ndarray):
                value_len = len(value)
            else:
                value_len = 1


        # if uncertainty is given
        if not uncert is None:

            # parse unit if given
            if not uncert_unit is None:
                factor, uncert_dim, uncert_unit = parse_unit(uncert_unit, unit_system)

            # parse value
            if isinstance(uncert, list) or isinstance(uncert, tuple):
                # if it's a list, parse each element
                parsed_list = []
                for u in uncert:
                    parsed_list.append(parse_expr(u, self.data))
            elif isinstance(uncert, str) or isinstance(uncert, Expr):
                # if it's not a list, parse once
                uncert = parse_expr(uncert, self.data)

            # make sure uncertainty is a number
            if isinstance(uncert, Expr) and not uncert.is_number:
                raise RuntimeError("uncertainty '%s' is not a number" % uncert)

            # if no unit given, set dimensionless
            if uncert_unit is None:
                factor = 1
                uncert_dim = Dimension()
                uncert_unit = S.One

            uncert=np.float_(factor)*np.float_(uncert)

            # calculate uncertainty length, ignore len(uncert)==1 because it can be duplicated to fit any value length
            if isinstance(uncert,np.ndarray):
                uncert_len = len(uncert)

        # if uncertainty can be calculated
        elif not value_depend is None:
            uncert, uncert_depend = get_uncertainty(value_depend)


        # merge dimensions
        dim = value_dim
        if not dim is None and not uncert_dim is None and not dim == uncert_dim:
            raise DimensionError("value dimension and uncertainty dimension are not the same\n%s != %s" % (dim, uncert_dim))
        if not uncert_dim is None:
            dim = uncert_dim

        # merge lengths
        new_len = value_len
        if not new_len is None and not uncert_len is None and not new_len == uncert_len:
            raise RuntimeError("value length doesn't fit uncertainty length for '%s':\n%s != %s" % (name, new_len, uncert_len))
        if not uncert_len is None:
            new_len = uncert_len


        # if quantity didn't exist
        if not name in self.data or replace:
            self.data[name] = Quantity(name)
        # if it did exist
        else:
            # get old length, len(uncert)=1 is not a length, because it can be duplicated to fit any value length
            old_len = None
            if not self.data[name].value is None:
                if isinstance(self.data[name].value, np.ndarray):
                    old_len = len(self.data[name].value)
                else:
                    old_len = 1
            if not self.data[name].uncert is None and isinstance(self.data[name].uncert, np.ndarray):
                old_len = len(self.data[name].uncert)


            # if new dimension or new length, create new quantity
            if (not self.data[name].dim == dim or
                   (not old_len is None and not new_len is None and not old_len == new_len)):
                self.data[name] = Quantity(name)

        # save stuff
        if not longname is None:
            self.data[name].longname = longname
        if not value is None:
            self.data[name].value = value
            self.data[name].value_depend = value_depend
        if not value_unit is None:
            self.data[name].value_prefUnit = value_unit
        if not uncert is None:
            self.data[name].uncert = uncert
            self.data[name].uncert_depend = uncert_depend
        if not uncert_unit is None:
            self.data[name].uncert_prefUnit = uncert_unit
        self.data[name].dim = dim



        # check if uncertainty must be duplicated to adjust to value length
        if isinstance(self.data[name].value, np.ndarray) and isinstance(self.data[name].uncert, np.float_):
            uncert_arr = np.full(len(self.data[name].value),self.data[name].uncert)
            self.data[name].uncert = uncert_arr

    def table(self, *quantities, maxcols=5, latexonly=False):
        u_sys = self.config["unit_system"]
        quants = [self[quant] for quant in quantities]
        if latexonly:
            return qtable(*quants, html=False, maxcols=maxcols, u_sys=u_sys)[0]
        else:
            return render_latex(qtable(*quants, maxcols=maxcols, u_sys=u_sys))

    def _repr_html_(self):
        u_sys = self.config["unit_system"]
        quantities = list(self.data.values())
        return qtable(*quantities, u_sys=u_sys)

    def __getitem__(self, qname):
        return parse_expr(qname, self.data)
