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
			command.value = syntacticCommand.value
			if hasattr(syntacticCommand, "unit"):
				command.value_unit = syntacticCommand.unit
				command.uncert_unit = syntacticCommand.unit
			if hasattr(syntacticCommand, "uncertainty"):
				command.uncert = syntacticCommand.uncertainty
			program.append(command)
		elif syntacticCommand.type == "MultiAssignment":
			# create one command for each column
			for columnIndex in range(len(syntacticCommand[0])):
				values = []
				for row in syntacticCommand:
					values.append(row[columnIndex])
				header = syntacticCommand.header[columnIndex]

				command = commands.Assignment(header.name)
				command.value = values
				if hasattr(header, "unit"):
					command.value_unit  = header.unit
					command.uncert_unit = header.unit
				if hasattr(header, "uncertainty"):
					command.uncert  = header.uncertainty
				program.append(command)
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
