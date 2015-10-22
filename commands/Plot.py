class Plot():
	def __init__(self):
		self.quantity_pairs = []
		self.plot_functions = []

	def execute(self, data, config, output):

		#TODO plot functions

		# get quantity objects and check dimension
		quantity_pairs = []
		xdim = None
		ydim = None
		for qpair_strs in self.quantity_pairs:
			x_quantity = data[qpair_strs[0]]
			y_quantity = data[qpair_strs[1]]
			if xdim:
				if not xdim == x_quantity.dim:
					raise ValueError("dimension mismatch in plotting. %s != %s" %s (xdim, x_quantity.dim))
			else:
				xdim = x_quantity.dim
			if ydim:
				if not ydim == y_quantity.dim:
					raise ValueError("dimension mismatch in plotting. %s != %s" %s (ydim, y_quantity.dim))
			else:
				ydim = y_quantity.dim
			quantity_pairs.append((x_quantity,y_quantity))


		# parse functions
		plot_functions = []
		for f in self.plot_functions:
			plot_functions.append(parse_expr(f))

		unit_system = __import__(config["unit_system"]).system

		# plot
		if config["plot_module"] == "matplotlib":
			import matplot
			matplot.plot(quantity_pairs, plot_functions, unit_system)
