from errorpro import interpreter, mean_value, output, plotting, pytex, quantities, units
from errorpro.parsing.parsing import parse, parse_file
from errorpro.dimensions.dimensions import Dimension
from errorpro.dimensions.solvers import dim_solve
from sympy import latex, Symbol, Function, Expr, S, sympify
import numpy as np
from IPython.display import Latex as render_latex
from importlib import import_module

class Project():
    def __init__(self):
        self.data = {}
        # standard configuration
        self.config = {"fit_module":"scipy",
                       "directory":".",
                       "plot_module":"matplotlib",
                       "auto_csv":"results.csv",
                       "rounding":True
                       }

    def save(self):
        """ saves data to csv file
        """
        unit_system = import_module(
            "errorpro." + self.config["unit_system"]).system
        if not self.config["auto_csv"] is None or self.config["auto_csv"]=="":
            output.save_as_csv(self.data, unit_system, self.config["auto_csv"])

        # TODO automatic error formulas file

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
        """ returns error formula of quantity as latex code

        Args:
            quantity: name of quantity or Quantity object
            adjust: if True, replaces "_err" suffix by "\sigma" function and adds equals sign in front

        Return:
            latex code string of error formula
        """

        quantity = quantities.parse_expr(quantity, self.data)
        assert isinstance(quantity, quantities.Quantity)

        if quantity.error_formula is None:
            raise ValueError("quantity '%s' doesn't have an error formula.")

        formula = quantity.error_formula
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

    def mean_value(self, quantity_to_assign, *quants, weighted=None, longname=None):
        """ Calculates mean value of quantities and assigns it to new quantity

        Args:
            quantity_to_assign: name or quantity object of new mean value
            quantities: one or more quantities names or objects of which mean value shall be calculated
            weighted: if True, will weight mean value by errors (returns error if not possible)
                      if False, will not weight mean value by errors
                      if None, will try to weight mean value, but if at least one error is not given, will not weight it
            longname: description for mean value quantity
        """
        # get quantities
        quantities_obj = []
        for q in quants:
            q_obj = quantities.parse_expr(q, self.data)
            assert isinstance(q_obj, quantities.Quantity)
            quantities_obj.append(q_obj)

        if isinstance(quantity_to_assign, str):
            name = quantity_to_assign
        elif isinstance(quantity_to_assign, quantities.Quantity):
            name = quantity_to_assign.name
        quantity_to_assign = quantities.Quantity(name, longname)
        self.data[name] = quantity_to_assign

        # standard behaviour for "weighted"
        if weighted is True:
            force_weighted = True
        else:
            force_weighted = False
        if weighted is None:
            weighted = True

        mean_value.mean_value(quantity_to_assign, quantities_obj, weighted=weighted, force_weighted=force_weighted)


    def plot(self, *expr_pairs, save=None, xunit=None, yunit=None, xrange=None, yrange=None, ignore_dim=False):
        """ Plots data or functions

        Args:
            expr_pairs: one or more pair of quantity on x-axis and on y-axis. e.g. ["p","V"]
                        y-axis can also be a function. e.g. ["t", "7*exp(t/t0)"]
            save: string of file name without extension. if specified, plot will be saved to '<save>.png'
            xunit: unit on x-axis. if not given, will find unit on its own
            yunit: unit on y-axis. if not given, will find unit on its own
            xrange: pair of x-axis range, e.g. [-5,10]
            yrange: pair of y-axis range
            ignore_dim: if True, will skip dimension check
        """

        if len(expr_pairs) == 0:#
            raise ValueError("nothing to plot specified.")

        expr_pairs_obj = []

        for expr_pair in expr_pairs:
            # parse expressions
            expr_pairs_obj.append( (quantities.parse_expr(expr_pair[0], self.data), quantities.parse_expr(expr_pair[1], self.data)) )

        if not xunit is None:
            xunit = units.parse_unit(xunit)[2]
        if not yunit is None:
            yunit = units.parse_unit(yunit)[2]
        if not xrange is None:
            xrange = [quantities.get_value(quantities.parse_expr(xrange[0], self.data)),
                      quantities.get_value(quantities.parse_expr(xrange[1], self.data))]
        if not yrange is None:
            yrange = [quantities.get_value(quantities.parse_expr(yrange[0], self.data)),
                      quantities.get_value(quantities.parse_expr(yrange[1], self.data))]
        return plotting.plot(expr_pairs_obj, self.config, save=save, xunit=xunit, yunit=yunit, xrange=xrange, yrange=yrange, ignore_dim=ignore_dim)



    def fit(self, fit_function, xydata, parameters, weighted=None, plot=False, ignore_dim=False):
        """ fits function to data

        Args:
            fit_function: function to fit, e.g. "n*t**2 + m*t + b"
            xydata: pair of x-quantity and y-quantity of data to fit to, e.g. ["t","U"]
            parameters: list of parameters in fit function, e.g. ["n","m","b"]
            weighted: if True, will weight fit by errors (returns error if not possible)
                      if False, will not weight fit by errors
                      if None, will try to weight fit, but if at least one error is not given, will not weight it
            plot: Bool, if data and fit function should be plotted
            ignore_dim: if True, will ignore dimensions and just calculate in base units instead
        """


        if self.config["fit_module"] == "scipy":
            import errorpro.fit_scipy as fit_module
        else:
            raise ValueError("no fit module called '%s'." % self.config["fit_module"])

        # get parameter quantities
        parameters_obj = []
        for p in parameters:
            if isinstance(p, str):
                if not p in self.data:
                    self.data[p] = quantities.Quantity(p)
                    self.data[p].dim = Dimension()
                parameters_obj.append(self.data[p])
            elif isinstance(p, quantities.Quantity):
                parameters_obj.append(p)
            else:
                raise TypeError("parameters can only be strings or Quantity objects")

        # parse fit function
        fit_function = quantities.parse_expr(fit_function, self.data)

        # get data quantities
        x_data = quantities.parse_expr(xydata[0], self.data)
        # if x-data is an expression
        if not isinstance(x_data, quantities.Quantity):
            dummy = quantities.Quantity()
            fit_function = fit_function.subs(x_data,dummy)
            dummy.value = quantities.get_value(x_data)
            dummy.error = quantities.get_error(x_data)[0]
            dummy.dim = quantities.get_dimension(x_data)
            x_data = dummy
        y_data = quantities.parse_expr(xydata[1], self.data)
        # if y-data is an expression
        if not isinstance(y_data, quantities.Quantity):
            dummy = quantities.Quantity()
            dummy.value = quantities.get_value(y_data)
            dummy.error = quantities.get_error(y_data)[0]
            dummy.dim = quantities.get_dimension(y_data)
            y_data = dummy

        # check if dimension fits
        if not ignore_dim:
            try:
                dim_func = quantities.get_dimension(fit_function)
            except ValueError:
                dim_func = None
            if not dim_func == y_data.dim:
                # try to solve for dimensionless parameters
                known_dimensions = {x_data.name: x_data.dim}
                known_dimensions = dim_solve(fit_function, y_data.dim, known_dimensions)
                for q_name in known_dimensions:
                    if q_name in self.data:
                        if not self.data[q_name].dim == known_dimensions[q_name]:
                            self.data[q_name].dim = known_dimensions[q_name]
                            self.data[q_name].prefer_unit = None
                dim_func = quantities.get_dimension(fit_function)
                # if it still doesn't work, raise error
                if not dim_func == y_data.dim:
                    raise RuntimeError("Finding dimensions of fit parameters was not sucessful.\n"\
                                                     "Check fit function or specify parameter units manually.\n"\
                                                     "This error will occur until dimensions are right.")

        # fit
        values, errors = fit_module.fit(x_data, y_data, fit_function, parameters_obj, weighted)


        # save results
        i = 0
        for p in parameters_obj:
            p.value = values[i]
            p.value_formula = "fit"
            p.error = errors[i]
            p.error_formula = "fit"
            i += 1

        # plot
        if plot:
            return plotting.plot([(x_data, y_data), (x_data, fit_function)], self.config, ignore_dim=ignore_dim)
        else:
            return self.table(*parameters_obj)

    def concat(self, new_name, *quants, longname=""):
        """ concatenates quantities

        Args:
            new_name: name of new quantity
            quants: quantities to be concatenated
        """

        values=[]
        errors=[]

        dim = None

        for q_str in quants:
            q = quantities.parse_expr(q_str, self.data)
            # check dimension
            if dim is None:
                dim = q.dim
            else:
                if not dim==q.dim:
                    raise RuntimeError("dimension mismatch\n%s != %s" % (dim,q.dim))

            # check if values or errors are None
            if not values is None:
                if q.value is None:
                    values = None
                else:
                    v= q.value
                    if not isinstance(q.value,np.ndarray):
                        v = v.reshape((1))
                    values.append(v)
            if not errors is None:
                if q.error is None:
                    errors = None
                else:
                    u = q.error
                    if not isinstance(q.error, np.ndarray):
                        u = u.reshape((1))
                    errors.append(u)
        # concatenate
        new_value = None
        new_error = None
        if not values is None:
            new_value = np.concatenate(values)
        if not errors is None:
            new_error = np.concatenate(errors)
        if new_value is None and new_error is None:
            raise RuntimeError("Could not concatenate. At least one value and one error are None.")

        new_q = quantities.Quantity(new_name, longname)
        new_q.value = new_value
        new_q.error = new_error
        new_q.dim = dim
        self.data[new_name] = new_q

    def slice(self, new_name, quantity, start=0, end=None, longname=""):
        """ creates new quantity from data set that only contains values from start to end

        Args:
            new_name: name of new quantity
            quantity: name of quantity to be sliced
            start: number of value in data set where new quantity is supposed to start
                   first value is 0
            end: number of value to be the first one not taken into the new quantity
                 None to get all values until the end
            longname: long name of new quantity
        """

        q = quantities.parse_expr(quantity, self.data)

        new_value = None
        new_uncert = None
        # check if values or uncerts are None
        if not q.value is None:
            if not isinstance(q.value, np.ndarray):
                raise RuntimeError("Could not slice '%s'. It's not a data set." % quantity)
            if end is None:
                new_value = q.value[start:]
            else:
                new_value = q.value[start:end]
        if not q.uncert is None:
            if not isinstance(q.value, np.ndarray):
                raise RuntimeError("Could not slice '%s'. Uncertainty is not an array." % quantity)
            if end is None:
                new_uncert = q.uncert[start:]
            else:
                new_uncert = q.uncert[start:end]


        new_q = quantities.Quantity(new_name, longname)
        new_q.value = new_value
        new_q.uncert = new_uncert
        new_q.dim = q.dim
        self.data[new_name] = new_q


    def assign(self, name, value=None, error=None, unit=None, longname=None, value_unit=None, error_unit=None, replace=False, ignore_dim=False):
        """ Assigns value and/or error to quantity

        Args:
            name: quantity name
            longname: description of quantity
            value: value to assign, can be expression, string, list or number
            error: error to assign, can be expression, string, list or number, but mustn't depend on other quantities
            unit: unit of both value and error, replaces 'value_unit' and 'error_unit' if given
            value_unit: value unit expression or string
            error_unit: error unit expression or string
            replace: if True, will replace quantity instead of trying to keep data
            ignore_dim: if True, will ignore calculated dimension and use given unit instead
        """

        if not unit is None:
            value_unit = unit
            error_unit = unit

        if value is None and error is None:
            raise ValueError("At least either value or error must be specified.")

        value_len = None
        value_dim = None
        value_formula = None
        error_len = None
        error_dim = None
        error_formula = None

        # if value is given
        if not value is None:

            # parse unit if given
            if not value_unit is None:
                factor, value_dim, value_unit = units.parse_unit(value_unit)

            # parse value
            if isinstance(value, list) or isinstance(value, tuple):
                # if it's a list, parse each element
                parsed_list = []
                for v in value:
                    parsed_list.append(quantities.parse_expr(v, self.data))
            elif isinstance(value, str) or isinstance(value, Expr):
                # if it's not a list, parse once
                value = quantities.parse_expr(value, self.data)

            # if it's a calculation
            if isinstance(value, Expr) and not value.is_number:
                # calculate value from dependency
                value_formula = value
                value = quantities.get_value(value_formula)

                # calculate dimension from dependency
                if not ignore_dim:
                    calculated_dim = quantities.get_dimension(value_formula)
                    if not value_dim is None and not calculated_dim == value_dim:
                        raise RuntimeError("dimension mismatch for '%s'\n%s != %s" % (name, value_dim, calculated_dim))
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


        # if error is given
        if not error is None:

            # parse unit if given
            if not error_unit is None:
                factor, error_dim, error_unit = units.parse_unit(error_unit)

            # parse value
            if isinstance(error, list) or isinstance(error, tuple):
                # if it's a list, parse each element
                parsed_list = []
                for u in error:
                    parsed_list.append(quantities.parse_expr(u, self.data))
            elif isinstance(error, str) or isinstance(error, Expr):
                # if it's not a list, parse once
                error = quantities.parse_expr(error, self.data)

            # make sure error is a number
            if isinstance(error, Expr) and not error.is_number:
                raise RuntimeError("error '%s' is not a number" % error)

            # if no unit given, set dimensionless
            if error_unit is None:
                factor = 1
                error_dim = Dimension()
                error_unit = S.One

            error=np.float_(factor)*np.float_(error)

            # calculate error length, ignore len(error)==1 because it can be duplicated to fit any value length
            if isinstance(error,np.ndarray):
                error_len = len(error)

        # if error can be calculated
        elif not value_formula is None:
            error, error_formula = quantities.get_error(value_formula)


        # merge dimensions
        dim = value_dim
        if not dim is None and not error_dim is None and not dim == error_dim:
            raise RuntimeError("value dimension and error dimension are not the same\n%s != %s" % (dim, error_dim))
        if not error_dim is None:
            dim = error_dim

        # merge lengths
        new_len = value_len
        if not new_len is None and not error_len is None and not new_len == error_len:
            raise RuntimeError("value length doesn't fit error length for '%s':\n%s != %s" % (name, new_len, error_len))
        if not error_len is None:
            new_len = error_len


        # if quantity didn't exist
        if not name in self.data or replace:
            self.data[name] = quantities.Quantity(name)
        # if it did exist
        else:
            # get old length, len(error)=1 is not a length, because it can be duplicated to fit any value length
            old_len = None
            if not self.data[name].value is None:
                if isinstance(self.data[name].value, np.ndarray):
                    old_len = len(self.data[name].value)
                else:
                    old_len = 1
            if not self.data[name].error is None and isinstance(self.data[name].error, np.ndarray):
                old_len = len(self.data[name].error)


            # if new dimension or new length, create new quantity
            if (not self.data[name].dim == dim or
                   (not old_len is None and not new_len is None and not old_len == new_len)):
                self.data[name] = quantities.Quantity(name)

        # save stuff
        if not longname is None:
            self.data[name].longname = longname
        if not value is None:
            self.data[name].value = value
            self.data[name].value_formula = value_formula
        if not value_unit is None:
            self.data[name].prefer_unit = value_unit
        elif not error_unit is None:
            self.data[name].prefer_unit = error_unit
        if not error is None:
            self.data[name].error = error
            self.data[name].error_formula = error_formula
        self.data[name].dim = dim



        # check if error must be duplicated to adjust to value length
        if isinstance(self.data[name].value, np.ndarray) and isinstance(self.data[name].error, np.float_):
            error_arr = np.full(len(self.data[name].value),self.data[name].error)
            self.data[name].error = error_arr

    def table(self, *quants, maxcols=5, latexonly=False):
        quants = [self[quant] for quant in quants]
        if latexonly:
            return quantities.qtable(*quants, html=False, maxcols=maxcols)[0]
        else:
            return render_latex(quantities.qtable(*quants, maxcols=maxcols))

    def _repr_html_(self):
        quantities = list(self.data.values())
        return quantities.qtable(*quantities)

    def __getitem__(self, qname):
        return quantities.parse_expr(qname, self.data)
