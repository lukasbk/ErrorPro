from numpy import ndarray
from scipy.stats import t as student_t

# calculate student-t-factor
def get_t_factor(sample_number, confidence_interval = 0.683):
	one_sided_ci = (confidence_interval + 1) / 2
	return student_t.ppf(one_sided_ci, sample_number-1 )

class MeanValue():

	def __init__(self):
		self.quantities = []

	def execute(self, data, config, output):

		# get quantities
		quantities = []
		for q in self.quantities:
			if not q in data:
				raise ValueError("quantity '%s' is not defined." % q)
			quantities.append(data[q])

		# put all values and uncertainties into arrays
		values = []
		uncerts = []
		weighted = True
		dim = None
		for q in quantities:
			if q.value is None:
				raise RuntimeError("quantity '%s' has no value, yet." % q.name)
			# if one uncertainty is missing, can't do weighted mean value
			if q.uncert is None or q.uncert==0:
				weighted = False

			# check dimension
			if dim is None:
				dim = q.dim
			else:
				if not dim == q.dim:
					raise RuntimeError("quantities don't have the same dimension: %s != %s" % (dim,q.dim))

			# put into arrays
			if isinstance(q.value, ndarray):
				values.extend(q.value)
			else:
				values.append(q.value)
			if weighted:
				if isinstance(q.uncert, ndarray):
					uncerts.extend(q.uncert)
				else:
					uncerts.append(q.uncert)

		#TODO calculation
