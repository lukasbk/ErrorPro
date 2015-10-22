import numpy as np
from quantities import Quantity
from calculations import standard_mean_value, standard_weighted_mean_value

class MeanValue():

	def __init__(self, quantity_to_assign):
		self.quantity_to_assign = quantity_to_assign
		self.longname = ""
		self.quantities = []
		self.try_weighted = True

	def execute(self, data, config, output):

		# get quantities
		quantities = []
		for q in self.quantities:
			if not q in data:
				raise ValueError("quantity '%s' is not defined." % q)
			quantities.append(data[q])

		# put all values and uncertainties into arrays
		values = np.ndarray((0),dtype=np.float_)
		uncerts = np.ndarray((0),dtype=np.float_)
		weighted = self.try_weighted
		dim = None
		for q in quantities:
			if q.value is None:
				raise RuntimeError("quantity '%s' has no value, yet." % q.name)
			# if one uncertainty is missing, can't do weighted mean value
			if q.uncert is None or q.uncert.any()==0:
				weighted = False

			# check dimension
			if dim is None:
				dim = q.dim
			else:
				if not dim == q.dim:
					raise RuntimeError("quantities don't have the same dimension: %s != %s" % (dim,q.dim))

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
