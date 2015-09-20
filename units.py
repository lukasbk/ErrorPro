from si import system as si
from sympy.physics.unitsystems.simplifiers import qsimplify
from sympy.parsing.sympy_parser import parse_expr as sym_parse_expr
from sympy.physics.unitsystems.quantities import Quantity as symQuantity

def parse_expr(exprStr):
	expr=sym_parse_expr(exprStr)
	for var in expr.free_symbols:
		if not var.name.isalpha():
			raise ValueError("Einheit besteht nicht aus Buchstaben.")
		
		unit=si.get_unit(var.name)
		if unit == None:
			raise ValueError("Einheit gibt es nicht.")
		expr=expr.subs(var,unit)
	expr=qsimplify(expr)
	if isinstance(expr,symQuantity):
		expr=expr.as_unit
	return expr