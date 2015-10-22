import commands
import re

def interpret (syntacticProgram):
	"""
	returns list of commands
	"""
	program = []
	for syntacticCommand in syntacticProgram:
		if syntacticCommand.type == "SingleAssignment":
			command = commands.Assignment(syntacticCommand.name)
			command.value      = syntacticCommand.value
			command.value_unit = syntacticCommand.unit
			command.uncert     = syntacticCommand.uncertainty
			program.append(command)
		elif syntacticCommand.type == "MultiAssignment":
			#TODO
			pass
		elif syntacticCommand.type == "PythonCode":
			program.append(commands.PythonCode(syntacticCommand))
		elif syntacticCommand.type == "Function":
			if syntacticCommand.name == "fit":
				reMatch = re.match("(.*) to \((.*),(.*)\) via (.*)", syntacticCommand)
				if reMatch == None:
					raise RuntimeError("Fit command has wrong format: '%s'" % syntacticCommand)
				fitFunction = reMatch.group(1)
				xData = reMatch.group(2)
				yData = reMatch.group(3)
				params = reMatch.group(4)
				program.append(commands.Fit(fitFunction, xData, yData, params))
			else:
				raise RuntimeError("Unknown Function '%s' " % syntacticCommand.name)
		else:
			raise RuntimeError("Unknown syntactic command type")

	return program
