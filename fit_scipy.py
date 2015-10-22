from scipy.optimize import curve_fit
from sympy.utilities.lambdify import lambdify
import numpy as np

def fit(x_data, y_data, fit_function, parameters):

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

	params_opt, params_covar = curve_fit (np_func,x_data.value,y_data.value,sigma=y_data.uncert,p0=start_params)
	params_err = np.sqrt(np.diag(params_covar))

	return (params_opt,params_err)
