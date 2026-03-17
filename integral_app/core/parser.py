import sympy
from sympy import Symbol, Pow, Mul, sin, cos, exp, log

x = Symbol("x")


def identify_rule(term: sympy.Expr) -> tuple:
    """Returns (rule_name, rule_formula) for a single term."""
    _, base = _split_coefficient(term)

    if x not in term.free_symbols:
        return ("Constant Rule", "integral(k) dx = kx")

    if isinstance(base, Pow) and base.args[0] == x and base.args[1] == -1:
        return ("Logarithmic Rule", "integral(1/x) dx = ln|x|")

    if base == x or (isinstance(base, Pow) and base.args[0] == x and base.args[1].is_number):
        return ("Power Rule", "integral(x^n) dx = x^(n+1)/(n+1)")

    if base == exp(x) or base == sympy.E**x:
        return ("Exponential Rule", "integral(e^x) dx = e^x")

    if base == sin(x):
        return ("Trigonometric Rule", "integral(sin(x)) dx = -cos(x)")

    if base == cos(x):
        return ("Trigonometric Rule", "integral(cos(x)) dx = sin(x)")

    if base == log(x):
        return ("Logarithmic Rule", "integral(ln(x)) dx = x*ln(x) - x")

    return ("Standard Integration", "integral(f(x)) dx  [computed by SymPy]")


def _split_coefficient(term: sympy.Expr):
    """Splits a Mul term into (numeric coefficient, base expression)."""
    if isinstance(term, Mul):
        numbers = [a for a in term.args if a.is_number]
        others  = [a for a in term.args if not a.is_number]
        if numbers and others:
            base = sympy.Mul(*others) if len(others) > 1 else others[0]
            return sympy.Mul(*numbers), base
    return sympy.Integer(1), term