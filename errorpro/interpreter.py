from errorpro import commands
import re

def interpret (program, data):
	"""
	executes the program
	"""
	for command in program:
		if command.parseinfo.rule == "assignment":
			data[command.name] = assign (command.value, command.error, command.unit, command.name, command.longname)
		elif command.parseinfo.rule == "multi_assignment":
			# collect columns:
			columns = {}
			for columnIndex in range(len(command.header)):
				values = []
				for row in command.rows:
					values.append(row[columnIndex])
				columns[command.header[columnIndex].name]["header"] = command.header[columnIndex]
				columns[command.header[columnIndex].name]["values"] = values
			# pair value columns with err-columns:
			for column in columns:
				if column["header"].name.endswith("_err"):
					continue
				if column["header"].name + "_err" in columns:
					errorColumn = columns[column["header"].name + "_err"]
					if errorColumn["header"].error is not None:
						raise RuntimeError("Variables with _err notation cannot use the <...> notation:  %s"%errorColumn["header"].name)
					if errorColumn["header"].header.longname is not None:
						raise RuntimeError("Variables with _err notation cannot have a long name: %s"%errorColumn["header"].longname)
					if column["header"].error is not None:
						raise RuntimeError("Variables with a corresponding _err column cannot have a general error specified: %s"%column["header"].name)
					data[column["header"].name] = assign (column["value"], errorColumn["value"], column["header"].unit, column["header"].name, column["header"].longname, None, errorColumn["header"].unit)
				else:
					data[column["header"].name] = assign (column["value"], column["header"].error, column["header"].unit, column["header"].name, column["header"].longname)

		elif command.parseinfo.rule == "python_code":
			code = '\n'.join(command.code)
			exec (code)
		else:
			raise RuntimeError("Unknown syntactic command type")
	return data
