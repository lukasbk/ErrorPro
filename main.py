import sys
from parsing.parsing import parse
import interpreter
import output
from os import path

data = {}
output = output.Output()
# standard configuration
config = {"unit_system":"si",
          "fit_module":"scipy",
          "plot_module":"matplotlib",
          "directory":".",
          "auto_results":"results.csv",
          "rounding":True
          }

if len(sys.argv) < 2:
    raise ValueError("no input file specified.")

# standard directory is dir of first interpreted file
config["directory"] = path.dirname(sys.argv[1])

# parse
syntax_trees = []
for fileName in sys.argv[1:]:
    fileHandle = open(fileName, 'r')
    syntax_trees.append(parse(fileHandle.read()))

# interpret
commands = []
for tree in syntax_trees:
    commands.extend(interpreter.interpret(tree))

# execute
for c in commands:
    c.execute(data, config, output)

# save
output.save(data, config)
