from scipy.optimize import curve_fit
from sympy.utilities.lambdify import lambdify
import numpy as np

def fit(x_data, y_data, fit_function, parameters, weighted=None):

	args = [x_data]
	args.extend(parameters)
	np_func = lambdify(tuple(args), fit_function, "numpy")

	start_params = []
	for p in parameters:
		if p.value == None:
			start_params.append(np.float_(1))
		else:
			if isinstance(p.value,np.ndarray):
				raise ValueError("fit parameter '%s' is a data set." % p.name)
			else:
				start_params.append(p.value)

	if weighted is False:
		uncerts = None
	else:
		uncerts = y_data.uncert

	if weighted is True and y_data.uncert is None:
		raise RuntimeError("can't perform weighted fit because uncertainty of '%s' is not set." % y_data.name)
	params_opt, params_covar = curve_fit (np_func,x_data.value,y_data.value,sigma=uncerts,p0=start_params)
	params_err = np.sqrt(np.diag(params_covar))

	return (params_opt,params_err)
