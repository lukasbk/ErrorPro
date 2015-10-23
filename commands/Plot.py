import plot
from exceptions import *
from quantities import parse_expr, get_dimension, Quantity
from sympy import Dummy

class Plot():
	def __init__(self):
		self.expr_pairs = []
		self.show = None
		self.save = None

	def execute(self, data, config, output):

		if len(self.expr_pairs) == 0:
			raise ValueError("nothing to plot specified.")

		data_pairs = []
		function_pairs = []
		x_dim = None
		y_dim = None
		for expr_pair_str in self.expr_pairs:
			# parse expressions
			x = parse_expr(expr_pair_str[0], data)
			y = parse_expr(expr_pair_str[1], data)

			# check dimensions
			if x_dim is None:
				x_dim = get_dimension(x)
			else:
				if not x_dim == get_dimension(x):
					raise DimensionError("dimension mismatch\n%s != %s" % (x_dim, get_dimension(x)))
			if y_dim is None:
				y_dim = get_dimension(y)
			else:
				if not y_dim == get_dimension(y):
					raise DimensionError("dimension mismatch\n%s != %s" % (y_dim, get_dimension(y)))

			# if y contains x, it must be a function
			if len(y.find(x)) > 0:
				# check if x is only quantity or more complicated expression
				if isinstance(x,Quantity):
					function_pairs.append((x,y))
				else:
					#if it's an expression, replace by Dummy
					dummy = Dummy("x")
					function_pairs.append((dummy, y.subs(x,dummy)))
					# TODO make sure, there's nothing of x left in y
			# if it doesn't, it must be a data set
			else:
				data_pairs.append((x,y))

		# standard show/save behaviour
		if self.show is None and self.save is None:
			self.show = True
		if self.show is None:
			self.show = False
		if self.save is None:
			self.save = False

		plot.plot(data_pairs, function_pairs, (x_dim, y_dim), config, show=self.show, save=self.save)
