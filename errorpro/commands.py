
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

	def execute(self, p):

		p.assign(self.name, longname=self.longname, value=self.value, value_unit=self.value_unit, error=self.error, error_unit=self.error_unit)
