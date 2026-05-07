"""
formatter.py - Converts raw SymPy string output into readable math notation.
Week 11 - Additional polish for fractional powers and product notation.
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
        x**(3/2)        ->  x^(3/2)
        2*x**(3/2)/3    ->  (2/3)x^(3/2)
    """
    s = str(expr)
    return _polish(s)


def _polish(s: str) -> str:
    """Applies all formatting rules to a raw SymPy string."""

    # exp(x) -> e^x
    s = s.replace("exp(x)", "e^x")
    s = s.replace("exp(-x)", "e^(-x)")

    # Inverse trig — before plain trig
    s = s.replace("atan(x)", "arctan(x)")
    s = s.replace("asin(x)", "arcsin(x)")
    s = s.replace("acos(x)", "arccos(x)")

    # log -> ln
    s = s.replace("log(x)", "ln(x)")
    s = s.replace("log(", "ln(")

    # x**n -> xⁿ for integer powers 2-9
    superscripts = {
        "2": "²", "3": "³", "4": "⁴", "5": "⁵",
        "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"
    }
    for n, sup in superscripts.items():
        s = s.replace(f"x**{n}", f"x{sup}")
        s = s.replace(f"x**(-{n})", f"x⁻{sup}")

    # Fractional powers: x**(3/2) -> x^(3/2)
    s = re.sub(r'x\*\*\(([^)]+)\)', r'x^(\1)', s)

    # Coefficient cleanup before fractional power: 2*x^(3/2)/3 -> (2/3)x^(3/2)
    s = re.sub(r'(\d+)\*x\^\((\d+/\d+)\)/(\d+)', r'(\1/\3)x^(\2)', s)

    # 3*x -> 3x (number * variable)
    s = re.sub(r'(\d)\*x', r'\1x', s)

    # Remove * between number and function names
    s = re.sub(
        r'(\d)\*(ln|sin|cos|tan|sec|csc|cot|sinh|cosh|tanh|arctan|arcsin|arccos|exp|sqrt)',
        r'\1\2', s)

    # x * trig/log/exp -> x·func (middle dot)
    s = re.sub(
        r'x\*(cos|sin|tan|ln|exp|arctan|arcsin|arccos|sinh|cosh|sqrt)',
        r'x·\1', s)

    # -1*x -> -x and 1*x -> x
    s = re.sub(r'(?<![0-9])-1\*x', '-x', s)
    s = re.sub(r'(?<![0-9])\b1\*x', 'x', s)

    # Clean up double spaces
    s = re.sub(r'  +', ' ', s)

    return s.strip()