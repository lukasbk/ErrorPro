from numpy import *
from scipy.stats import t as student_t
import numpy as np
from errorpro.quantities import Quantity
from errorpro.exceptions import DimensionError

def mean_value(quantity_to_assign, quantities, weighted, force_weighted):
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
					raise RuntimeError("at least one uncertainty missing or zero for calculating mean value '%s'" % quantity_to_assign.name)
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
	quantity_to_assign.value = mean_value
	quantity_to_assign.value_depend = value_depend
	quantity_to_assign.uncert = stat_uncert
	quantity_to_assign.uncert_depend = uncert_depend
	quantity_to_assign.dim = dim

# calculate student-t-factor
def get_t_factor(sample_number, confidence_interval = 0.683):
	one_sided_ci = (confidence_interval + 1) / 2
	return student_t.ppf(one_sided_ci, sample_number-1 )

def standard_mean_value(values):
    values = float_(values)
    mean_value = values.sum() / len(values)
    stat_uncert = get_t_factor(len(values)) * sqrt(1 / (len(values) * (len(values)-1) ) * ((values - mean_value)**2).sum() )
    return (mean_value, stat_uncert)

def standard_weighted_mean_value(values, uncerts):
    values = float_(values)
    uncerts = float_(uncerts)
    mean_value = ( values / uncerts**2 ).sum() / ( 1 / uncerts**2 ).sum()
    stat_uncert = sqrt(1 / (1 / uncerts**2).sum())
    return (mean_value, stat_uncert)

# weighted mean value for results with very different precision, not tested
def alternate_weighted_mean_value(values, uncerts):
    values = float_(values)
    uncerts = float_(uncerts)
    mean_value = ( values / uncerts**2 ).sum() / ( 1 / uncerts**2 ).sum()
    stat_uncert = sqrt( ( (values - mean_value)**2 / uncerts**2).sum() / ((len(values)-1) * (1/uncerts**2).sum()))
    return (mean_value, stat_uncert)
