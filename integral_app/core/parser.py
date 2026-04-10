"""
parser.py - Identifies the integration rule for a single term.
Week 8 - Added Integration by Parts detection.
"""

import sympy
from sympy import Symbol, Pow, Mul, sin, cos, exp, log, tan, sec, csc, sinh, cosh, cot, asin, atan

x = Symbol("x")


def identify_rule(term: sympy.Expr) -> tuple:
    """Returns (rule_name, rule_formula) for a single term."""
    coeff, base = _split_coefficient(term)

    # Constant (no x)
    if not term.free_symbols:
        return ("Constant Rule", "integral(k) dx = kx")

    # 1/x — before general Power Rule
    if isinstance(base, Pow) and base.args[0] == x and base.args[1] == -1:
        return ("Logarithmic Rule", "integral(1/x) dx = ln|x|")

    # Power Rule (with or without coefficient)
    if base == x or (isinstance(base, Pow) and base.args[0] == x and base.args[1].is_number):
        return ("Power Rule", "integral(x^n) dx = x^(n+1)/(n+1)")

    # Exponential
    if base == exp(x) or base == sympy.E**x:
        return ("Exponential Rule", "integral(e^x) dx = e^x")

    # Basic trig
    if base == sin(x):
        return ("Trigonometric Rule", "integral(sin(x)) dx = -cos(x)")

    if base == cos(x):
        return ("Trigonometric Rule", "integral(cos(x)) dx = sin(x)")

    if base == sympy.tan(x):
        return ("Trigonometric Rule", "integral(tan(x)) dx = -ln|cos(x)|")

    if base == sympy.sec(x)**2:
        return ("Trigonometric Rule", "integral(sec^2(x)) dx = tan(x)")

    if base == sympy.csc(x)**2:
        return ("Trigonometric Rule", "integral(csc^2(x)) dx = -cot(x)")

    if base == sympy.sec(x) * sympy.tan(x):
        return ("Trigonometric Rule", "integral(sec(x)*tan(x)) dx = sec(x)")

    # Inverse trig
    if base == 1 / sympy.sqrt(1 - x**2):
        return ("Inverse Trigonometric Rule", "integral(1/sqrt(1-x^2)) dx = arcsin(x)")

    if base == 1 / (1 + x**2):
        return ("Inverse Trigonometric Rule", "integral(1/(1+x^2)) dx = arctan(x)")

    # Hyperbolic
    if base == sympy.sinh(x):
        return ("Hyperbolic Rule", "integral(sinh(x)) dx = cosh(x)")

    if base == sympy.cosh(x):
        return ("Hyperbolic Rule", "integral(cosh(x)) dx = sinh(x)")

    # Logarithm — must come before IBP so log(x) alone uses Logarithmic Rule
    if base == log(x):
        return ("Logarithmic Rule", "integral(ln(x)) dx = x*ln(x) - x")

    # Integration by Parts — products of polynomial × function
    if _is_integration_by_parts(term) or (coeff != 1 and _is_integration_by_parts(base)):
        return ("Integration by Parts", "integral(u dv) dx = u*v - integral(v du) dx")

    # Constant Multiple Rule — fallback when base has no specific rule
    if coeff != 1:
        return ("Constant Multiple Rule", "integral(c*f(x)) dx = c * integral(f(x)) dx")

    return ("Standard Integration", "integral(f(x)) dx  [computed by SymPy]")


def _is_integration_by_parts(term: sympy.Expr) -> bool:
    """
    Detects expressions that are best handled by integration by parts.
    Covers: x*sin(x), x*cos(x), x*exp(x), x*log(x), x*arctan(x), x*arcsin(x)
    Note: log(x) alone is handled by the Logarithmic Rule above, not here.
    """
    if term == atan(x) or term == asin(x):
        return True

    if isinstance(term, Mul):
        factors = term.args
        has_poly     = any(_is_power_of_x(f) for f in factors)
        has_ibp_func = any(_is_ibp_function(f) for f in factors)
        return has_poly and has_ibp_func

    return False


def _is_power_of_x(expr: sympy.Expr) -> bool:
    """Returns True if expr is x or x^n (positive integer power)."""
    return (
        expr == x or
        (isinstance(expr, Pow) and
         expr.args[0] == x and
         expr.args[1].is_number and
         expr.args[1] > 0)
    )


def _is_ibp_function(expr: sympy.Expr) -> bool:
    """Returns True if expr is a function type suited for IBP."""
    return expr in {
        sin(x), cos(x), exp(x), log(x),
        atan(x), asin(x), sinh(x), cosh(x)
    }


def _split_coefficient(term: sympy.Expr):
    """Splits a Mul term into (numeric coefficient, base expression)."""
    if isinstance(term, Mul):
        numbers = [a for a in term.args if a.is_number]
        others  = [a for a in term.args if not a.is_number]
        if numbers and others:
            base = sympy.Mul(*others) if len(others) > 1 else others[0]
            return sympy.Mul(*numbers), base
    return sympy.Integer(1), term