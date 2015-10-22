import commands
import re

def createAssignmentCommand(value, header):
	name = header.name
	if name.endswith("_err"):
		name = name[:-4]
		command = commands.Assignment(header.name)
		command.uncert = value
		if hasattr(header, "unit"):
			command.uncert_unit = header.unit
		if hasattr(header, "uncertainty"):
			raise RuntimeError("Variables with _err notation cannot use the <...> notation.")
		if hasattr(header, "longname"):
			raise RuntimeError("Variables with _err notation cannot have a long name.")
	else:
		command = commands.Assignment(header.name)
		command.value = value
		if hasattr(header, "longname"):
			command.longname = header.longname
		if hasattr(header, "unit"):
			command.value_unit = header.unit
		if hasattr(header, "uncertainty"):
			command.uncert = header.uncertainty
			if hasattr(header, "unit"):
				command.uncert_unit = header.unit
	return command

def interpret (syntacticProgram):
	"""
	returns list of commands
	"""
	program = []
	for syntacticCommand in syntacticProgram:
		if syntacticCommand.type == "SingleAssignment":
			program.append(createAssignmentCommand(syntacticCommand.value, syntacticCommand))
		elif syntacticCommand.type == "MultiAssignment":
			# create one command for each column
			for columnIndex in range(len(syntacticCommand.header)):
				values = []
				for row in syntacticCommand:
					values.append(row[columnIndex])
				header = syntacticCommand.header[columnIndex]
				program.append(createAssignmentCommand(values, header))
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
			elif syntacticCommand.name == "set":
				reMatch = re.match("(.*) (.*)", syntacticCommand)
				if reMatch == None:
					raise RuntimeError("Set command has wrong format: '%s'" % syntacticCommand)
				program.append(commands.Set(reMatch.group(1), reMatch.group(2)))
			else:
				raise RuntimeError("Unknown Function '%s' " % syntacticCommand.name)
		else:
			raise RuntimeError("Unknown syntactic command type")

	return program
