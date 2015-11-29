import unittest
from errorpro.parsing.parsing import parse
from errorpro import interpreter
from errorpro import commands
import io

class InterpreterTestCase(unittest.TestCase):
    def test_pythoncode_combi(self):
        a=(">bla\n"+
           ">bla\n"+
           "a=3")
        ast = parse(a)
        program = interpreter.interpret(ast)
        self.assertTrue(type(program[0]) is commands.PythonCode)
        self.assertEqual(program[0].code, "bla\nbla")
        self.assertTrue(type(program[1]) is commands.Assignment)

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
        program = interpreter.interpret(ast)

    def test_coordinated_brackets(self):
        ast = parse(
            "grad_Bi = (a1)*(a0)"
        )
        program = interpreter.interpret(ast)


    def test_multiple_commands(self):
        ast = parse(
            "x = 12.5e-3 <0.001> [ms]\n#Comment\n" +
            "# Comment 2\n" +
            ">fit('m*x1+b',('x1','x2'),['m','b'])\n"
        )
        program = interpreter.interpret(ast)
        self.assertTrue(type(program[0]) is commands.Assignment)
        self.assertTrue(type(program[1]) is commands.PythonCode)

    def test_assignment(self):
        ast = parse(
            "\"Force\" F = 1.234 <0.01> [N]"
        )
        program = interpreter.interpret(ast)
        self.assertTrue(type(program[0]) is commands.Assignment)
        self.assertEqual(program[0].longname, 'Force')
        self.assertEqual(program[0].name, 'F')
        self.assertEqual(program[0].value, '1.234 ')
        self.assertEqual(program[0].uncert, '0.01')
        self.assertEqual(program[0].value_unit, 'N')
        self.assertEqual(program[0].uncert_unit, 'N')

    def test_assignment_formula(self):
        ast = parse(
            "\"Force\" F = a * (b+3)"
        )
        program = interpreter.interpret(ast)
        self.assertTrue(type(program[0]) is commands.Assignment)
        self.assertEqual(program[0].longname, 'Force')
        self.assertEqual(program[0].name, 'F')
        self.assertEqual(program[0].value, 'a * (b+3)')

    def test_unquoted_longname(self):
        ast = parse(
            "My favorite väriable F = a * (b+3)"
        )
        program = interpreter.interpret(ast)
        self.assertTrue(type(program[0]) is commands.Assignment)
        self.assertEqual(program[0].longname, 'My favorite väriable')
        self.assertEqual(program[0].name, 'F')
        self.assertEqual(program[0].value, 'a * (b+3)')

    def test_assignment_formula_quoted(self):
        ast = parse(
            "\"Force\" F = 'a * [b+3]'"
        )
        program = interpreter.interpret(ast)
        self.assertTrue(type(program[0]) is commands.Assignment)
        self.assertEqual(program[0].longname, 'Force')
        self.assertEqual(program[0].name, 'F')
        self.assertEqual(program[0].value, 'a * [b+3]')

    def test_python_code(self):
        ast = parse(
            ">if var=True:\n"+
            ">    print('World')"
        )
        program = interpreter.interpret(ast)
        self.assertTrue(type(program[0]) is commands.PythonCode)
        self.assertEqual(program[0].code,
            "if var=True:\n"+
            "    print('World')"
        )

    def test_multi_assignment(self):
        ast = parse(
            "{\n" +
            " F[N], s[m], s_err[cm]\n" +
            " 1.1 2 0.1\n" +
            " 3 4 0.2\n"
            "}"
        )
        program = interpreter.interpret(ast)
        self.assertTrue(type(program[0]) is commands.Assignment)
        self.assertEqual(program[0].name, 'F')
        self.assertEqual(program[0].value, ['1.1','3'])
        self.assertTrue(type(program[1]) is commands.Assignment)
        self.assertEqual(program[1].name, 's')
        self.assertEqual(program[1].value, ['2','4'])
        self.assertTrue(type(program[2]) is commands.Assignment)
        self.assertEqual(program[2].name, 's')
        self.assertEqual(program[2].uncert, ['0.1','0.2'])

if __name__ == '__main__':
    unittest.main()
