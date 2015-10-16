from quantities import Quantity, parse_expr
from units import dim_simplify, parse_unit
from sympy import Symbol
from sympy.utilities.lambdify import lambdify
from sympy.physics.unitsystems.dimensions import Dimension
import sympy
import numpy as np

class Command():
	def execute(self,data,config):
		pass


class Assignment(Command):

	def __init__(self, name, longname=""):
		self.name = name
		self.longname = longname
		self.value = None
		self.value_unit = None
		self.uncert = None
		self.uncert_unit = None

	def execute(self, data, config):

		if not self.name in data or (self.value and self.uncert):
			data[self.name] = Quantity(self.name,self.longname)

		# if value is set
		# find out exact value, its dependency, preferred unit and dimension
		if self.value:
			value_dim = None
			value_prefUnit = None
			value_depend = None
			# parse value's unit if given
			if not self.value_unit == None:
				factor, value_dim, unit = parse_unit(self.value_unit, config["unitSystem"])

			value = parse_expr(self.value, data)
			# if it's a number
			if value.is_number:
				# if no unit given, set dimensionless
				if self.value_unit == None:
					factor = 1
					value_dim = Dimension()
				else:
					value_prefUnit = unit

				value=np.float_(factor)*np.float_(value)

			# if it's a calculation
			else:
				# calculate value from dependency
				value_depend = value
				calcFunction=lambdify(value_depend.free_symbols, value_depend)
				depValues=[]
				for var in value_depend.free_symbols:
					depValues.append(var.value)
				value = calcFunction(*depValues)

				# calculate dimension from dependency
				calculated_dim = value_depend
				for var in value_depend.free_symbols:
					calculated_dim=calculated_dim.subs(var,var.dim)
				calculated_dim = dim_simplify(calculated_dim)

				if value_dim and not value_dim == calculated_dim:
					raise ValueError ("given value dimension %s doesn't fit to dependency's dimension %s." % (value_dim, calculated_dim))
				value_dim = calculated_dim

			# save things
			data[self.name].value = value
			data[self.name].value_prefUnit = value_prefUnit
			data[self.name].value_depend = value_depend
			if data[self.name].dim and not data[self.name].dim == value_dim:
				raise ValueError ("given value dimension %s doesn't fit to quantity's former dimension %s." % (value_dim, data[self.name].dim))
			data[self.name].dim = value_dim


		# if uncertainty is set
		if self.uncert:
			uncert_prefUnit = None
			# parse uncertainty's unit if given
			if not self.uncert_unit == None:
				factor, uncert_dim, uncert_prefUnit = parse_unit(self.uncert_unit, config["unitSystem"])
			# otherwise, set dimensionless
			else:
				factor = 1
				uncert_dim = Dimension()

			# parse uncertainty
			uncert = parse_expr(self.uncert, data)
			if not uncert.is_number:
				raise ValueError("uncertainty %s is not a number." % uncert)
			uncert = np.float_(factor)*np.float_(uncert)

			# save things
			data[self.name].uncert = uncert
			if data[self.name].dim and not data[self.name].dim == uncert_dim:
				raise ValueError("given uncertainty dimension %s doesn't fit to dimension %s." % (uncert_dim, data[self.name].dim))
			data[self.name].dim = uncert_dim
			data[self.name].uncert_prefUnit = uncert_prefUnit

		# if uncertainty can be calculated from dependency
		elif value_depend:

			integrand = 0
			uncert_depend = 0
			for varToDiff in value_depend.free_symbols:
				differential = sympy.diff(value_depend,varToDiff)
				uncert_depend += ( Symbol(varToDiff.name+"_err") * differential )**2
				diffFunction = lambdify(differential.free_symbols,differential)

				diffValues = []
				for var in differential.free_symbols:
					diffValues.append(var.value)

				integrand += ( varToDiff.uncert*diffFunction(*diffValues) )**2

			data[self.name].uncert_depend = sympy.sqrt (uncert_depend)
			data[self.name].uncert = np.sqrt(integrand)


class MeanValue(Command):
	pass

class Fit(Command):
	pass

class Plot(Command):
	pass
