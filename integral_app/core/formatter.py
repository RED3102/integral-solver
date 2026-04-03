"""
formatter.py - Converts raw SymPy string output into readable math notation.
"""

import re


def fmt(expr) -> str:
    """
    Takes a SymPy expression and returns a clean readable string.
    Examples:
        x**3            ->  x³
        x**2            ->  x²
        3*x             ->  3x
        log(x)          ->  ln(x)
        exp(x)          ->  e^x
        atan(x)         ->  arctan(x)
        asin(x)         ->  arcsin(x)
        x*cos(x)        ->  x·cos(x)
    """
    s = str(expr)
    return _polish(s)


def _polish(s: str) -> str:
    """Applies all formatting rules to a raw SymPy string."""

    # exp(x) -> e^x  (before other substitutions)
    s = s.replace("exp(x)", "e^x")
    s = s.replace("exp(-x)", "e^(-x)")

    # Inverse trig — must come before plain trig replacements
    s = s.replace("atan(x)", "arctan(x)")
    s = s.replace("asin(x)", "arcsin(x)")
    s = s.replace("acos(x)", "arccos(x)")

    # log -> ln
    s = s.replace("log(x)", "ln(x)")
    s = s.replace("log(", "ln(")

    # x**n -> xⁿ for common integer powers
    superscripts = {
        "2": "²", "3": "³", "4": "⁴", "5": "⁵",
        "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"
    }
    for n, sup in superscripts.items():
        s = s.replace(f"x**{n}", f"x{sup}")
        s = s.replace(f"x**(-{n})", f"x⁻{sup}")

    # x**(1/n) fractions — strip ** and use ^
    s = re.sub(r'x\*\*\(([^)]+)\)', r'x^(\1)', s)

    # 3*x -> 3x  (number * variable)
    s = re.sub(r'(\d)\*x', r'\1x', s)

    # Remove * between number and ln/sin/cos etc.
    s = re.sub(r'(\d)\*(ln|sin|cos|tan|sec|csc|cot|sinh|cosh|tanh|arctan|arcsin|arccos|exp)', r'\1\2', s)

    # x * trig/log/exp  ->  x·func  (middle dot instead of asterisk)
    s = re.sub(r'x\*(cos|sin|tan|ln|exp|arctan|arcsin|arccos|sinh|cosh)', r'x·\1', s)

    # Clean up double spaces
    s = re.sub(r'  +', ' ', s)

    return s.strip()