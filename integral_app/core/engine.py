import sympy
from sympy import Symbol, Add, integrate, expand

x = Symbol("x")


def compute_integral(expr: sympy.Expr) -> sympy.Expr:
    result = integrate(expr, x)
    if result.has(sympy.Integral):
        raise ValueError("No closed-form antiderivative found. Try a simpler expression.")
    return result


def get_terms(expr: sympy.Expr) -> list:
    expanded = expand(expr)
    return list(expanded.args) if isinstance(expanded, Add) else [expanded]


def integrate_term(term: sympy.Expr) -> sympy.Expr:
    result = integrate(term, x)
    if result.has(sympy.Integral):
        raise ValueError(f"Could not integrate term: {term}")
    return result