from quantities import Quantity
from units import parse_unit
import numpy as np
from sympy import N

# Sollte das so oder so ähnlich aussehen?

class Command():
	def execute(self,data,config):
		pass


class Assignment(Command):
	"""
	Attributes: name, longname, value, valueUnit, uncertainty, uncertaintyUnit
	"""
	def execute(self,data,config):
		factor, dim = parse_unit(self.unit)
		if not data[name]:
			data[name]=Quantity(self.name,self.longname)
			# ...
		else:
			if self.longname:
				data[name].longname=self.longname
		
		data[name].value=N(factor)*np.float_(value)

class Formula(Command):
	def execute():
		pass