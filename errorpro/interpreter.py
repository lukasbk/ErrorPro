from errorpro import commands
import re

def createAssignmentCommand(value, header):
	name = header.name
	if name.endswith("_err"):
		name = name[:-4]
		command = commands.Assignment(name)
		command.uncert = value
		command.uncert_unit = header.unit
		if header.uncertainty is not None:
			raise RuntimeError("Variables with _err notation cannot use the <...> notation.")
		if header.longname is not None:
			raise RuntimeError("Variables with _err notation cannot have a long name: %s"%header.longname)
	else:
		command = commands.Assignment(name)
		command.value = value
		command.longname = header.longname
		command.value_unit = header.unit
		command.uncert = header.uncertainty
		if header.uncertainty is not None:
			command.uncert_unit = header.unit
	return command

def interpret (syntacticProgram):
	"""
	returns list of commands
	"""
	program = []
	for syntacticCommand in syntacticProgram:
		if syntacticCommand.parseinfo.rule == "assignment":
			program.append(createAssignmentCommand(syntacticCommand.value, syntacticCommand))
		elif syntacticCommand.parseinfo.rule == "multi_assignment":
			# create one command for each column
			for columnIndex in range(len(syntacticCommand.header)):
				values = []
				for row in syntacticCommand.rows:
					values.append(row[columnIndex])
				header = syntacticCommand.header[columnIndex]
				program.append(createAssignmentCommand(values, header))
		elif syntacticCommand.parseinfo.rule == "python_code":
			code = '\n'.join(syntacticCommand.code)
			program.append(commands.PythonCode(code))
		elif syntacticCommand.parseinfo.rule == "function":
			if syntacticCommand.name == "fit":
				fitFunction = syntacticCommand.parameters[0]
				xData = syntacticCommand.parameters[1]
				yData = syntacticCommand.parameters[2]
				params = syntacticCommand.parameters[3]
				program.append(commands.Fit(fitFunction, xData, yData, params))
			elif syntacticCommand.name == "set":
				name = syntacticCommand.parameters[0]
				value = syntacticCommand.parameters[1]
				program.append(commands.Set(name, value))
			elif syntacticCommand.name == "meanvalue":
				name = syntacticCommand.parameters[0]
				longname = None
				reMatch = re.match('"(.*)"[ \t]+([-_\w]+)', name)
				if reMatch is not None:
					longname = reMatch.group(1)
					name = reMatch.group(2)
				quantities = syntacticCommand.parameters[1]

				command = commands.MeanValue(name)
				command.longname = longname
				command.quantities = quantities

				program.append(command)
			elif syntacticCommand.name == "plot":
				command = commands.Plot()
				command.expr_pairs = syntacticCommand.parameters[0]
				program.append(command)
			else:
				raise RuntimeError("Unknown Function '%s' " % syntacticCommand.name)
		else:
			raise RuntimeError("Unknown syntactic command type")

	return program
