from sympy import Symbol, Add, Mul, Pow
from dimensions.dimensions import Dimension
from dimensions.simplifiers import dim_simplify

def dim_solve(expr, dim = None, resolved=None):
    if resolved is None:
        resolved = {}

    if dim == None:
        if isinstance(expr, Add):
            for arg in expr.args:
                argdim = dim_solve_global(arg, resolved)
                if argdim != None:
                    return dim_solve(expr, argdim, resolved)

        return resolved

    else:
        if isinstance(expr, Dimension):
            if expr == dim:
                return resolved
            else:
                raise ValueError()

        if isinstance(expr, Symbol):
            if expr.name in resolved:
                if resolved[expr.name] != dim:
                    raise ValueError()
            else:
                resolved[expr.name] = dim
            return resolved

        if isinstance(expr, Add):
            for arg in expr.args:
                resolved = dim_solve(arg, dim, resolved)
            return resolved

        if isinstance(expr, Mul):
            for arg in expr.args:
                resolved = dim_solve(arg, None, resolved)

            # we can only conclude sth else if only one arg is of unknown dimension
            unknown = None
            unknowndim = dim
            for arg in expr.args:
                argdim = dim_solve_global(arg, resolved)
                if argdim == None:
                    if unknown != None:
                        # second unknown factor found, give up
                        return resolved
                    unknown = arg
                else:
                    unknowndim = unknowndim.div(argdim)
            return dim_solve(unknown, unknowndim, resolved)

        if isinstance(expr, Pow):
            if expr.args[1].is_number:
                return dim_solve(expr.args[0], dim.pow(1/expr.args[1]), resolved)
            else:
                return dim_solve(expr.args[0], Dimension({}), resolved)


def dim_solve_global(expr, resolved={}):
    expr = subs_symbols(expr, resolved)

    try:
        return dim_simplify(expr)
    except ValueError:
        return None

def subs_symbols(expr, subs):
    if isinstance(expr, Symbol) and expr.name in subs:
        return subs[expr.name]

    if hasattr(expr, "args") and len(expr.args)>0:
        return expr.func(*[subs_symbols(arg, subs) for arg in expr.args])
    else:
        return expr
