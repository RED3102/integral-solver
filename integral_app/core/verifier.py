import sympy
from sympy import Symbol, diff
from core.formatter import fmt

x = Symbol("x")


def verify(original_expr: sympy.Expr, antiderivative: sympy.Expr) -> tuple:
    """
    Checks that d/dx(antiderivative) == original_expr.
    Returns (is_correct, message_string).
    """
    derivative = diff(antiderivative, x)
    difference = sympy.simplify(derivative - original_expr)
    is_correct = (difference == 0)

    if is_correct:
        msg = (
            f"VERIFICATION PASSED\n"
            f"  d/dx [ {fmt(antiderivative)} ]  =  {fmt(derivative)}\n"
            f"  This equals the original f(x) = {fmt(original_expr)}  [OK]"
        )
    else:
        msg = (
            f"VERIFICATION NOTE\n"
            f"  d/dx [ {fmt(antiderivative)} ]  =  {fmt(derivative)}\n"
            f"  Original f(x) = {fmt(original_expr)}\n"
            f"  (Could not confirm equivalence automatically.)"
        )

    return is_correct, msg