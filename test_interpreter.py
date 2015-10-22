import unittest
import parse
import interpreter
import commands

class InterpreterTestCase(unittest.TestCase):

    def test_interpreter(self):
        p = parse.parse_file(
            "x = 12.5e-3 <0.001> [ms]\n"
            "$fit m*x1+b to (x1,x2) via m,b"
        )
        program = interpreter.interpret(p)
        self.assertTrue(type(program[0]) is commands.Assignment)
        self.assertTrue(type(program[1]) is commands.Fit)

if __name__ == '__main__':
    unittest.main()
