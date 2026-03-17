import sympy
from sympy import Symbol, diff

x = Symbol("x")


def verify(original_expr: sympy.Expr, antiderivative: sympy.Expr) -> tuple:
    derivative = diff(antiderivative, x)
    difference = sympy.simplify(derivative - original_expr)

    is_correct = (difference == 0)

    deriv_str    = str(derivative)
    original_str = str(original_expr)
    F_str        = str(antiderivative)

    if is_correct:
        msg = (
            f"VERIFICATION PASSED\n"
            f"  d/dx [ {F_str} ]  =  {deriv_str}\n"
            f"  This equals the original f(x) = {original_str}  [OK]"
        )
    else:
        msg = (
            f"VERIFICATION NOTE\n"
            f"  d/dx [ {F_str} ]  =  {deriv_str}\n"
            f"  Original f(x) = {original_str}\n"
            f"  (Could not confirm equivalence automatically.)"
        )

    return is_correct, msg