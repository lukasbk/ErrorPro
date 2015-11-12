import plot
from quantities import parse_expr

class Plot():
	def __init__(self):
		self.expr_pairs = []
		self.show = True
		self.save = True
		self.xunit = None
		self.yunit = None

	def execute(self, data, config, output):
		unit_system = __import__(config["unit_system"]).system

		if len(self.expr_pairs) == 0:
			raise ValueError("nothing to plot specified.")

		expr_pairs = []

		for expr_pair_str in self.expr_pairs:
			# parse expressions
			expr_pairs.append( (parse_expr(expr_pair_str[0], data), parse_expr(expr_pair_str[1], data)) )

		if not self.xunit is None:
			self.xunit = parse_unit(self.xunit, unit_system)[2]
		if not self.yunit is None:
			self.yunit = parse_unit(self.yunit, unit_system)[2]

		plot.plot(expr_pairs, config, output, show=self.show, save=self.save, xunit=self.xunit, yunit=self.yunit)
