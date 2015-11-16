from sympy import Symbol, Dummy
import sympy
#from sympy.parsing.sympy_parser import parse_expr as sym_parse_expr
from sympy import sympify
from units import convert_to_unit
from dimensions.simplifiers import dim_simplify
from sympy.utilities.lambdify import lambdify
import numpy as np

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
		if var.dim == None:
			raise RuntimeError ("quantity '%s' doesn't have a dimension, yet." % var.name)
		dim = dim.subs(var,var.dim)
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
