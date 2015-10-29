import numpy as np
from quantities import Quantity
from exceptions import DimensionError
from calculations import standard_mean_value, standard_weighted_mean_value

class MeanValue():

	def __init__(self, quantity_to_assign):
		self.quantity_to_assign = quantity_to_assign
		self.longname = ""
		self.quantities = []
		self.weighted = None

	def execute(self, data, config, output):

		# get quantities
		quantities = []
		for q in self.quantities:
			if not q in data:
				raise ValueError("quantity '%s' is not defined." % q)
			quantities.append(data[q])

		if self.weighted is False:
			weighted = False
		else:
			weighted = True
			if self.weighted is True:
				force_weighted = True
			else:
				force_weighted = False

		# put all values and uncertainties into arrays
		values = np.ndarray((0),dtype=np.float_)
		uncerts = np.ndarray((0),dtype=np.float_)
		dim = None
		for q in quantities:
			if q.value is None:
				raise RuntimeError("quantity '%s' has no value, yet." % q.name)
			# if one uncertainty is missing, can't do weighted mean value
			if q.uncert is None or q.uncert.any()==0:
				if weighted is True:
					if force_weighted:
						raise RuntimeError("at least one uncertainty missing or zero for calculating mean value '%s'" % self.quantity_to_assign.name)
					else:
						weighted = False

			# check dimension
			if dim is None:
				dim = q.dim
			else:
				if not dim == q.dim:
					raise DimensionError("quantities don't have the same dimension: %s != %s" % (dim,q.dim))

			# put into arrays
			values = np.append(values, q.value)
			if weighted:
				uncerts = np.append(uncerts,q.uncert)

		# mean value calculation
		if weighted:
			mean_value, stat_uncert = standard_weighted_mean_value(values, uncerts)
			value_depend = "standard weighted mean value"
			uncert_depend = "standard weighted mean value error"
		else:
			mean_value, stat_uncert = standard_mean_value(values)
			value_depend = "standard mean value"
			uncert_depend = "standard mean value error"

		# save things
		data[self.quantity_to_assign] = Quantity(self.quantity_to_assign, self.longname)
		data[self.quantity_to_assign].value = mean_value
		data[self.quantity_to_assign].value_depend = value_depend
		data[self.quantity_to_assign].uncert = stat_uncert
		data[self.quantity_to_assign].uncert_depend = uncert_depend
		data[self.quantity_to_assign].dim = dim
