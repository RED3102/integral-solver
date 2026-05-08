"""
verifier.py - Comprehensive verification with detailed mathematical analysis.
Week 11 - Extended breakdown with expanded/simplified forms.
"""

import sympy
from sympy import Symbol, diff, simplify, expand, factor
from core.formatter import fmt

x = Symbol("x")


def _get_derivative_details(antiderivative):
    """Computes derivative and returns multiple simplified forms."""
    result    = diff(antiderivative, x)
    expanded  = expand(result)
    simplified = simplify(result)
    return {
        "raw":        result,
        "expanded":   expanded,
        "simplified": simplified,
    }


def _compare_expressions(original, derivative):
    """Detailed comparison of two expressions."""
    diff_simplified = simplify(derivative - original)
    return {
        "equal":               (diff_simplified == 0),
        "difference":          diff_simplified,
        "original_expanded":   expand(original),
        "derivative_expanded": expand(derivative),
    }


def verify(original_expr: sympy.Expr, antiderivative: sympy.Expr) -> tuple:
    """
    Comprehensive verification with detailed mathematical analysis.
    Returns (is_correct, message_string).
    """
    derivative   = diff(antiderivative, x)
    deriv_detail = _get_derivative_details(antiderivative)
    comparison   = _compare_expressions(original_expr, derivative)
    is_correct   = comparison["equal"]

    SEP = "  " + "-" * 45
    lines = []

    lines.append("=" * 55)
    lines.append("  COMPREHENSIVE VERIFICATION ANALYSIS")
    lines.append("=" * 55)
    lines.append("")

    # Verification method
    lines.append("  VERIFICATION METHOD:")
    lines.append(SEP)
    lines.append("  Check that d/dx[F(x)] = f(x).")
    lines.append("  If the derivative of the antiderivative equals")
    lines.append("  the original function, the integration is correct.")
    lines.append("")

    # Given information
    lines.append("  GIVEN INFORMATION:")
    lines.append(SEP)
    lines.append(f"  Original function  :  f(x) = {fmt(original_expr)}")
    lines.append(f"  Antiderivative     :  F(x) = {fmt(antiderivative)}")
    lines.append("")

    # Derivative computation
    lines.append("  DERIVATIVE COMPUTATION:")
    lines.append(SEP)
    lines.append(f"  d/dx[ {fmt(antiderivative)} ]")
    lines.append(f"  = {fmt(deriv_detail['raw'])}")

    if deriv_detail["raw"] != deriv_detail["expanded"]:
        lines.append(f"\n  Expanded  :  {fmt(deriv_detail['expanded'])}")

    lines.append(f"\n  Simplified:  {fmt(deriv_detail['simplified'])}")
    lines.append("")

    # Comparison
    lines.append("  COMPARISON:")
    lines.append(SEP)
    lines.append(f"  Derivative  :  {fmt(comparison['derivative_expanded'])}")
    lines.append(f"  Original    :  {fmt(comparison['original_expanded'])}")

    if is_correct:
        lines.append(f"  Difference  :  0  [EQUAL]")
    else:
        lines.append(f"  Difference  :  {fmt(comparison['difference'])}")
    lines.append("")

    # Result
    lines.append("  VERIFICATION RESULT:")
    lines.append(SEP)

    if is_correct:
        lines.append("  VERIFICATION PASSED [OK]")
        lines.append("")
        lines.append("  The derivative of the antiderivative equals")
        lines.append("  the original function. Integration is CORRECT.")
        lines.append("")
        lines.append(f"  Final Answer:")
        lines.append(f"    integral( {fmt(original_expr)} ) dx  =  {fmt(antiderivative)} + C")
    else:
        lines.append("  VERIFICATION NOTE")
        lines.append("")
        lines.append("  Automatic comparison could not confirm equivalence.")
        lines.append("  The expressions may still be mathematically equal.")
        lines.append("")
        lines.append(f"  Derivative  :  {fmt(derivative)}")
        lines.append(f"  Original    :  {fmt(original_expr)}")
        lines.append(f"  Difference  :  {fmt(comparison['difference'])}")
        lines.append("")
        lines.append(f"  Answer:  integral( {fmt(original_expr)} ) dx  =  {fmt(antiderivative)} + C")

    lines.append("")
    lines.append("=" * 55)

    return is_correct, "\n".join(lines)