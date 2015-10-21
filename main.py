import sys
import parse
import interpreter
import output


data = {}
output = output.Output()
# standard configuration
config = {"unit_system":"si",
          "fit_module":"scipy",
          "plot_module":"matplotlib",
          "directory":"results",
          "auto_results":"results.ods",
          "rounding":True}

# parse
syntax_trees = []
for files in sys.argv:
    syntax_trees.append(parse.parse_file())

# interpret
commands = []
for tree in syntax_trees:
    commands.extend(interpreter.interpret(tree))

# execute
for c in commands:
    c.execute(data, config, output)

output.save()
