from sympy import latex, Symbol, Function

def uncert_formula(quantity, adjust):

    if quantity.uncert_depend is None:
        raise ValueError("quantity '%s' doesn't have an uncertainty formula.")
    formula = quantity.uncert_depend

    # replace "_err" by sigma function
    if adjust:
        sigma = Function("\sigma")
        for var in formula.free_symbols:
            if var.name[-4:] == "_err":
                formula = formula.subs(var, sigma( Symbol(var.name[:-4], **var._assumptions)))
        return latex(sigma(quantity)) + " = " + latex(formula)

    return latex(formula)
