from sympy import Symbol,diff
import sympy
import numpy as np
from sympy.parsing.sympy_parser import parse_expr as sym_parse_expr
from sympy.utilities.lambdify import lambdify
from units import parse_unit, convert_to_unit, dim_simplify
from si import system as si

# TODO
# gewichtetes Mittel

def parse_expr(expr,data):
	expr=sym_parse_expr(expr,local_dict=data)
	for q in expr.free_symbols:
		if not isinstance(q,Quantity):
			raise ValueError("Symbol '%s' is not defined." % q.name)
	return expr

#only for internal use
def uncertaintyFormula(expr):
	formula=0
	for var in expr.free_symbols:
		formula+=(Symbol("{\\sigma_{"+var.name+"}}",positive=True)*diff(expr,var))**2
	return sympy.sqrt(formula)

class Quantity(Symbol):
	def __new__(cls,name,longname):
		self = Symbol.__new__(cls, name)
		self.abbrev=name
		self._name=name
		self._longname=longname
		return self
	
	def getLongname(self):
		return self._longname

	def getResult(self,unit=None,baseUnits=False):
		"""
		standard method to get value, uncertainty and unit of this quantity
		If you don't specify anything, it will try to find the best unit by itself.
		Alternatively, you can specify your own unit to convert to or demand only base units.
		Returns (value,uncertainty,unit).
		"""
		if self._value==None:
			raise RuntimeError("Value has not been calculated, yet.")
		if self._uncertainty==None:
			raise RuntimeError("Uncertainty has not been calculated, yet.")
		if self._dim==None:
			raise RuntimeError("Dimension has not been calculated, yet.")
		if not unit:
			unit=self._standardUnit
		factor,unit=convert_to_unit(self._dim,si,outputUnit=unit,onlyBase=baseUnits)
		return (self._value/np.float_(factor),self._uncertainty/np.float_(factor),unit)

	def getValue(self):
		"""
		method to get the raw value data in base units
		"""
		if self._value==None:
			raise RuntimeError("Value has not been calculated, yet.")
		return self._value
	
	def getUncertainty(self):
		"""
		method to get the raw uncertainty data in base units
		"""
		if self._uncertainty==None:
			raise RuntimeError("Uncertainty has not been calculated, yet.")
		return self._uncertainty

	def getDimension(self):
		if self._dim==None:
			raise RuntimeError("Dimension has not been calculated, yet.")
		return self._dim

	def getLength(self):
		if isinstance(self._value,np.ndarray):
			return len(self._value)
		else:
			return 1
		
class Measurement(Quantity):

	def __new__(cls, name, longname, value, uncertainty, valueUnit, uncertUnit):
		self=Quantity.__new__(cls,name,longname)
		vFactor, self._dim = parse_unit(valueUnit,si)
		uFactor, uDim = parse_unit(uncertUnit,si)
		if not self._dim == uDim:
			raise ValueError("value and uncertainty dimensions do not match\n%s\n%s" % (self._dim, uDim))
		self._standardUnit=None
		self._value=np.float_(value)*np.float_(vFactor)
		self._uncertainty=np.float_(uncertainty)*np.float_(uFactor)
		return self

class Result(Quantity):
	def __new__(cls, name, longname, term, standardUnit, data):
		self=Quantity.__new__(cls,name,longname)
		self._term=parse_expr(term,data)
		if standardUnit:
			self._standardUnit = standardUnit
		else:
			self._standardUnit = None
		self.calculate()
		return self

	def calculate(self):
		#calculate value
		calcFunction=lambdify(self._term.free_symbols,self._term)
		values=[]
		for var in self._term.free_symbols:
			values.append(var.getValue())
		self._value=calcFunction(*values)

		#calculate uncertainty
		integrand=0
		for outerVar in self._term.free_symbols:
			differential=diff(self._term,outerVar)
			diffFunction=lambdify(differential.free_symbols,differential)
			
			values=[]
			for var in differential.free_symbols:
				values.append(var.getValue())
			
			integrand+=( outerVar.getUncertainty()*diffFunction(*values) )**2

		self._uncertainty=np.sqrt(integrand)

		#calculate unit
		dim=self._term
		for var in self._term.free_symbols:
			dim=dim.subs(var,var.getDimension())
		self._dim=dim_simplify(dim)

	def getUncertaintyFormula(self):
		return uncertaintyFormula(self._term)

# TODO
# Student-t-Faktor
class UnweightedMeanValue(Result):
	def __new__(cls, name, longname, listObj):
		self=Quantity.__new__(cls,name,longname)
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
	def __new__(cls, name, longname,unit):
		self=Quantity.__new__(cls,name,longname)
		#TODO Einheiten überlegen
		self._unit=unit
		return self

	def set(self,value,uncertainty):
		self._value=value
		self._uncertainty=uncertainty
