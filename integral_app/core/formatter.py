import re

def fmt(expr) -> str:
    """
    Takes a SymPy expression and returns a clean readable string.
    Examples:
        x**3        ->  x³
        x**2        ->  x²
        3*x         ->  3x
        log(x)      ->  ln(x)
        exp(x)      ->  eˣ
        -cos(x)     ->  -cos(x)  (unchanged)
    """
    s = str(expr)
    return _polish(s)


def _polish(s: str) -> str:
    """Applies all formatting rules to a raw SymPy string."""

    # exp(x) -> eˣ  before anything else
    s = s = s.replace("exp(x)", "e^x")
    s = s = s.replace("exp(-x)", "e^(-x)")

    # log(x) -> ln(x)
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

    # x**(1/n) fractions — leave as-is, just strip the **
    s = re.sub(r'x\*\*\(([^)]+)\)', r'x^(\1)', s)

    # 3*x -> 3x  (remove * between number and variable)
    s = re.sub(r'(\d)\*x', r'\1x', s)
    # Remove * between number and ln/sin/cos etc.
    s = re.sub(r'(\d)\*(ln|sin|cos|tan|exp)', r'\1\2', s)

    # Clean up any double spaces
    s = re.sub(r'  +', ' ', s)

    return s.strip()