from sympy import Expr,Symbol
from sympy.parsing.sympy_parser import parse_expr as sym_parse_expr

units={} #NEU MACHEN!!!

def makeUnit(name,dependency=False):
	if not isinstance(name,str):
		raise TypeError("Einheitenname muss ein String sein.")
	if not (dependency==False or isinstance(dependency,str)):
		raise TypeError("Abhängigkeit der Einheit muss als String angegeben werden.")
	if name in units:
		raise ValueError("Einheit gibt es schon.")
	if dependency==False:
		units[name]=BaseUnit(name)
	else:
		units[name]=DerivedUnit(name,parse_expr(dependency))

#gibt Einheitenobjekt zurück
def getUnit(sym):
	if isinstance(sym,Symbol):
		name=sym.name
	elif isinstance(sym,str):
		name=sym
	else:
		raise TypeError
	if name in units:
		return units[name]
	else:
		raise ValueError("Diese Einheit gibt es nicht.")

#bringt Einheiten in eine schönere Form
def clearUnits(expr):
	result=expr

	#Einheiten expandieren
	for unit in expr.free_symbols:
		result=result.subs(unit,unit.expand())

	#Einheiten nach Komplexität ordnen
	unitList=[]
	for key in units:
		unitList.append(units[key])
	sortedList=sorted(unitList,key=lambda u: -u.getComplexity())

	#Einheiten nach Komplexitätsstufe einsetzen
	for unit in sortedList:
		result=result.subs(unit.expand(),unit)

	return result

def parse_expr(exprStr):
	expr=sym_parse_expr(exprStr)
	for var in expr.free_symbols:
		if not var.name in units:
			raise ValueError("Einheit gibt es nicht.")
		expr=expr.subs(var,units[var.name])
	return expr

class Unit(Symbol):

	def __new__(cls,name):
		self = Symbol.__new__(cls, name, positive=True)
		self.abbrev=name
		self._name=name
		return self

	def getComplexity(self):
		return self._complexity
	#gibt Einheit in Grundeinheiten an
	def expand(self):
		pass

class BaseUnit(Unit):
	def __new__(cls, name,  **assumptions):
		self=Unit.__new__(cls,name)
		self._complexity=1
		return self
	def expand(self):
		return self

class DerivedUnit(Unit):
	def __new__(cls, name, dependency, **assumptions):
		self=Unit.__new__(cls,name)
		self._dependency=dependency
		self._complexity=len(dependency.free_symbols)

		return self

	def expand(self):
		result=self._dependency
		for unit in self._dependency.free_symbols:
			result=result.subs(unit,getUnit(unit).expand())
		return result
