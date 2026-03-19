"""
validator.py - Validates user input before symbolic processing.
"""

import sympy
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


def validate_input(raw_input: str):
    """
    Validates the raw string from the user input field.
    Returns (is_valid, error_message, parsed_expression).
    """
    stripped = raw_input.strip()

    # Check 1: empty input
    if not stripped:
        return False, "Please enter a function before clicking Integrate.", None

    local_dict = {
        "x": sympy.Symbol("x"),
        "e": sympy.E,
        "pi": sympy.pi,
        "sin": sympy.sin,
        "cos": sympy.cos,
        "tan": sympy.tan,
        "exp": sympy.exp,
        "ln": sympy.ln,
        "log": sympy.log,
        "sqrt": sympy.sqrt,
    }

    # Check 2: parse expression
    try:
        expr = parse_expr(stripped, local_dict=local_dict, transformations=TRANSFORMATIONS)
    except Exception:
        return (
            False,
            f"Could not read '{stripped}' as a valid expression.\n"
            "Check your syntax — use * for multiplication and ^ for powers.\n"
            "Example: 3*x^2 + sin(x)",
            None,
        )

    # Check 3: must contain x
    x = sympy.Symbol("x")
    if x not in expr.free_symbols and expr.free_symbols:
        unknown = ", ".join(str(s) for s in expr.free_symbols)
        return (
            False,
            f"'{unknown}' is not recognised as a valid variable.\n"
            "Please write your function in terms of x.",
            None,
        )

    return True, "", expr