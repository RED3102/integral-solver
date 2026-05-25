import re


_SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def _sup(n: str) -> str:
    """Convert a numeric string to Unicode superscript."""
    return n.translate(_SUP)


def fmt(expr) -> str:
    """
    Converts a SymPy expression to a clean, readable single-line string.
    No ** or bare ^ characters remain in the output.
    """
    s = str(expr)
    return _polish(s)


def _polish(s: str) -> str:

    # ── exp(x) → e^x  (before other subs) ───────────────────────────────
    s = s.replace("exp(x)", "eˣ")
    s = s.replace("exp(-x)", "e⁻ˣ")
    # exp(n*x)
    s = re.sub(r'exp\((-?\d+)\*x\)', lambda m: f"e^({m.group(1)}x)", s)

    # ── Inverse trig ─────────────────────────────────────────────────────
    s = s.replace("atan(x)", "arctan(x)")
    s = s.replace("asin(x)", "arcsin(x)")
    s = s.replace("acos(x)", "arccos(x)")

    # ── log → ln ─────────────────────────────────────────────────────────
    s = s.replace("log(x)", "ln(x)")
    s = s.replace("log(", "ln(")

    # ── sqrt cleanup ─────────────────────────────────────────────────────
    # sqrt(x) → √x
    s = s.replace("sqrt(x)", "√x")
    # 1/sqrt(x) → 1/√x
    s = s.replace("1/√x", "1/√x")

    # ── x**n → xⁿ  for integer powers ───────────────────────────────────
    def replace_xpow(m):
        n = m.group(1)
        if n.lstrip('-').isdigit():
            return "x" + _sup(n)
        return m.group(0)   # keep original if not simple integer

    s = re.sub(r'x\*\*\((-?\d+)\)', replace_xpow, s)   # x**(-2) → x⁻²
    s = re.sub(r'x\*\*(-?\d+)', replace_xpow, s)        # x**3 → x³

    # ── x**(p/q) → xᵖᐟq  readable fraction superscript ─────────────────
    # e.g. x**(3/2) → x^(3/2)  with superscripted fraction label
    def replace_frac_pow(m):
        p, q = m.group(1), m.group(2)
        return f"x^({p}/{q})"
    s = re.sub(r'x\*\*\((\d+)/(\d+)\)', replace_frac_pow, s)

    # ── Coefficient * x^(p/q) pattern: 2*x^(3/2)/3 → (2/3)x^(3/2) ──────
    s = re.sub(r'(\d+)\*x\^\((\d+/\d+)\)/(\d+)', r'(\1/\3)x^(\2)', s)

    # ── x**n remaining (powers > 9 not caught by superscript map) ────────
    # e.g. x**10 → x^10
    def replace_remaining_xpow(m):
        n = m.group(1)
        return f"x^{n}"
    s = re.sub(r'x\*\*(\d+)', replace_remaining_xpow, s)

    # ── General a**n  (non-x bases, integer power) ───────────────────────
    # e.g. 2**3 → 2³
    def replace_gen_pow(m):
        base, exp_val = m.group(1), m.group(2)
        if exp_val.lstrip('-').isdigit() and int(exp_val.lstrip('-')) <= 9:
            return base + _sup(exp_val)
        return f"{base}^{exp_val}"
    s = re.sub(r'(\w+)\*\*(-?\d+)', replace_gen_pow, s)

    # ── Remove * between number and variable/function ─────────────────────
    s = re.sub(r'(\d)\*x', r'\1x', s)
    s = re.sub(
        r'(\d)\*(ln|sin|cos|tan|sec|csc|cot|sinh|cosh|tanh|arctan|arcsin|arccos|√)',
        r'\1\2', s)

    # ── x · trig/log/exp → middle dot ────────────────────────────────────
    s = re.sub(
        r'x\*(cos|sin|tan|ln|eˣ|arctan|arcsin|arccos|sinh|cosh|√)',
        r'x·\1', s)

    # ── Clean up double spaces ────────────────────────────────────────────
    s = re.sub(r'  +', ' ', s)

    return s.strip()


# ── Input display conversion (used by app_ui for live preview) ────────────────

# Maps what user types → what displays in the entry field
INPUT_SUP_MAP = {
    '^0': '⁰', '^1': '¹', '^2': '²', '^3': '³', '^4': '⁴',
    '^5': '⁵', '^6': '⁶', '^7': '⁷', '^8': '⁸', '^9': '⁹',
}

# Maps display superscripts back to SymPy-parseable form
DISPLAY_TO_SYMPY = {v: f'^{k[1]}' for k, v in INPUT_SUP_MAP.items()}


def prettify_input(raw: str) -> tuple[str, int]:
    """
    Converts typed input like '3*x^2' to display form '3*x²'.
    Handles single and double digit exponents: x^10 -> x¹⁰.
    Returns (display_string, cursor_offset).
    """
    import re as _re
    def sup_digits(m):
        return _sup(m.group(1))
    # Replace ^digit(s) with superscript
    result = _re.sub(r'\^(\d+)', lambda m: _sup(m.group(1)), raw)
    offset = len(result) - len(raw)
    return result, offset


def display_to_raw(display: str) -> str:
    """
    Converts display form '3*x²' back to SymPy-parseable '3*x^2'.
    Called by validator before parsing.
    """
    import re as _re
    # Map each superscript digit back to normal digit
    _sup_rev = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")
    # Find runs of superscript characters and convert them
    def replace_sup_run(m):
        return "^" + m.group(0).translate(_sup_rev)
    result = _re.sub(r"[⁰¹²³⁴-⁹⁻]+", replace_sup_run, display)
    return result