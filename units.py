from sympy import Expr,Symbol
from sympy.core.mul import Mul
from sympy.parsing.sympy_parser import parse_expr as sym_parse_expr

# TODO
# Einheitensystem neu machen
# Momentan addieren sich "3 m + 3 m" zu "6 2m"
# Entweder muss das ausgebessert werden oder das sympy-Paket unitsystems benutzt werden (siehe Branch newUnits)

# TODO
# SI-System implementieren

# TODO
# M,m,k,mikro als Vorfaktoren

units={}

def makeUnit(name,dependency=False,inOutput=True):
	if not isinstance(name,str):
		raise TypeError("Einheitenname muss ein String sein.")
	if not (dependency==False or isinstance(dependency,str)):
		raise TypeError("Abhängigkeit der Einheit muss als String angegeben werden.")
	if name in units:
		raise ValueError("Einheit gibt es schon.")
	if dependency==False:
		units[name]=BaseUnit(name,inOutput=inOutput)
	else:
		units[name]=DerivedUnit(name,parse_expr(dependency),inOutput=inOutput)

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
#TODO Diese Funktion verbessern
def clearUnits(expr):
	result=expr

	#Einheiten expandieren
	for unit in expr.free_symbols:
		result=result.subs(unit,unit.expandUnits())

	result=simplifyUnits(result)

	#Einheiten nach Komplexität ordnen
	unitList=[]
	for key in units:
		unitList.append(units[key])
	sortedList=sorted(unitList,key=lambda u: -u.getComplexity())

	#Einheiten nach Komplexitätsstufe einsetzen
	for unit in sortedList:
		if unit.inOutput():
			result=result.subs(unit.expandUnits(),unit)			

	return result

def simplifyUnits(expr):
	newArgs=[]
	for arg in expr.args:
		if not (expr.func==Mul and arg.is_number):
			newArgs.append(arg)
	return expr.func(*newArgs)

def parse_expr(exprStr):
	expr=sym_parse_expr(exprStr)
	for var in expr.free_symbols:
		if not var.name in units:
			raise ValueError("Einheit "+var.name+" gibt es nicht.")
		expr=expr.subs(var,units[var.name])
	return expr

class Unit(Symbol):

	def __new__(cls,name,inOutput):
		self = Symbol.__new__(cls, name, positive=True)
		self.abbrev=name
		self._name=name
		self._inOutput=inOutput
		return self

	def inOutput(self):
		return self._inOutput

	def getComplexity(self):
		return self._complexity
	#gibt Einheit in Grundeinheiten an
	def expandUnits(self):
		pass

class BaseUnit(Unit):
	def __new__(cls, name,  inOutput):
		self=Unit.__new__(cls,name,inOutput)
		self._complexity=1
		return self
	def expandUnits(self):
		return self

class DerivedUnit(Unit):
	def __new__(cls, name, dependency, inOutput):
		self=Unit.__new__(cls,name,inOutput)
		self._dependency=dependency
		expanded=self.expandUnits()
		self._complexity=0
		for var in expanded.free_symbols:
			self._complexity+=abs(expanded.as_coeff_exponent(var)[1])

		return self

	def expandUnits(self):
		result=self._dependency
		for unit in self._dependency.free_symbols:
			result=result.subs(unit,getUnit(unit).expandUnits())
		return result

makeUnit("m")
makeUnit("s")
makeUnit("A")
makeUnit("mol")
makeUnit("cd")
makeUnit("kg")
makeUnit("K")

makeUnit("mA","A/1000",inOutput=False)
makeUnit("mm","m/1000",inOutput=False)
makeUnit("Hz","1/s",inOutput=False)
#Newton
makeUnit("Pa","kg/m/s**2")
makeUnit("J","m**2*kg/s**2")
makeUnit("W","m**2*kg/s**3")
makeUnit("C","s*A")
makeUnit("V","m**2*kg/s**3/A")
makeUnit("F","s**4*A**2/m**2/kg")
makeUnit("ohm","m**2*kg/s**3/A**2")