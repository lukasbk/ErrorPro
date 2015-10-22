from numpy import *
from scipy.stats import t as student_t

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
