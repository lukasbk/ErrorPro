import numpy as np
from quantities import Quantity
from scipy.stats import t as student_t

# calculate student-t-factor
def get_t_factor(sample_number, confidence_interval = 0.683):
	one_sided_ci = (confidence_interval + 1) / 2
	return student_t.ppf(one_sided_ci, sample_number-1 )

class MeanValue():

	def __init__(self, quantity_to_assign):
		self.quantity_to_assign = quantity_to_assign
		self.longname = ""
		self.quantities = []
		self.tryWeighted = True

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
		weighted = self.tryWeighted
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
			mean_value = ( values / uncerts**2 ).sum() / ( 1 / uncerts**2 ).sum()
			value_depend = "standard weighted mean value"
			stat_uncert = np.sqrt(1 / (1 / uncerts**2).sum())
			uncert_depend = "standard weighted mean value error"
		else:
			mean_value = values.sum() / len(values)
			value_depend = "standard mean value"
			stat_uncert = get_t_factor(len(values)) * np.sqrt(1 / (len(values) * (len(values)-1) ) * ((values - mean_value)**2).sum() )
			uncert_depend = "standard mean value error"

		# save things
		data[self.quantity_to_assign] = Quantity(self.quantity_to_assign, self.longname)
		data[self.quantity_to_assign].value = mean_value
		data[self.quantity_to_assign].value_depend = value_depend
		data[self.quantity_to_assign].uncert = stat_uncert
		data[self.quantity_to_assign].uncert_depend = uncert_depend
		data[self.quantity_to_assign].dim = dim
