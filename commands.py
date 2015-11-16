from quantities import Quantity, parse_expr, get_dimension, get_value, get_uncertainty
from exceptions import DimensionError
from units import parse_unit
from sympy import Symbol
from dimensions.dimensions import Dimension
import sympy
import numpy as np


class PythonCode():
	def __init__(self, code):
		self.code = code

	def execute(self, p):
		exec(self.code)

class Assignment():

	def __init__(self, name, longname=None):
		self.name = name
		self.longname = longname
		self.value = None
		self.value_unit = None
		self.uncert = None
		self.uncert_unit = None

	def execute(self, p):


		unit_system = __import__(p.config["unit_system"]).system

		if not self.name in p.data or (self.value and self.uncert):
			p.data[self.name] = Quantity(self.name,self.longname)

		# if value is set
		# find out exact value, its dependency, preferred unit and dimension
		if self.value:
			value_dim = None
			value_prefUnit = None
			value_depend = None
			# parse value's unit if given
			if not self.value_unit is None:
				factor, value_dim, unit = parse_unit(self.value_unit, unit_system)

			if isinstance(self.value,list):
				value = self.value
			else:
				value = parse_expr(self.value, p.data)

			if not self.value_unit is None:
				value_prefUnit = unit

			# if it's a number
			if isinstance(value,list) or value.is_number:

				# if no unit given, set dimensionless
				if self.value_unit is None:
					factor = 1
					value_dim = Dimension()

				value=np.float_(factor)*np.float_(value)

			# if it's a calculation
			else:
				# calculate value from dependency
				value_depend = value
				value = get_value(value_depend)

				# calculate dimension from dependency
				calculated_dim = get_dimension(value_depend)

				if value_dim and not value_dim == calculated_dim:
					raise DimensionError ("given value dimension %s doesn't fit to dependency's dimension %s." % (value_dim, calculated_dim))
				value_dim = calculated_dim

			# save things
			if not p.data[self.name].uncert is None:
				if isinstance(value, np.ndarray) or isinstance(p.data[self.name].uncert, np.ndarray):
					if not len(value) == len(p.data[self.name].uncert):
						raise RuntimeError ("length of value %s doesn't fit length of uncertainty %s" % (len(value), len(p.data[self.name].uncert)))
			p.data[self.name].value = value
			p.data[self.name].value_prefUnit = value_prefUnit
			p.data[self.name].value_depend = value_depend
			if p.data[self.name].dim and not p.data[self.name].dim == value_dim:
				raise DimensionError ("given value dimension %s doesn't fit to quantity's former dimension %s." % (value_dim, p.data[self.name].dim))
			p.data[self.name].dim = value_dim


		# if uncertainty is set
		if self.uncert:
			uncert_prefUnit = None
			# parse uncertainty's unit if given
			if not self.uncert_unit is None:
				factor, uncert_dim, uncert_prefUnit = parse_unit(self.uncert_unit, unit_system)
			# otherwise, set dimensionless
			else:
				factor = 1
				uncert_dim = Dimension()

			# parse uncertainty
			if isinstance(self.uncert, list):
				uncert = self.uncert
			else:
				uncert = parse_expr(self.uncert, p.data)
			if not isinstance(self.uncert,list) and not uncert.is_number:
				raise ValueError("uncertainty %s is not a number." % uncert)
			uncert = np.float_(factor)*np.float_(uncert)

			# save things
			if not p.data[self.name].uncert is None:
				if isinstance(uncert, np.ndarray) or isinstance(p.data[self.name].value, np.ndarray):
					if not len(uncert) == len (p.data[self.name].value):
						raise RuntimeError ("length of uncertainty %s doesn't fit length of value %s" % (len(uncert), len(p.data[self.name].value)))
			p.data[self.name].uncert = uncert
			if p.data[self.name].dim and not p.data[self.name].dim == uncert_dim:
				raise DimensionError("given uncertainty dimension %s doesn't fit to dimension %s." % (uncert_dim, p.data[self.name].dim))
			p.data[self.name].dim = uncert_dim
			p.data[self.name].uncert_prefUnit = uncert_prefUnit

		# if uncertainty can be calculated from dependency
		elif value_depend:
			p.data[self.name].uncert, p.data[self.name].uncert_depend = get_uncertainty(value_depend)

		# check if uncertainty must be duplicated to adjust to value length
		if isinstance(p.data[self.name].value, np.ndarray) and isinstance(p.data[self.name].uncert, np.float_):
			uncert_arr = np.full(len(p.data[self.name].value),p.data[self.name].uncert)
			p.data[self.name].uncert = uncert_arr
