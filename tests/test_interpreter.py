import unittest
from parsing.parsing import parse
import interpreter
import commands
import io

class InterpreterTestCase(unittest.TestCase):

    def test_multiple_commands(self):
        ast = parse(
            "x = 12.5e-3 <0.001> [ms]\n" +
            "fit(m*x1+b,x1,x2,[m,b])\n"
        )
        program = interpreter.interpret(ast)
        self.assertTrue(type(program[0]) is commands.Assignment)
        self.assertTrue(type(program[1]) is commands.Fit)

    def test_set_function(self):
        ast = parse(
            "set(foo,bar)"
        )
        program = interpreter.interpret(ast)
        self.assertTrue(type(program[0]) is commands.Set)
        self.assertEqual(program[0].entry, 'foo')
        self.assertEqual(program[0].value, 'bar')

    def test_fit_function(self):
        ast = parse(
            "fit(m*x1+b,x1,x2,[m,b])"
        )
        program = interpreter.interpret(ast)
        self.assertTrue(type(program[0]) is commands.Fit)
        self.assertEqual(program[0].fit_function_str, 'm*x1+b')
        self.assertEqual(program[0].x_data_str, 'x1')
        self.assertEqual(program[0].y_data_str, 'x2')
        self.assertEqual(program[0].parameters_str, ['m', 'b'])

    def test_plot_function(self):
        ast = parse(
            "plot([[A1,A2],[B1,B2]])"
        )
        program = interpreter.interpret(ast)
        self.assertTrue(type(program[0]) is commands.Plot)
        self.assertEqual(program[0].quantity_pairs, [['A1','A2'],['B1','B2']])

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
            " F[N], s[m]\n" +
            " 1.1 2\n" +
            " 3 4\n"
            "}"
        )
        program = interpreter.interpret(ast)
        self.assertTrue(type(program[0]) is commands.Assignment)
        self.assertEqual(program[0].name, 'F')
        self.assertEqual(program[0].value, ['1.1','3'])
        self.assertTrue(type(program[1]) is commands.Assignment)
        self.assertEqual(program[1].name, 's')
        self.assertEqual(program[1].value, ['2','4'])

if __name__ == '__main__':
    unittest.main()
