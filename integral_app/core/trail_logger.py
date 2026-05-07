"""
trail_logger.py - Builds the plain-text step-by-step solution trail.
Week 11 - Improved visual structure and section headers.
"""

import sympy
from sympy import Symbol
from core.engine import get_terms, integrate_term
from core.parser import identify_rule
from core.formatter import fmt

x = Symbol("x")

# Visual dividers
DIVIDER_HEAVY = "═" * 55
DIVIDER_LIGHT = "─" * 55
DIVIDER_DOT   = "┄" * 55


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

    # ── GIVEN ──────────────────────────────────────────────────────────────
    lines.append(DIVIDER_HEAVY)
    lines.append("  GIVEN")
    lines.append(DIVIDER_HEAVY)
    lines.append(f"\n  ∫ ( {expr_str} ) dx\n")

    # ── STEP 1: Linearity ──────────────────────────────────────────────────
    if multi:
        lines.append(DIVIDER_LIGHT)
        lines.append("  STEP 1  —  Linearity of Integration")
        lines.append(DIVIDER_LIGHT)
        lines.append("\n  ∫(a + b + c) dx = ∫a dx + ∫b dx + ∫c dx + …\n")
        lines.append("  = " + "  +  ".join(f"∫({fmt(t)}) dx" for t in terms))
        lines.append("")
        step_num = 2
    else:
        step_num = 1

    # ── STEP 2: Integrate each term ────────────────────────────────────────
    lines.append(DIVIDER_LIGHT)
    lines.append(f"  STEP {step_num}  —  Integrate Each Term")
    lines.append(DIVIDER_LIGHT)

    term_results = []
    for i, term in enumerate(terms, start=1):
        try:
            result = integrate_term(term)
        except ValueError:
            result = sympy.Symbol("?")
        rule_name, rule_formula = identify_rule(term)

        lines.append(f"\n  Term {i}")
        lines.append(DIVIDER_DOT)
        lines.append(f"  Expression :  ∫( {fmt(term)} ) dx")
        lines.append(f"  Rule       :  {rule_name}")
        if rule_name == "Standard Integration":
            lines.append(f"  Note       :  No single standard rule applies.")
            lines.append(f"                SymPy computed this directly.")
        else:
            lines.append(f"  Formula    :  {rule_formula}")
        lines.append(f"  Result     :  {fmt(result)}")
        term_results.append(result)

    lines.append("")

    # ── STEP 3: Combine ────────────────────────────────────────────────────
    if multi:
        lines.append(DIVIDER_LIGHT)
        lines.append(f"  STEP {step_num + 1}  —  Combine Results")
        lines.append(DIVIDER_LIGHT)
        lines.append(f"\n{_join_terms(term_results)}")
        lines.append(f"\n  Simplified:  {fmt(antiderivative)}\n")

    # ── FINAL ANSWER ───────────────────────────────────────────────────────
    lines.append(DIVIDER_HEAVY)
    lines.append("  FINAL ANSWER")
    lines.append(DIVIDER_HEAVY)
    lines.append(f"\n  ∫ ( {expr_str} ) dx  =  {fmt(antiderivative)}  +  C\n")

    # ── VERIFICATION ───────────────────────────────────────────────────────
    lines.append(DIVIDER_LIGHT)
    lines.append("  VERIFICATION")
    lines.append(DIVIDER_LIGHT)
    lines.append("")
    for vline in verification_msg.splitlines():
        lines.append(f"  {vline}")
    lines.append("")
    lines.append(DIVIDER_HEAVY)

    return "\n".join(lines)