from sympy import Symbol,diff
import sympy
import numpy as np
from sympy.parsing.sympy_parser import parse_expr as sym_parse_expr
from sympy.utilities.lambdify import lambdify
from sympy.physics.unitsystems.simplifiers import dim_simplify
from units import parse_unit, write_as_unit
from si import system as si

# TODO
# gewichtetes Mittel

def parse_expr(expr,data):
	expr=sym_parse_expr(expr)
	for var in expr.free_symbols:
		if not (var.name in data):
			raise ValueError("Formelzeichen "+var.name+" ist nicht definiert.")
		expr=expr.subs(var,data[var.name])
	return expr

#intern: Fehlerformel
def uncertaintyFormula(expr):
	formula=0
	for var in expr.free_symbols:
		formula+=(Symbol("{\\sigma_{"+var.name+"}}",positive=True)*diff(expr,var))**2
	return sympy.sqrt(formula)

class Quantity(Symbol):
	def __new__(cls,name,description):
		self = Symbol.__new__(cls, name)
		self.abbrev=name
		self._name=name
		self._description=description
		return self
	
	def getDescription(self):
		return self._description

	def getValue(self):
		if self._value==None:
			raise RuntimeError("Wert wurde noch nicht berechnet.")
		return self._value
	
	def getUncertainty(self):
		if self._uncertainty==None:
			raise RuntimeError("Fehler wurde noch nicht berechnet.")
		return self._uncertainty

	def getDimension(self):
		if self._dim==None:
			raise RuntimeError("Dimension wurde noch nicht berechnet.")
		return self._dim

	def getUnit(self):
		if self._dim==None:
			raise RuntimeError("Einheit wurde noch nicht berechnet.")
		return write_as_unit(self._dim,si)

	def getLength(self):
		if isinstance(self._value,np.ndarray):
			return len(self._value)
		else:
			return 1
		
class Measurement(Quantity):

	def __new__(cls, name, description, value, uncertainty, unit):
		self=Quantity.__new__(cls,name,description)
		factor,self._dim=parse_unit(unit,si)

		self._value=np.float_(value)*np.float_(factor)
		self._uncertainty=np.float_(uncertainty)*np.float_(factor)
		return self

class Result(Quantity):
	def __new__(cls, name, description, term):
		self=Quantity.__new__(cls,name,description)
		self._term=term
		self.calculate()
		return self

	def calculate(self):
		#Wert berechnen
		calcFunction=lambdify(self._term.free_symbols,self._term)
		values=[]
		for var in self._term.free_symbols:
			values.append(var.getValue())
		self._value=calcFunction(*values)

		#Fehler berechnen
		integrand=0
		for outerVar in self._term.free_symbols:
			differential=diff(self._term,outerVar)
			diffFunction=lambdify(differential.free_symbols,differential)
			
			values=[]
			for var in differential.free_symbols:
				values.append(var.getValue())
			
			integrand+=( outerVar.getUncertainty()*diffFunction(*values) )**2

		self._uncertainty=np.sqrt(integrand)

		#Einheit berechnen
		dim=self._term
		for var in self._term.free_symbols:
			dim=dim.subs(var,var.getDimension())
		self._dim=dim_simplify(dim)

	def getUncertaintyFormula(self):
		return uncertaintyFormula(self._term)

# TODO
# Student-t-Faktor
class UnweightedMeanValue(Result):
	def __new__(cls, name, description, listObj):
		self=Quantity.__new__(cls,name,description)
		self._list=listObj
		self.calculate()
		return self

	def calculate(self):
		#Wert berechnen
		sum=0
		for item in self._list.getItems():
			sum+=item.getValue()
		self._value=sum/self._list.getLength()
		
		#Fehler berechnen
		sum=0
		for item in self._list.getItems():
			sum+=(item.getValue()-self._value)**2
		self._uncertainty=np.sqrt(1/self._list.getLength()/(self._list.getLength()-1)*sum)

		self._dim=self._list.getDimension()

class FitParameter(Quantity):
	def __new__(cls, name, description,unit):
		self=Quantity.__new__(cls,name,description)
		#TODO Einheiten überlegn
		self._unit=unit
		return self

	def set(self,value,uncertainty):
		self._value=value
		self._uncertainty=uncertainty
