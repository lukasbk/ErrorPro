import plot
from quantities import parse_expr

class Plot():
	def __init__(self):
		self.expr_pairs = []
		self.show = None
		self.save = None

	def execute(self, data, config, output):

		if len(self.expr_pairs) == 0:
			raise ValueError("nothing to plot specified.")

		expr_pairs = []

		for expr_pair_str in self.expr_pairs:
			# parse expressions
			expr_pairs.append( (parse_expr(expr_pair_str[0], data), parse_expr(expr_pair_str[1], data)) )

		# standard show/save behaviour
		if self.show is None and self.save is None:
			self.show = True
		if self.show is None:
			self.show = False
		if self.save is None:
			self.save = False

		plot.plot(expr_pairs, config, show=self.show, save=self.save)
