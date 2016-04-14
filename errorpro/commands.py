from errorpro.core import assign
from quantities import parse_expr

class PythonCode():
	def __init__(self, code):
		self.code = code

	def execute(self, p):
		exec(self.code)

class Assignment():

	def __init__(self, name, longname=None):
		self.name = name
		self.longname = longname
		self.value = None
		self.value_unit = None
		self.error = None
		self.error_unit = None

	def execute(self, namespace):
		if self.value is not None:
		 	self.value = parse_expr(self.value, namespace)
		if self.error is not None:
		 	self.error = parse_expr(self.error, namespace)


		namespace[self.name] = assign(self.value, error=self.error,\
					name=self.name, longname=self.longname,\
					value_unit=self.value_unit, error_unit=self.error_unit)
