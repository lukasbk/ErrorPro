class PythonCode():
	def __init__(self, code):
		self.code = code

	def execute(self, data, config, output):
		exec(self.code)

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
