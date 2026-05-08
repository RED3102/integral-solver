"""
trail_logger.py - Builds the comprehensive step-by-step solution trail.
Week 11 - Extended analysis with function profiling and rule explanations.
"""

import sympy
from sympy import Symbol, Poly, Pow, Mul, sin, cos, exp, log, tan, sec, csc, sinh, cosh
from core.engine import get_terms, integrate_term
from core.parser import identify_rule
from core.formatter import fmt

x = Symbol("x")
DIVIDER     = "=" * 70
SUB_DIVIDER = "-" * 70


# ── Function analysis helpers ──────────────────────────────────────────────────

def _analyze_function(expr):
    """Analyzes function properties and returns a description dict."""
    return {
        "num_terms":        len(get_terms(expr)),
        "has_trig":         _contains_trig(expr),
        "has_exp":          _contains_exp(expr),
        "has_log":          _contains_log(expr),
        "complexity":       _estimate_complexity(expr),
        "polynomial_degree":_get_polynomial_degree(expr),
    }


def _contains_trig(expr):
    trig_funcs = (sympy.sin, sympy.cos, sympy.tan, sympy.sec, sympy.csc,
                  sympy.asin, sympy.acos, sympy.atan)
    return any(expr.has(f) for f in trig_funcs)


def _contains_exp(expr):
    return expr.has(sympy.exp) or expr.has(sympy.E**x)


def _contains_log(expr):
    return expr.has(sympy.log)


def _get_polynomial_degree(expr):
    try:
        return Poly(expr, x).degree()
    except Exception:
        return None


def _estimate_complexity(expr):
    terms = get_terms(expr)
    n = len(terms)
    if n == 1:
        has_trig = _contains_trig(expr)
        has_exp  = _contains_exp(expr)
        if (has_trig or has_exp) and expr.has(Pow):
            return "High"
        return "Low"
    return "Medium" if n <= 3 else "High"


# ── Rule explanation library ───────────────────────────────────────────────────

def _get_rule_explanation(rule_name):
    explanations = {
        "Constant Rule": (
            "A constant integrates to the constant times the variable.\n"
            "  integral(k) dx = kx + C"
        ),
        "Power Rule": (
            "For any power n != -1:  integral(x^n) dx = x^(n+1)/(n+1) + C\n"
            "  When n = -1, use the Logarithmic Rule instead.\n"
            "  Coefficients carry through: integral(c*x^n) dx = c*x^(n+1)/(n+1) + C"
        ),
        "Logarithmic Rule": (
            "The reciprocal integrates to natural logarithm.\n"
            "  integral(1/x) dx = ln|x| + C\n"
            "  For ln(x): integral(ln(x)) dx = x*ln(x) - x + C"
        ),
        "Exponential Rule": (
            "The exponential function e^x is self-integrating.\n"
            "  integral(e^x) dx = e^x + C"
        ),
        "Trigonometric Rule": (
            "Trigonometric functions integrate to related functions:\n"
            "  integral(sin(x)) dx = -cos(x) + C\n"
            "  integral(cos(x)) dx = sin(x) + C\n"
            "  integral(tan(x)) dx = -ln|cos(x)| + C\n"
            "  integral(sec^2(x)) dx = tan(x) + C\n"
            "  integral(csc^2(x)) dx = -cot(x) + C"
        ),
        "Inverse Trigonometric Rule": (
            "Special rational functions integrate to inverse trig:\n"
            "  integral(1/sqrt(1-x^2)) dx = arcsin(x) + C\n"
            "  integral(1/(1+x^2)) dx = arctan(x) + C"
        ),
        "Hyperbolic Rule": (
            "Hyperbolic functions integrate similarly to trig:\n"
            "  integral(sinh(x)) dx = cosh(x) + C\n"
            "  integral(cosh(x)) dx = sinh(x) + C"
        ),
        "Integration by Parts": (
            "For products use:  integral(u dv) = u*v - integral(v du)\n"
            "  Common forms:  x*sin(x),  x*cos(x),  x*e^x,  x*ln(x)"
        ),
        "Constant Multiple Rule": (
            "A constant factor can be pulled out of the integral:\n"
            "  integral(c*f(x)) dx = c * integral(f(x)) dx + C"
        ),
    }
    return explanations.get(rule_name, f"{rule_name}: computed symbolically by SymPy.")


# ── Term joining ───────────────────────────────────────────────────────────────

def _join_terms(term_results):
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


# ── Main trail builder ─────────────────────────────────────────────────────────

