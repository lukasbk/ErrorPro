from quantities import Quantity
from units import parse_unit
import numpy as np
from sympy import N

class Command():
	def execute(self,data,config):
		pass


class Assignment(Command):
	"""
	Attributes: name, longname, value, valueUnit, uncertainty, uncertaintyUnit
	"""
	def execute(self,data,config):
		factor, dim = parse_unit(self.valueUnit)
		if not data[name]:
			data[name]=Quantity(self.name,self.longname)
			# ...
		#else: doesn't exist, create it

		#if value and its unit is set
			#parse value
			#calculate value
			#dependencies??
				#calculate unit
			#parse unit -> compare
		#if uncert and its unit is set
			#parse uncertainty
			#calculate uncertainty
			#parse unit -> compare
		#else
			#calculate uncertainty from value dependencies if possible


class MeanValue(Command):
	pass

class Fit(Command):
	pass

class Plot(Command):
	pass
