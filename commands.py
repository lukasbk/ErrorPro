from commands_calculations import *
from commands_output import *
from quantities import Quantity
from units import parse_unit
import numpy as np
from sympy import N

# Sollte das so oder so ähnlich aussehen?

class Command():
	def execute(self,data,config):
		pass


class SetValue(Command):
	def __init__(self, name, longname, value, unit):
		self.name = name
		self.longname = longname
		self.value = v
		self.unit = unit
	
	def execute(self,data,config):
		factor, dim = parse_unit(self.unit)
		if not data[name]:
			data[name]=Quantity(self.name,self.longname)
			# ...
		else:
			if self.longname:
				data[name].longname=self.longname
		
		data[name].value=N(factor)*np.float_(value)

class SetUncertainty(Command):
	def __init__(self, name, value, unit, longname=""):
		self.name=name
		self.value=v
		self.uncertainty=u
	# ...