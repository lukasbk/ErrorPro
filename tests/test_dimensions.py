import unittest
from errorpro.dimensions.solvers import dim_solve, dim_solve_global
from errorpro.dimensions.simplifiers import dim_simplify
from errorpro.dimensions.dimensions import Dimension
from sympy import Symbol, Add, Mul, Pow, sin, sympify

class DimensionTestCase(unittest.TestCase):

    def test_sin(self):
        L = Dimension({"length":1})
        solution = dim_solve(
            sin(Symbol("x"))*Symbol("y"),
            L
        )
        self.assertEqual(solution["x"], Dimension({}))
        self.assertEqual(solution["y"], L)

    def test_dim_solve_global(self):
        self.assertEqual(dim_solve_global(Symbol('x'), {'x':Dimension({})}),Dimension({}))
        self.assertEqual(dim_solve_global(Symbol('x'), {}), None)
        self.assertEqual(dim_solve_global(sympify('t-b'), {'t':Dimension({'time':1})}), Dimension({'time':1}))
        self.assertEqual(dim_solve_global(sympify('t-b'), {'t':Dimension({'time':1}), 'b':Dimension({'time':1})}), Dimension({'time':1}))

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

    def test_solve_pow(self):
        L = Dimension({"length":1})
        T = Dimension({"time":1})
        solution = dim_solve(
            sympify("a*(t-b)**2+c"),
            L,
            {'t': T}
        )
        self.assertEqual(solution["b"], T)
        self.assertEqual(solution["a"], L.mul(T.pow(-2)))
        self.assertEqual(solution["t"], T)
        self.assertEqual(solution["c"], L)

if __name__ == '__main__':
    unittest.main()
