from quantities import Quantity, parse_expr, get_dimension

class Fit():

	#TODO Support für mehr als 1-dimensionale datasets

	def __init__(self, fit_function_str, x_data_str, y_data_str, parameters_str):
		self.x_data_str = x_data_str
		self.y_data_str = y_data_str
		self.fit_function_str = fit_function_str
		self.parameters_str = parameters_str

	def execute(self, data, config, output):
		if config["fit_module"] == "scipy":
			import fit_scipy as fit_module
		elif config["fit_module"] == "gnuplot":
			import gnuplot as fit_module
		else:
			raise ValueError("no fit module called '%s'." % config["fit_module"])

		if not data[self.x_data_str]:
			raise ValueError("quantity %s doesn't exist" % self.x_data_str)
		if not data[self.y_data_str]:
			raise ValueError("quantity %s doesn't exist" % self.y_data_str)

		# get data quantities
		x_data = data[self.x_data_str]
		y_data = data[self.y_data_str]
		# parse fit function
		fit_function = parse_expr(self.fit_function_str, data)

		# check if dimension fits
		dim_func = get_dimension(fit_function)
		if not dim_func == y_data.dim:
			raise RuntimeError("dimension of fit function %s doesn't fit dimension of y-data %s" % (dim_func, y_data.dim))

		# get parameter quantities
		parameters = []
		for p in self.parameters_str:
			if not p in data:
				data[p] = Quantity(p)
			parameters.append(data[p])

		# fit
		values, uncerts = fit_module.fit(x_data, y_data, fit_function, parameters)


		# save results
		i = 0
		for p in parameters:
			p.value = values[i]
			p.value_depend = "fit"
			p.uncert = uncerts[i]
			p.uncert_depend = "fit"
			i += 1
