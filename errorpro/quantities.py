from sympy import Symbol, Dummy
import sympy
#from sympy.parsing.sympy_parser import parse_expr as sym_parse_expr
from sympy import sympify, latex
from errorpro.units import convert_to_unit
from errorpro.dimensions.simplifiers import dim_simplify
from errorpro.dimensions.solvers import subs_symbols
from sympy.utilities.lambdify import lambdify
import numpy as np
from errorpro import pytex
from importlib import import_module

# parses string to expression containing quantities
def parse_expr(expr, data):
    try:
        expr=sympify(expr,locals=data)
    except(SyntaxError):
        raise SyntaxError("error parsing term '%s'" % expr)

    for q in expr.free_symbols:
        if not isinstance(q,Quantity):
            raise ValueError("Symbol '%s' is not defined." % q.name)

    return expr

# returns dimension of expression containing quantities
def get_dimension(expr):
    dim = expr
    for var in expr.free_symbols:
        if var.dim is None:
            raise RuntimeError ("quantity '%s' doesn't have a dimension, yet." % var.name)
        dim = subs_symbols(dim,{var.name:var.dim})
    return dim_simplify(dim)

# returns value and uncertainty according to unit
def adjust_to_unit (q, unit_system, prefUnit=None):
    if prefUnit is None:
        prefUnit = q.value_prefUnit
    factor, unit = convert_to_unit(q.dim, unit_system, outputUnit=prefUnit)
    factor = np.float_(factor)
    value = None if q.value is None else q.value / factor
    uncert = None if q.uncert is None else q.uncert / factor
    return (value, uncert, unit)

# returns value of expression
def get_value(expr):
    calcFunction=lambdify(expr.free_symbols, expr, modules="numpy")
    depValues=[]
    for var in expr.free_symbols:
        if var.value is None:
            raise RuntimeError ("quantity '%s' doesn't have a value, yet." % var.name)
        depValues.append(var.value)
    return calcFunction(*depValues)


# returns uncertainty and uncertainty formula
def get_uncertainty(expr):
    integrand = 0
    uncert_depend = 0
    for varToDiff in expr.free_symbols:
        if not varToDiff.uncert is None:
            differential = sympy.diff(expr,varToDiff)
            uncert_depend += ( Symbol(varToDiff.name+"_err",positive=True) * differential )**2
            diffFunction = lambdify(differential.free_symbols,differential, modules="numpy")

            diffValues = []
            for var in differential.free_symbols:
                diffValues.append(var.value)

            integrand += ( varToDiff.uncert*diffFunction(*diffValues) )**2
    if isinstance(integrand,np.ndarray):
        if (integrand==0).all():
            return (None,None)
    elif integrand == 0:
        return (None,None)

    return (np.sqrt(integrand),sympy.sqrt (uncert_depend))

class Quantity(Symbol):
    quantity_count = 0
    dummy_count = 1

    def __new__(cls,name="",longname=None):
        if name == "":
            name = "Dummy_"+str(Quantity.dummy_count)
            Quantity.dummy_count += 1
            self = Dummy.__new__(cls, name)
        else:
            self = Symbol.__new__(cls, name)

        self.count = Quantity.quantity_count
        Quantity.quantity_count += 1

        self.abbrev = name
        self.name = name
        self.longname = longname
        self.value = None
        self.value_prefUnit = None
        self.value_depend = None
        self.uncert = None
        self.uncert_prefUnit = None
        self.uncert_depend = None
        self.dim = None
        return self

    def _repr_html_(self):
        return qtable(self)



def qtable(*quantities, html=True, maxcols=5, u_sys='si'):
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
