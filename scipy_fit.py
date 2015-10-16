from scipy.optimize import curve_fit
from sympy.utilities.lambdify import lambdify
import numpy as np

# TODO use errors of y-data

def fit(x_data, y_data, fit_function, parameters):

	args = [x_data]
	args.extend(parameters)
	np_func = lambdify(tuple(args), fit_function, "numpy")

	params_opt, params_covar = curve_fit (np_func,x_data.value,y_data.value)
	params_err = np.sqrt(np.diag(params_covar))

	return (params_opt,params_err)