def build_trail(expr, antiderivative, verification_msg):
    """Returns a comprehensive solution trail with all system functions covered."""
    lines = []
    expr_str = fmt(expr)
    terms    = get_terms(expr)
    multi    = len(terms) > 1
    analysis = _analyze_function(expr)

    # ── HEADER ────────────────────────────────────────────────────────────
    lines.append("")
    lines.append(DIVIDER)
    lines.append("  INTEGRAL SOLVER  -  COMPLETE ANALYSIS")
    lines.append(DIVIDER)
    lines.append("")

    # ── SECTION 1: Function Analysis ──────────────────────────────────────
    lines.append(SUB_DIVIDER)
    lines.append("SECTION 1: FUNCTION ANALYSIS")
    lines.append(SUB_DIVIDER)
    lines.append("")
    lines.append(f"  Given Function     : {expr_str}")
    lines.append(f"  Number of Terms    : {analysis['num_terms']}")
    lines.append(f"  Complexity Level   : {analysis['complexity']}")

    func_types = []
    deg = analysis["polynomial_degree"]
    if deg is not None:
        func_types.append(f"Polynomial (degree {deg})")
    if analysis["has_trig"]:
        func_types.append("Trigonometric")
    if analysis["has_exp"]:
        func_types.append("Exponential")
    if analysis["has_log"]:
        func_types.append("Logarithmic")
    if func_types:
        lines.append(f"  Function Types     : {', '.join(func_types)}")
    lines.append("")

    # ── SECTION 2: Problem Setup ───────────────────────────────────────────
    lines.append(SUB_DIVIDER)
    lines.append("SECTION 2: PROBLEM SETUP")
    lines.append(SUB_DIVIDER)
    lines.append("")
    lines.append(f"  Objective          : Find F(x) such that F'(x) = {expr_str}")
    lines.append(f"  Problem            : integral( {expr_str} ) dx = ?")
    lines.append(f"  Variable           : x")
    lines.append(f"  Strategy           : Linearity + Term-by-Term Integration")
    lines.append("")

    # ── SECTION 3: Integration Process ────────────────────────────────────
    lines.append(SUB_DIVIDER)
    lines.append("SECTION 3: INTEGRATION PROCESS")
    lines.append(SUB_DIVIDER)
    lines.append("")

    if multi:
        lines.append("  STEP 1 - Apply Linearity of Integration")
        lines.append("  " + "-" * 45)
        lines.append("")
        lines.append("  integral [f(x) + g(x) + ...] dx = integral f(x) dx + integral g(x) dx + ...")
        lines.append(f"  Applied to: integral( {expr_str} ) dx")
        lines.append("")
        lines.append("  Decomposed into:")
        for i, t in enumerate(terms, 1):
            lines.append(f"    ({i}) integral( {fmt(t)} ) dx")
        lines.append("")
        step_num = 2
    else:
        step_num = 1

    lines.append(f"  STEP {step_num} - Integrate Individual Terms")
    lines.append("  " + "-" * 45)
    lines.append("")

    term_results = []
    for i, term in enumerate(terms, start=1):
        try:
            result = integrate_term(term)
        except ValueError:
            result = sympy.Symbol("?")

        rule_name, rule_formula = identify_rule(term)
        explanation = _get_rule_explanation(rule_name)

        lines.append(f"  Term {i} of {len(terms)}:")
        lines.append(f"  +-- Input       : integral( {fmt(term)} ) dx")
        lines.append(f"  +-- Rule        : {rule_name}")
        lines.append(f"  +-- Formula     : {rule_formula}")
        lines.append(f"  +-- Explanation :")
        for exp_line in explanation.split("\n"):
            lines.append(f"  |     {exp_line}")
        lines.append(f"  +-- Result      : {fmt(result)}")
        lines.append("")
        term_results.append(result)

    if multi:
        lines.append(f"  STEP {step_num + 1} - Combine and Simplify")
        lines.append("  " + "-" * 45)
        lines.append("")
        lines.append("  Combining all integrated terms:")
        lines.append(_join_terms(term_results))
        lines.append("")
        lines.append(f"  Simplified Form  : {fmt(antiderivative)}")
        lines.append("")

    # ── SECTION 4: Final Solution ──────────────────────────────────────────
    lines.append(SUB_DIVIDER)
    lines.append("SECTION 4: FINAL SOLUTION")
    lines.append(SUB_DIVIDER)
    lines.append("")
    lines.append("  INDEFINITE INTEGRAL:")
    lines.append("")
    lines.append(f"    integral( {expr_str} ) dx  =  {fmt(antiderivative)} + C")
    lines.append("")
    lines.append("  where C is an arbitrary constant of integration")
    lines.append("")

    # ── SECTION 5: Verification ────────────────────────────────────────────
    lines.append(SUB_DIVIDER)
    lines.append("SECTION 5: MATHEMATICAL VERIFICATION")
    lines.append(SUB_DIVIDER)
    lines.append("")
    lines.append("  Taking the derivative of our result should return the original function.")
    lines.append("")
    for vline in verification_msg.splitlines():
        lines.append(f"  {vline}")
    lines.append("")

    # ── SECTION 6: Summary ─────────────────────────────────────────────────
    lines.append(SUB_DIVIDER)
    lines.append("SECTION 6: SUMMARY")
    lines.append(SUB_DIVIDER)
    lines.append("")
    lines.append(f"  Original Expression    : {expr_str}")
    lines.append(f"  Antiderivative Found   : {fmt(antiderivative)}")
    lines.append(f"  Full Answer            : {fmt(antiderivative)} + C")
    lines.append(f"  Total Terms Processed  : {len(terms)}")
    lines.append(f"  Techniques Used        : {'Linearity + ' if multi else ''}Term-by-Term Analysis")
    lines.append("")
    lines.append(DIVIDER)
    lines.append("")

    return "\n".join(lines)