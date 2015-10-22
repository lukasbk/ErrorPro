class PythonCode():
	def __init__(self, code):
		self.code = code

	def execute(self, data, config, output):
		exec(self.code)
