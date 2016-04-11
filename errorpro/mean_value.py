from numpy import *
from scipy.stats import t as student_t
import numpy as np
from errorpro.quantities import Quantity

def mean_value(quantity_to_assign, quantities, weighted, force_weighted):
	# put all values and errors into arrays
	values = np.ndarray((0),dtype=np.float_)
	errors = np.ndarray((0),dtype=np.float_)
	dim = None
	for q in quantities:
		if q.value is None:
			raise RuntimeError("quantity '%s' has no value, yet." % q.name)
		# if one error is missing, can't do weighted mean value
		if q.error is None or q.error.any()==0:
			if weighted is True:
				if force_weighted:
					raise RuntimeError("at least one error missing or zero for calculating mean value '%s'" % quantity_to_assign.name)
				else:
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
			errors = np.append(errors,q.error)

	# mean value calculation
	if weighted:
		mean_value, stat_error = standard_weighted_mean_value(values, errors)
		value_formula = "standard weighted mean value"
		error_formula = "standard weighted mean value error"
	else:
		mean_value, stat_error = standard_mean_value(values)
		value_formula = "standard mean value"
		error_formula = "standard mean value error"

	# save things
	quantity_to_assign.value = mean_value
	quantity_to_assign.value_formula = value_formula
	quantity_to_assign.error = stat_error
	quantity_to_assign.error_formula = error_formula
	quantity_to_assign.dim = dim

# calculate student-t-factor
def get_t_factor(sample_number, confidence_interval = 0.683):
	one_sided_ci = (confidence_interval + 1) / 2
	return student_t.ppf(one_sided_ci, sample_number-1 )

def standard_mean_value(values):
    values = float_(values)
    mean_value = values.sum() / len(values)
    stat_error = get_t_factor(len(values)) * sqrt(1 / (len(values) * (len(values)-1) ) * ((values - mean_value)**2).sum() )
    return (mean_value, stat_error)

def standard_weighted_mean_value(values, errors):
    values = float_(values)
    errors = float_(errors)
    mean_value = ( values / errors**2 ).sum() / ( 1 / errors**2 ).sum()
    stat_error = sqrt(1 / (1 / errors**2).sum())
    return (mean_value, stat_error)

# weighted mean value for results with very different precision, not tested
def alternate_weighted_mean_value(values, errors):
    values = float_(values)
    errors = float_(errors)
    mean_value = ( values / errors**2 ).sum() / ( 1 / errors**2 ).sum()
    stat_error = sqrt( ( (values - mean_value)**2 / errors**2).sum() / ((len(values)-1) * (1/errors**2).sum()))
    return (mean_value, stat_error)
