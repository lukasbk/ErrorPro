from scipy.optimize import curve_fit
from sympy.utilities.lambdify import lambdify
import numpy as np

def fit(func, xdata, ydata, params, weighted=True, absolute_sigma=True):
	""" fits function to data
	Args:
	- xdata: Quantity of x-axis data
	- ydata: Quantity of y-axis data
	- params: list of Quantity objects. parameters to be fitted.
	- weighted: bool. If fit should be weighted by errors or not.
	- absolute_sigma: bool. If False, uses errors only to weight data points.
					  Overall magnitude of errors doesn't affect output errors.
					  If True, estimated output errors will be based on input
					  error magnitude.
	"""

	# create fit function
	args = [xdata].extend(params)
	np_func = lambdify(tuple(args), func, "numpy")

	# list starting values
	start_params = []
	for p in params:
		if p.value == None:
			start_params.append(np.float_(1))
		else:
			if isinstance(p.value,np.ndarray):
				raise ValueError("fit parameter '%s' is a data set." % p.name)
			else:
				start_params.append(p.value)

	# weight fit
	if weighted:
		errors = ydata.error
	else:
		errors = None

	if weighted is True and ydata.error is None:
		raise RuntimeError("can't perform weighted fit because error of '%s' is not set." % ydata.name)

	# perform fit
	params_opt, params_covar = curve_fit (np_func,xdata.value, ydata.value,
				sigma=errors, p0=start_params, absolute_sigma=absolute_sigma)
	# calculate errors
	params_err = np.sqrt(np.diag(params_covar))

	return (params_opt,params_err)
