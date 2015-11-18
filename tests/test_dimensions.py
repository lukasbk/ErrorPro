import unittest
from dimensions.solvers import dim_solve, dim_solve_global
from dimensions.simplifiers import dim_simplify
from dimensions.dimensions import Dimension
from sympy import Symbol, Add, Mul, Pow

class DimensionTestCase(unittest.TestCase):

    def test_dim_solve_global(self):
        self.assertEqual(dim_solve_global(Symbol('x'), {'x':Dimension({})}),Dimension({}))
        self.assertEqual(dim_solve_global(Symbol('x'), {}), None)

    def test_solve_pow(self):
        L = Dimension({"length":1})
        solution = dim_solve(
            Pow(Add(Symbol("x"),Symbol("y")), 2),
            L.pow(2)
        )
        self.assertEqual(solution["x"], L)
        self.assertEqual(solution["y"], L)


    def test_solve_mul_add(self):
        L = Dimension({"length":1})
        solution = dim_solve(
            Mul(Symbol("y"), Add(Symbol("x"), L)),
            L
        )
        self.assertEqual(solution["x"], L)
        self.assertEqual(solution["y"], Dimension({}))

    def test_solve_mul2(self):
        L = Dimension({"length":1})
        solution = dim_solve(
            Mul(Symbol("y"), Symbol("x")),
            L
        )
        self.assertEqual(solution, {})

    def test_solve_mul(self):
        L = Dimension({"length":1})
        solution = dim_solve(
            Mul(L, Symbol("x")),
            L.mul(L)
        )
        self.assertEqual(solution["x"], L)

    def test_solve_add(self):
        L = Dimension({"length":1})
        solution = dim_solve(
            Add(L, Symbol("x")),
            L
        )
        self.assertEqual(solution["x"], L)

    def test_solve_add2(self):
        L = Dimension({"length":1})
        solution = dim_solve(
            Add(L, Symbol("x"))
        )
        self.assertEqual(solution["x"], L)

if __name__ == '__main__':
    unittest.main()
