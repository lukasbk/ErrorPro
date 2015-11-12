import latex

class LatexFormula():
	def __init__(self, quantities):
		self.quantities = quantities
		self.adjust = True

	def execute(self, data, config, output):
		for q in quantities:
			output.addLatexCode(latex.uncert_formula(q, self.adjust))

class Set():
	def __init__(self, entry, value):
		self.entry = entry
		self.value = value

	def execute(self, data, config, output):
		if self.value.lower() == "on" or self.value.lower() == "true":
			config[self.entry] = True
		elif self.value.lower() == "off" or self.value.lower() == "false":
			config[self.entry] = False
		else:
			config[self.entry] = self.value


class PythonCode():
	def __init__(self, code):
		self.code = code

	def execute(self, data, config, output):
		exec(self.code)

def last_figure(output):
	from matplot import Matplot
	for i in range(0, len(output.files)):
		f = output.files[ len(output.files) - i - 1 ]
		if isinstance( f, Matplot):
			return f.figure
	return None
