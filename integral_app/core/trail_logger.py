import sympy
from sympy import Symbol
from core.engine import get_terms, integrate_term
from core.parser import identify_rule

x = Symbol("x")
DIVIDER = "-" * 55


def build_trail(expr, antiderivative, verification_msg):
    """Returns the full solution trail as a plain multi-line string."""
    lines = []
    expr_str = str(expr)

    # GIVEN
    lines.append(DIVIDER)
    lines.append("GIVEN")
    lines.append(DIVIDER)
    lines.append(f"  integral( {expr_str} ) dx")
    lines.append("")

    # STEP 1: Linearity (multi-term only)
    terms = get_terms(expr)
    if len(terms) > 1:
        lines.append(DIVIDER)
        lines.append("STEP 1 - Linearity of Integration")
        lines.append(DIVIDER)
        lines.append("  integral(a + b + c) dx = integral(a) dx + integral(b) dx + ...")
        lines.append("  = " + " + ".join(f"integral({str(t)}) dx" for t in terms))
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
        lines.append(f"\n  Term {i}: integral( {str(term)} ) dx")
        lines.append(f"  Rule    : {rule_name}")
        lines.append(f"  Formula : {rule_formula}")
        lines.append(f"  Result  : {str(result)}")
        term_results.append(result)
    lines.append("")

    # STEP 3: Combine (multi-term only)
    if len(terms) > 1:
        lines.append(DIVIDER)
        lines.append(f"STEP {step_num + 1} - Combine Results")
        lines.append(DIVIDER)
        lines.append("  " + " + ".join(str(r) for r in term_results))
        lines.append(f"  Simplified: {str(antiderivative)}")
        lines.append("")

    # FINAL ANSWER
    lines.append(DIVIDER)
    lines.append("FINAL ANSWER")
    lines.append(DIVIDER)
    lines.append(f"  integral( {expr_str} ) dx  =  {str(antiderivative)} + C")
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