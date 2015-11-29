import sys
from errorpro.parsing.parsing import parse_file
from errorpro import interpreter
from errorpro import output
from os import path

data = {}
output = output.Output()
# standard configuration
config = {"unit_system":"si",
          "fit_module":"scipy",
          "plot_module":"matplotlib",
          "auto_csv":"results.csv",
          "rounding":True
          }

if len(sys.argv) < 2:
    raise ValueError("no input file specified.")

# standard directory is dir of first interpreted file
config["directory"] = path.dirname(sys.argv[1])

# parse
syntax_trees = []
for fileName in sys.argv[1:]:
    syntax_trees.append(parse_file(fileName))

# interpret
commands = []
for tree in syntax_trees:
    commands.extend(interpreter.interpret(tree))

# execute
for c in commands:
    c.execute(data, config, output)

# save
output.generate(data, config)
