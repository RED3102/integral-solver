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
    stripped = raw_input.strip()

    # Check 1: empty input
    if not stripped:
        return False, "Input cannot be empty. Please enter a function f(x).", None

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
    except Exception as e:
        return False, f"Could not parse '{stripped}'.\nTip: Use * for multiplication, ^ for powers.\nDetails: {e}", None

    # Check 3: must contain x
    x = sympy.Symbol("x")
    if x not in expr.free_symbols and expr.free_symbols:
        unknown = ", ".join(str(s) for s in expr.free_symbols)
        return False, f"Unknown symbol(s): {unknown}. Please use x as the variable.", None

    return True, "", expr