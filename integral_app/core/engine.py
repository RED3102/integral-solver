import sympy
from sympy import Symbol, Add, integrate, expand

x = Symbol("x")


def compute_integral(expr: sympy.Expr) -> sympy.Expr:
    """
    Returns the indefinite integral of expr w.r.t. x (without + C).
    Raises ValueError if no closed-form result is found.
    """
    result = integrate(expr, x)
    if result.has(sympy.Integral):
        raise ValueError(
            "This function does not have a standard antiderivative.\n"
            "Try a simpler expression."
        )
    return result


def get_terms(expr: sympy.Expr) -> list:
    """Splits an expression into its additive terms."""
    expanded = expand(expr)
    return list(expanded.args) if isinstance(expanded, Add) else [expanded]


def integrate_term(term: sympy.Expr) -> sympy.Expr:
    """Integrates a single term w.r.t. x."""
    result = integrate(term, x)
    if result.has(sympy.Integral):
        raise ValueError(
            "One or more terms could not be integrated.\n"
            "Try a simpler expression."
        )
    return result