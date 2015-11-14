from quantities import Quantity, parse_expr, get_dimension
from exceptions import DimensionError
from plot import plot
from mean_value import mean_value
from parsing.parsing import parse_file
from quantities import adjust_to_unit
import interpreter
import output
from sympy import latex, Symbol, Function
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

    def table(self, *quantities_str):
        unit_system = __import__(self.config["unit_system"]).system
        cols = []
        for q_name in quantities_str:
            if not q_name in self.data:
                raise RuntimeError("quantity '%s' is not defined." % q_name)
            q = self.data[q_name]
            value, uncert, unit = adjust_to_unit(q, unit_system)
            header = (q.longname+" " if q.longname else "") + q.name + " [" + latex(unit) + "]"
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

        return plot(expr_pairs, self.config, self.output, show=show, save=save, xunit=xunit, yunit=yunit)



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
            plot([(x_data, y_data), (x_data, fit_function)], self.config, self.output, show=False, save=True)
