import unittest
from errorpro.parsing.parsing import parse
from errorpro import interpreter
import io

class InterpreterTestCase(unittest.TestCase):
    def test_pythoncode_combi(self):
        ns = {"a":1}
        a=(">a+=1\n"+
           ">a+=1\n"+
           "b=3")
        ast = parse(a)
        program = interpreter.interpret(ast, ns)
        self.assertEqual(ns["a"], 3)
        self.assertEqual(ns["b"].value, 3)

    def test_example(self):
        a=("\n#bla\n" +
          "{\n" +
          "Zeit t <0.1> [s], Höhe h [m], h_err [dm]\n" +
          "4 5 6\n" +
          "}\n" +
          "\n" +
          "# Bismut\n" +
          "a=3")
        ast = parse(a)
        program = interpreter.interpret(ast, {})

    def test_coordinated_brackets(self):
        ast = parse(
            "grad_Bi = (2)*(3)"
        )
        program = interpreter.interpret(ast, {})


    def test_assignment(self):
        ns = {}
        ast = parse(
            "\"Force\" F = 1.234 <0.01> [N]"
        )
        program = interpreter.interpret(ast, ns)
        self.assertEqual(ns["F"].longname, 'Force')
        self.assertEqual(ns["F"].name, 'F')
        self.assertEqual(ns["F"].value, 1.234)
        self.assertEqual(ns["F"].error, 0.01)
        #TODO: test units/dim
        #self.assertEqual(ns["F"].unit, 'N')
        #self.assertEqual(ns["F"].error_unit, 'N')

    def test_assignment_formula(self):
        ns = {}
        ast = parse(
            "\"Force\" F = 1 * (2+3)"
        )
        program = interpreter.interpret(ast, ns)
        self.assertEqual(ns["F"].longname, 'Force')
        self.assertEqual(ns["F"].name, 'F')
        self.assertEqual(ns["F"].value, 5)

    def test_unquoted_longname(self):
        ns = {}
        ast = parse(
            "My favorite väriable F = 1 * (2+3)"
        )
        program = interpreter.interpret(ast, ns)
        self.assertEqual(ns["F"].longname, 'My favorite väriable')
        self.assertEqual(ns["F"].name, 'F')


    def test_multi_assignment(self):
        ns = {}
        ast = parse(
            "{\n" +
            " F[N], s[m], s_err[cm]\n" +
            " 1.1 2 0.1\n" +
            " 3 4 0.2\n"
            "}"
        )
        program = interpreter.interpret(ast, ns)
        self.assertEqual(ns["F"].name, 'F')
        self.assertEqual(ns["F"].value[0], 1.1)
        self.assertEqual(ns["F"].value[1], 3)
        self.assertEqual(ns["s"].name, 's')
        self.assertEqual(ns["s"].value[0], 2)
        self.assertEqual(ns["s"].value[1], 4)
        self.assertEqual(ns["s"].error[0], 0.001)
        self.assertEqual(ns["s"].error[1], 0.002)

""" TODO
    def test_assignment_formula_quoted(self):
        ns = {}
        ast = parse(
            "a = 4\n"+
            "\"Force\" F = 'a * [2+3]'"
        )
        program = interpreter.interpret(ast, ns)
        self.assertEqual(ns["F"].longname, 'Force')
        self.assertEqual(ns["F"].name, 'F')
        self.assertEqual(ns["F"].value, 5)
"""

if __name__ == '__main__':
    unittest.main()
