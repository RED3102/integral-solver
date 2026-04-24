import sympy
from sympy import Symbol, Add, integrate, expand

x = Symbol("x")

# SymPy special functions that indicate a non-standard result
SPECIAL_FUNCTIONS = (
    sympy.erf, sympy.erfi, sympy.Si, sympy.Ci,
    sympy.Ei, sympy.li, sympy.fresnels, sympy.fresnelc,
    sympy.uppergamma, sympy.lowergamma, sympy.hyper,
)


def compute_integral(expr: sympy.Expr) -> sympy.Expr:
    """
    Returns the indefinite integral of expr w.r.t. x (without + C).
    Raises ValueError if no closed-form result is found or if the
    result contains special functions beyond standard calculus.
    """
    result = integrate(expr, x)

    # SymPy returned an unevaluated Integral — no closed form
    if result.has(sympy.Integral):
        raise ValueError(
            "This function does not have a standard antiderivative.\n"
            "Try a simpler expression."
        )

    # Result contains special functions — not useful for this tool
    if any(result.has(fn) for fn in SPECIAL_FUNCTIONS):
        raise ValueError(
            "The antiderivative involves special functions (e.g. erf, Si, Ci)\n"
            "that are beyond standard calculus notation.\n"
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