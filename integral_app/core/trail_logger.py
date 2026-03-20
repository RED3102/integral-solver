import sympy
from sympy import Symbol
from core.engine import get_terms, integrate_term
from core.parser import identify_rule
from core.formatter import fmt

x = Symbol("x")
DIVIDER = "-" * 55


def _join_terms(term_results):
    """
    Joins term results into a clean string.
    Handles negative terms so '+ -cos(x)' becomes '- cos(x)'.
    """
    parts = []
    for i, r in enumerate(term_results):
        r_str = fmt(r)
        if i == 0:
            parts.append(r_str)
        elif r_str.startswith("-"):
            parts.append("- " + r_str[1:].strip())
        else:
            parts.append("+ " + r_str)
    return "  " + "  ".join(parts)


def build_trail(expr, antiderivative, verification_msg):
    """Returns the full solution trail as a plain multi-line string."""
    lines = []
    expr_str = fmt(expr)
    terms = get_terms(expr)
    multi = len(terms) > 1

    # GIVEN
    lines.append(DIVIDER)
    lines.append("GIVEN")
    lines.append(DIVIDER)
    lines.append(f"  integral( {expr_str} ) dx")
    lines.append("")

    # STEP 1: Linearity — multi-term only
    if multi:
        lines.append(DIVIDER)
        lines.append("STEP 1 - Linearity of Integration")
        lines.append(DIVIDER)
        lines.append("  integral(a + b + c) dx = integral(a) dx + integral(b) dx + ...")
        lines.append("  = " + " + ".join(f"integral({fmt(t)}) dx" for t in terms))
        lines.append("")
        step_num = 2
    else:
        step_num = 1

    # STEP 2: Integrate each term
    lines.append(DIVIDER)
    lines.append(f"STEP {step_num} - Integrate Each Term")
    lines.append(DIVIDER)

    term_results = []
    for i, term in enumerate(terms, start=1):
        try:
            result = integrate_term(term)
        except ValueError:
            result = sympy.Symbol("?")
        rule_name, rule_formula = identify_rule(term)
        lines.append(f"\n  Term {i}: integral( {fmt(term)} ) dx")
        lines.append(f"  Rule    : {rule_name}")
        lines.append(f"  Formula : {rule_formula}")
        lines.append(f"  Result  : {fmt(result)}")
        term_results.append(result)
    lines.append("")

    # STEP 3: Combine — multi-term only
    if multi:
        lines.append(DIVIDER)
        lines.append(f"STEP {step_num + 1} - Combine Results")
        lines.append(DIVIDER)
        lines.append(_join_terms(term_results))
        lines.append(f"  Simplified: {fmt(antiderivative)}")
        lines.append("")

    # FINAL ANSWER
    lines.append(DIVIDER)
    lines.append("FINAL ANSWER")
    lines.append(DIVIDER)
    lines.append(f"  integral( {expr_str} ) dx  =  {fmt(antiderivative)} + C")
    lines.append("")

    # VERIFICATION
    lines.append(DIVIDER)
    lines.append("VERIFICATION")
    lines.append(DIVIDER)
    for vline in verification_msg.splitlines():
        lines.append(f"  {vline}")
    lines.append("")
    lines.append(DIVIDER)

    return "\n".join(lines)