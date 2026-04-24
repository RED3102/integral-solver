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
            f"VERIFICATION PASSED [OK]\n"
            f"\n"
            f"  Step 1: Original function (what we integrated)\n"
            f"    f(x) = {fmt(original_expr)}\n"
            f"\n"
            f"  Step 2: The antiderivative we found\n"
            f"    F(x) = {fmt(antiderivative)}\n"
            f"\n"
            f"  Step 3: Take the derivative of F(x)\n"
            f"    d/dx [ F(x) ] = d/dx [ {fmt(antiderivative)} ]\n"
            f"                  = {fmt(derivative)}\n"
            f"\n"
            f"  Step 4: Check if it equals the original\n"
            f"    {fmt(derivative)} = {fmt(original_expr)}  [MATCH]\n"
            f"\n"
            f"  Result: The integration is CORRECT."
        )
    else:
        msg = (
            f"VERIFICATION NOTE\n"
            f"\n"
            f"  Step 1: Original function (what we integrated)\n"
            f"    f(x) = {fmt(original_expr)}\n"
            f"\n"
            f"  Step 2: The antiderivative we found\n"
            f"    F(x) = {fmt(antiderivative)}\n"
            f"\n"
            f"  Step 3: Take the derivative of F(x)\n"
            f"    d/dx [ F(x) ] = d/dx [ {fmt(antiderivative)} ]\n"
            f"                  = {fmt(derivative)}\n"
            f"\n"
            f"  Step 4: Compare with the original\n"
            f"    Derivative result : {fmt(derivative)}\n"
            f"    Original f(x)     : {fmt(original_expr)}\n"
            f"    Difference        : {fmt(difference)}\n"
            f"\n"
            f"  Note: Could not automatically confirm equivalence.\n"
            f"        The expressions may still be mathematically equal."
        )

    return is_correct, msg