from quantities import Quantity, parse_expr, get_dimension
from exceptions import DimensionError
import plot as plotting
from mean_value import mean_value
from parsing.parsing import parse_file, parse
from quantities import adjust_to_unit, parse_expr, get_value, get_dimension, get_uncertainty
from units import parse_unit
from sympy.physics.unitsystems.dimensions import Dimension
import interpreter
import output
from sympy import latex, Symbol, Function, Expr, S
import numpy as np
from IPython.display import Latex as render_latex
import pytex

class Project():
    def __init__(self):
        self.data = {}
        self.output = output.Output()
        # standard configuration
        self.config = {"unit_system":"si",
                       "fit_module":"scipy",
                       "directory":".",
                       "plot_module":"matplotlib",
                       "auto_csv":"results.csv",
                       "rounding":True
                       }

    def save(self):
        self.output.generate(self.data, self.config)

    def set(self, entry, value):
        """ Change entry of configuration

        Args:
            entry: configuration entry name
            value: new value to assign to entry

        Currently usable entries:
            "plot_module": "gnuplot" or "matplotlib"
            "auto_csv": filename of automatic csv results file, None if not wanted

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

    def code(self, code):
        """ parses and executes code

        Args:
            code: string of code like in data file
        """

        # parse
        syntax_tree = parse(code)

        # interpret
        commands = interpreter.interpret(syntax_tree)

        # execute
        for c in commands:
            c.execute(self)

    def table(self, *quantities_str):
        unit_system = __import__(self.config["unit_system"]).system
        cols = []
        for q_name in quantities_str:
            if not q_name in self.data:
                raise RuntimeError("quantity '%s' is not defined." % q_name)
            q = self.data[q_name]
            value, uncert, unit = adjust_to_unit(q, unit_system)
            header = (q.longname+" " if q.longname else "") + q.name + " [" + latex(unit) + "]"
            if uncert is None:
                column = [header] + pytex.align_num_list(value)
            else:
                column = [header] + pytex.format_valerr_list(value,uncert)
            cols.append(column)

        print(pytex.table_latex(cols))
        return render_latex(pytex.table_html(cols))

    def formula(self, quantity_str, adjust=True):
        """ returns uncertainty formula of quantity as latex code

        Args:
            quantity_str: name of quantity
            adjust: if True, replaces "_err" suffix by "\sigma" function and adds equals sign in front

        Return:
            latex code string of uncertainty formula
        """

        if not quantity_str in self.data:
            raise RuntimeError("quantity '%s' is not defined." % quantity_str)

        quantity = self.data[quantity_str]

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
            self.output.addLatexCode(formula)
            return formula

    def mean_value(self, quantity_to_assign_str, *quantities_str, weighted=None, longname=None):
        """ Calculates mean value of quantities and assigns it to new quantity

        Args:
            quantity_to_assign_str: name of new mean value quantity
            quantities_str: one or more names of quantities of which mean value shall be calculated
            weighted: if True, will weight mean value by uncertainties (returns error if not possible)
                      if False, will not weight mean value by uncertainties
                      if None, will try to weight mean value, but if at least one uncertainty is not given, will not weight it
            longname: description for mean value quantity
        """
        # get quantities
        quantities = []
        for q in quantities_str:
            if not q in self.data:
                raise RuntimeError("quantity '%s' is not defined." % q)
            quantities.append(self.data[q])

        # standard behaviour for "weighted"
        if weighted is True:
            force_weighted = True
        else:
            force_weighted = False
        if weighted is None:
            weighted = True

        self.data[quantity_to_assign_str] = Quantity(quantity_to_assign_str, longname)
        mean_value(self.data[quantity_to_assign_str], quantities, weighted=weighted, force_weighted=force_weighted)


    def plot(self, *expr_pairs_str, show=True, save=False, xunit=None, yunit=None):
        """ Plots data or functions

        Args:
            expr_pairs_str: one or more pair of quantity on x-axis and on y-axis. e.g. ["p","V"]
                            y-axis can also be a function. e.g. ["t", "7*exp(t/t0)"]
            show: Bool, if plot is supposed to be shown
            save: Bool, if plot is supposed to be saved to file
            xunit: unit on x-axis. if not given, will find unit on its own
            yunit: unit on y-axis. if not given, will find unit on its own
        """

        unit_system = __import__(self.config["unit_system"]).system

        if len(expr_pairs_str) == 0:#
            raise ValueError("nothing to plot specified.")

        expr_pairs = []

        for expr_pair_str in expr_pairs_str:
            # parse expressions
            expr_pairs.append( (parse_expr(expr_pair_str[0], self.data), parse_expr(expr_pair_str[1], self.data)) )

        if not xunit is None:
            xunit = parse_unit(xunit, unit_system)[2]
        if not yunit is None:
            yunit = parse_unit(yunit, unit_system)[2]

        return plotting.plot(expr_pairs, self.config, self.output, show=show, save=save, xunit=xunit, yunit=yunit)



    def fit(self, fit_function_str, xydata_str, parameters_str, weighted=None, plot=False):
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
        #TODO xydata should also allow expressions
        #TODO if parameter not set, find out dimension

        if self.config["fit_module"] == "scipy":
            import fit_scipy as fit_module
        elif self.config["fit_module"] == "gnuplot":
            import gnuplot as fit_module
        else:
            raise ValueError("no fit module called '%s'." % self.config["fit_module"])

        if not self.data[xydata_str[0]]:
            raise ValueError("quantity %s doesn't exist" % xydata_str[0])
        if not self.data[xydata_str[1]]:
            raise ValueError("quantity %s doesn't exist" % xydata_str[1])

        # get data quantities
        x_data = self.data[xydata_str[0]]
        y_data = self.data[xydata_str[1]]
        # parse fit function
        fit_function = parse_expr(fit_function_str, self.data)

        # check if dimension fits
        dim_func = get_dimension(fit_function)
        if not dim_func == y_data.dim:
            raise DimensionError("dimension of fit function %s doesn't fit dimension of y-data %s" % (dim_func, y_data.dim))

        # get parameter quantities
        parameters = []
        for p in parameters_str:
            if not p in self.data:
                self.data[p] = Quantity(p)
            parameters.append(self.data[p])

        # fit
        values, uncerts = fit_module.fit(x_data, y_data, fit_function, parameters, weighted)


        # save results
        i = 0
        for p in parameters:
            p.value = values[i]
            p.value_depend = "fit"
            p.uncert = uncerts[i]
            p.uncert_depend = "fit"
            i += 1

        # plot
        if plot:
            return plotting.plot([(x_data, y_data), (x_data, fit_function)], self.config, self.output, show=True, save=False)


    def assign(self, name, longname=None, value=None, value_unit=None, uncert=None, uncert_unit=None, replace=False):
        """ Assigns value and/or uncertainty to quantity

        Args:
            name: quantity name
            longname: description of quantity
            value: value to assign, can be expression, string, list or number
            value_unit: value unit expression or string
            uncert: uncertainty to assign, can be expression, string, list or number, but mustn't depend on other quantities
            uncert_unit: uncertainty unit expression or string
            replace: if True, will replace quantity instead of trying to keep data
        """

        unit_system = __import__(self.config["unit_system"]).system

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
                calculated_dim = get_dimension(value_depend)
                if not value_dim is None and not calculated_dim == value_dim:
                    raise DimensionError("dimension mismatch for '%s'\n%s != %s" % (name, value_dim, calculated_dim))
                elif value_dim is None:
                    value_dim = calculated_dim

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
