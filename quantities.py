from sympy import Expr,Symbol,diff,sqrt
from sympy.parsing.sympy_parser import parse_expr as sym_parse_expr
from sympy.physics.unitsystems.quantities import Quantity as symQuantity
import units
quantities={}
lists={}

#erzeugt neuen Messwert
def newMeasurement(name,value,uncertainty,unit):
	if name in lists or name in quantities:
		raise ValueError("Symbol gibt es schon.")
	value=sym_parse_expr(str(value))
	uncertainty=sym_parse_expr(str(uncertainty))
	if not (value.is_number and uncertainty.is_number):
		raise ValueError("Wert und Fehler müssen Zahlen sein")
	quantities[name]=Measurement(name,value,uncertainty,units.parse_expr(unit))
	return quantities[name]

#erzeugt neue abhängige Größe
def newResult(name,value):
	if name in lists or name in quantities:
		raise ValueError("Symbol gibt es schon.")

	expr=parse_expr(value)
	for var in expr.free_symbols:
		if not isinstance(var,Quantity):
			raise ValueError("Wert darf nur Größen enthalten.")

	quantities[name]=Result(name,expr)
	return quantities[name]

def newMeasurementList(name,values,uncertainties,unit):
	if name in lists or name in quantities:
		raise ValueError("Symbol gibt es schon.")
	if not len(values)==len(uncertainties):
		raise ValueError("Werte und Fehler sind nicht gleich viele.")

	valuesExpr=[]
	for value in values:
		value=sym_parse_expr(str(value))
		if not (value.is_number):
			raise ValueError("Wert muss eine Zahl sein.")
		valuesExpr.append(value)
	uncertExpr=[]
	for uncertainty in uncertainties:
		uncertainty=sym_parse_expr(str(uncertainty))
		if not (uncertainty.is_number):
			raise ValueError("Fehler muss eine Zahl sein.")
		uncertExpr.append(uncertainty)

	lists[name]=MeasurementList(name,valuesExpr,uncertExpr,units.parse_expr(unit))
	return lists[name]

def newResultList(name,value,length):
	if name in lists or name in quantities:
		raise ValueError("Symbol gibt es schon.")
	lists[name]=ResultList(name,parse_expr(value),length)
	return lists[name]

def newUnweightedMeanValue(name,list):
	if name in lists or name in quantities:
		raise ValueError("Symbol gibt es schon.")
	if not isinstance(list,QuantityList):
		raise TypeError("Es muss ein Listen-Objekt übergeben werden.")
	quantities[name]=UnweightedMeanValue(name,list)
	return quantities[name]

def parse_expr(expr):
	expr=sym_parse_expr(expr)
	for var in expr.free_symbols:
		if not (var.name in quantities or var.name in lists):
			raise ValueError("Ausdruck enthält Symbole, die nicht definiert sind.")
		elif var.name in quantities:
			expr=expr.subs(var,quantities[var.name])
		else:
			expr=expr.subs(var,lists[var.name])
	return expr

#gibt Quantity-Objekt zurück
def getQuantity(sym):
	if isinstance(sym,str):
		name=sym
	else:
		raise TypeError
	if name in quantities:
		return quantities[name]
	else:
		raise ValueError("Diese Größe gibt es nicht.")

#intern: Fehlerformel
def uncertaintyFormula(expr):
	formula=0
	for var in expr.free_symbols:
		formula+=(Symbol("\\sigma_{"+var.name+"}",positive=True)*diff(expr,var))**2
	return sqrt(formula)

class Quantity(Symbol):
	def __new__(cls,name):
		self = Symbol.__new__(cls, name)
		self.abbrev=name
		self._name=name
		return self
	
	#berechnet Größe durch rekursives Einsetzen
	def calculate(self):
		pass
	
	#berechnet Fehler durch rekursives Einsetzen
	def calculateUncertainty(self):
		pass
		
class Measurement(Quantity):

	def __new__(cls, name, value, uncertainty, unit):
		self=Quantity.__new__(cls,name)
		self._value=symQuantity(value,unit)
		self._uncertainty=symQuantity(uncertainty,unit)
		return self

	def calculate(self):
		return self._value

	def calculateUncertainty(self):
		return self._uncertainty

class Result(Quantity):
	def __new__(cls, name, value):
		self=Quantity.__new__(cls,name)
		self._value=value
		return self

	def calculate(self):
		calculation=self._value
		for var in self._value.free_symbols:
			calculation=calculation.subs(var,var.calculate())
		return calculation
	def calculateUncertainty(self):
		integrand=0
		for var in self._value.free_symbols:
			#Ableitung ausrechnen
			result=diff(self._value,var)
			for var in result.free_symbols:
				result=result.subs(var,var.calculate())

			integrand+=( var.calculateUncertainty()
						*result )**2
		return sqrt(integrand)

	def getUncertaintyFormula(self):
		return uncertaintyFormula(self._value)

class UnweightedMeanValue(Result):
	def __new__(cls, name, listObj):
		self=Quantity.__new__(cls,name)
		self._list=listObj
		return self

	def calculate(self):
		sum=0
		for item in self._list.getItems():
			sum+=item.calculate()
		return sum/self._list.getLength()
		
	def calculateUncertainty(self):
		value=self.calculate()
		sum=0
		for item in self._list.getItems():
			sum+=(item.calculate()-value)**2
		#todo: t-Faktor muss hier noch rein
		return sqrt(1/self._list.getLength()/(self._list.getLength()-1)*sum)


class QuantityList(Symbol):
	def __new__(cls,name):
		self = Symbol.__new__(cls, name)
		self.abbrev=name
		self._name=name
		return self
	
	def getLength(self):
		return self._length
	def getItem(self,no):
		return self._items[no]
	def getItems(self):
		return self._items

class MeasurementList(QuantityList):
	def __new__(cls, name, value, uncertainty, unit):
		self=QuantityList.__new__(cls,name)
		self._length=0
		self._items=[]
		self._unit=unit
		for index, valueItem in enumerate(value):
			self._length+=1
			itemName=name+"_item_"+str(index)
			if itemName in quantities:
				raise ValueError("Größe mit diesem Item-Namen gibt es schon.")
			quantities[itemName]=Measurement(itemName,valueItem,uncertainty[index],unit)
			self._items.append(quantities[itemName])
		return self
	

class ResultList(QuantityList):
	def __new__(cls, name, value, length):
		self=QuantityList.__new__(cls,name)
		
		self._items=[]
		for i in range(0,length):
			resultValue=value
			for var in value.free_symbols:
				if isinstance(var,QuantityList):
					resultValue=resultValue.subs(var,var.getItem(i))
			itemName=name+"_item_"+str(i)
			if itemName in quantities:
				raise ValueError("Größe mit diesem Item-Namen gibt es schon.")
			quantities[itemName]=Result(itemName,resultValue)
			self._items.append(quantities[itemName])
		self._length=length
		self._value=value

		return self

	def getUncertaintyFormula(self):
		return uncertaintyFormula(self._value)
