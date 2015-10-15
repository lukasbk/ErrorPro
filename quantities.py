from sympy import Symbol

class Quantity(Symbol):
	def __new__(cls,name,longname):
		self = Symbol.__new__(cls, name)
		self.abbrev=name
		self.name=name
		self.longname=longname
		return self
