from sympy import Symbol
from sympy.parsing.sympy_parser import parse_expr as sym_parse_expr

def parse_expr(expr, data):
	expr=sym_parse_expr(expr,local_dict=data)
	for q in expr.free_symbols:
		if not isinstance(q,Quantity):
			raise ValueError("Symbol '%s' is not defined." % q.name)
	return expr

class Quantity(Symbol):
	def __new__(cls,name,longname):
		self = Symbol.__new__(cls, name)
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

	def __repr__(self):
		return "%s +- %s" % (self.value, self.uncert)
