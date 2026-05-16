
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import sympy
from sympy import Symbol, sin, cos, exp, log, tan, sinh, cosh

x = Symbol("x")


# ══════════════════════════════════════════════════════════════════════════════
# validator.py tests
# ══════════════════════════════════════════════════════════════════════════════

from core.validator import validate_input

class TestValidator:

    def test_empty_input_rejected(self):
        ok, msg, expr = validate_input("")
        assert ok is False
        assert "enter" in msg.lower()

    def test_whitespace_only_rejected(self):
        ok, msg, expr = validate_input("   ")
        assert ok is False

    def test_bad_syntax_rejected(self):
        ok, msg, expr = validate_input("???")
        assert ok is False
        assert expr is None

    def test_wrong_variable_rejected(self):
        ok, msg, expr = validate_input("3*y**2")
        assert ok is False
        assert "y" in msg

    def test_valid_polynomial_accepted(self):
        ok, msg, expr = validate_input("3*x^2")
        assert ok is True
        assert expr is not None

    def test_valid_trig_accepted(self):
        ok, msg, expr = validate_input("sin(x)")
        assert ok is True

    def test_valid_exponential_accepted(self):
        ok, msg, expr = validate_input("exp(x)")
        assert ok is True

    def test_valid_multiterm_accepted(self):
        ok, msg, expr = validate_input("3*x^2 + sin(x) - 4/x + exp(x)")
        assert ok is True

    def test_valid_hyperbolic_accepted(self):
        ok, msg, expr = validate_input("sinh(x)")
        assert ok is True

    def test_valid_inverse_trig_accepted(self):
        ok, msg, expr = validate_input("1/(1+x^2)")
        assert ok is True

    def test_constant_accepted(self):
        """Pure constants are valid — integral is kx."""
        ok, msg, expr = validate_input("5")
        assert ok is True

    def test_implicit_multiply_accepted(self):
        """3x^2 without * should still parse."""
        ok, msg, expr = validate_input("3x^2")
        assert ok is True

    def test_caret_power_accepted(self):
        """x^2 should be treated as x**2."""
        ok, msg, expr = validate_input("x^3")
        assert ok is True


# ══════════════════════════════════════════════════════════════════════════════
# engine.py tests
# ══════════════════════════════════════════════════════════════════════════════

from core.engine import compute_integral, get_terms, integrate_term

class TestEngine:

    def test_power_rule(self):
        _, _, expr = validate_input("x^2")
        result = compute_integral(expr)
        assert sympy.simplify(result - x**3/3) == 0

    def test_sin_integral(self):
        _, _, expr = validate_input("sin(x)")
        result = compute_integral(expr)
        assert sympy.simplify(result - (-cos(x))) == 0

    def test_cos_integral(self):
        _, _, expr = validate_input("cos(x)")
        result = compute_integral(expr)
        assert sympy.simplify(result - sin(x)) == 0

    def test_exp_integral(self):
        _, _, expr = validate_input("exp(x)")
        result = compute_integral(expr)
        assert sympy.simplify(result - exp(x)) == 0

    def test_reciprocal_integral(self):
        _, _, expr = validate_input("1/x")
        result = compute_integral(expr)
        assert sympy.simplify(result - log(x)) == 0

    def test_constant_integral(self):
        _, _, expr = validate_input("5")
        result = compute_integral(expr)
        assert sympy.simplify(result - 5*x) == 0

    def test_polynomial_integral(self):
        _, _, expr = validate_input("x^3 - 2*x + 5")
        result = compute_integral(expr)
        expected = x**4/4 - x**2 + 5*x
        assert sympy.simplify(result - expected) == 0

    def test_special_function_blocked(self):
        """exp(x^2) has no standard antiderivative — should raise ValueError."""
        _, _, expr = validate_input("exp(x^2)")
        with pytest.raises(ValueError, match="special"):
            compute_integral(expr)

    def test_x_to_x_blocked(self):
        """x^x has no closed-form antiderivative."""
        _, _, expr = validate_input("x^x")
        with pytest.raises(ValueError):
            compute_integral(expr)

    def test_get_terms_multiterm(self):
        _, _, expr = validate_input("x^2 + sin(x)")
        terms = get_terms(expr)
        assert len(terms) == 2

    def test_get_terms_single(self):
        _, _, expr = validate_input("sin(x)")
        terms = get_terms(expr)
        assert len(terms) == 1

    def test_integrate_term_power(self):
        result = integrate_term(x**2)
        assert sympy.simplify(result - x**3/3) == 0

    def test_integrate_term_sin(self):
        result = integrate_term(sin(x))
        assert sympy.simplify(result - (-cos(x))) == 0


# ══════════════════════════════════════════════════════════════════════════════
# parser.py tests
# ══════════════════════════════════════════════════════════════════════════════

from core.parser import identify_rule

class TestParser:

    def _rule(self, expr_str):
        _, _, expr = validate_input(expr_str)
        rule, _ = identify_rule(expr)
        return rule

    def test_constant_rule(self):
        assert self._rule("5") == "Constant Rule"

    def test_power_rule_simple(self):
        assert self._rule("x^2") == "Power Rule"

    def test_power_rule_with_coefficient(self):
        assert self._rule("3*x^2") == "Power Rule"

    def test_logarithmic_rule_reciprocal(self):
        assert self._rule("1/x") == "Logarithmic Rule"

    def test_logarithmic_rule_ln(self):
        assert self._rule("log(x)") == "Logarithmic Rule"

    def test_exponential_rule(self):
        assert self._rule("exp(x)") == "Exponential Rule"

    def test_trig_rule_sin(self):
        assert self._rule("sin(x)") == "Trigonometric Rule"

    def test_trig_rule_cos(self):
        assert self._rule("cos(x)") == "Trigonometric Rule"

    def test_trig_rule_tan(self):
        assert self._rule("tan(x)") == "Trigonometric Rule"

    def test_inverse_trig_arctan(self):
        assert self._rule("1/(1+x^2)") == "Inverse Trigonometric Rule"

    def test_hyperbolic_sinh(self):
        assert self._rule("sinh(x)") == "Hyperbolic Rule"

    def test_hyperbolic_cosh(self):
        assert self._rule("cosh(x)") == "Hyperbolic Rule"

    def test_ibp_x_sin(self):
        assert self._rule("x*sin(x)") == "Integration by Parts"

    def test_ibp_x_cos(self):
        assert self._rule("x*cos(x)") == "Integration by Parts"

    def test_ibp_x_exp(self):
        assert self._rule("x*exp(x)") == "Integration by Parts"

    def test_ibp_x_log(self):
        assert self._rule("x*log(x)") == "Integration by Parts"

    def test_sin_not_ibp(self):
        """sin(x) alone should not be IBP."""
        assert self._rule("sin(x)") != "Integration by Parts"

    def test_polynomial_not_ibp(self):
        """3*x^2 should be Power Rule, not IBP or Constant Multiple."""
        assert self._rule("3*x^2") == "Power Rule"


# ══════════════════════════════════════════════════════════════════════════════
# formatter.py tests
# ══════════════════════════════════════════════════════════════════════════════

from core.formatter import fmt

class TestFormatter:

    def _fmt(self, expr_str):
        return fmt(sympy.parse_expr(expr_str, transformations="all"))

    def test_power_superscript_2(self):
        assert "x²" in self._fmt("x**2")

    def test_power_superscript_3(self):
        assert "x³" in self._fmt("x**3")

    def test_exp_notation(self):
        assert "e^x" in self._fmt("exp(x)")

    def test_log_to_ln(self):
        assert "ln(x)" in self._fmt("log(x)")

    def test_atan_to_arctan(self):
        assert "arctan(x)" in self._fmt("atan(x)")

    def test_asin_to_arcsin(self):
        assert "arcsin(x)" in self._fmt("asin(x)")

    def test_coefficient_multiply_removed(self):
        result = self._fmt("3*x**2")
        assert "3*x" not in result
        assert "3x" in result

    def test_number_times_ln_cleaned(self):
        result = self._fmt("4*log(x)")
        assert "4*ln" not in result
        assert "4ln" in result

    def test_negative_power(self):
        """1/x should not show ** notation."""
        result = self._fmt("-1/x")
        assert result == "-1/x"


# ══════════════════════════════════════════════════════════════════════════════
# verifier.py tests
# ══════════════════════════════════════════════════════════════════════════════

from core.verifier import verify
from core.engine import compute_integral

class TestVerifier:

    def _verify(self, expr_str):
        _, _, expr = validate_input(expr_str)
        integral = compute_integral(expr)
        is_correct, msg = verify(expr, integral)
        return is_correct, msg

    def test_power_verifies(self):
        ok, _ = self._verify("x^2")
        assert ok is True

    def test_sin_verifies(self):
        ok, _ = self._verify("sin(x)")
        assert ok is True

    def test_exp_verifies(self):
        ok, _ = self._verify("exp(x)")
        assert ok is True

    def test_multiterm_verifies(self):
        ok, _ = self._verify("3*x^2 + sin(x) - 4/x + exp(x)")
        assert ok is True

    def test_ibp_verifies(self):
        ok, _ = self._verify("x*sin(x)")
        assert ok is True

    def test_hyperbolic_verifies(self):
        ok, _ = self._verify("sinh(x) + cosh(x)")
        assert ok is True

    def test_inverse_trig_verifies(self):
        ok, _ = self._verify("1/(1+x^2)")
        assert ok is True

    def test_pass_message_contains_ok(self):
        _, msg = self._verify("x^2")
        assert "PASSED" in msg or "OK" in msg

    def test_verification_msg_is_string(self):
        _, msg = self._verify("sin(x)")
        assert isinstance(msg, str)
        assert len(msg) > 0


# ══════════════════════════════════════════════════════════════════════════════
# Integration tests — full pipeline
# ══════════════════════════════════════════════════════════════════════════════

from core.trail_logger import build_trail

class TestFullPipeline:

    def _run(self, expr_str):
        ok, err, expr = validate_input(expr_str)
        assert ok is True, f"Validation failed for '{expr_str}': {err}"
        integral = compute_integral(expr)
        is_correct, vmsg = verify(expr, integral)
        trail = build_trail(expr, integral, vmsg)
        return integral, is_correct, trail

    def test_pipeline_polynomial(self):
        _, ok, trail = self._run("x^2")
        assert ok is True
        assert "SECTION 4" in trail
        assert "VERIFICATION" in trail

    def test_pipeline_multiterm(self):
        _, ok, trail = self._run("3*x^2 + sin(x)")
        assert ok is True
        assert "SECTION 1" in trail
        assert "SECTION 6" in trail

    def test_pipeline_ibp(self):
        _, ok, trail = self._run("x*sin(x)")
        assert ok is True
        assert "Integration by Parts" in trail

    def test_pipeline_hyperbolic(self):
        _, ok, trail = self._run("sinh(x)")
        assert ok is True
        assert "Hyperbolic Rule" in trail

    def test_pipeline_inverse_trig(self):
        _, ok, trail = self._run("1/(1+x^2)")
        assert ok is True
        assert "Inverse Trigonometric Rule" in trail

    def test_trail_contains_final_answer(self):
        _, _, trail = self._run("x^2")
        assert "FINAL SOLUTION" in trail

    def test_trail_contains_given(self):
        _, _, trail = self._run("sin(x)")
        assert "GIVEN" in trail or "FUNCTION ANALYSIS" in trail

    def test_error_on_special_function(self):
        ok, err, expr = validate_input("exp(x^2)")
        assert ok is True  # valid syntax
        with pytest.raises(ValueError):
            compute_integral(expr)

    def test_error_on_empty(self):
        ok, err, expr = validate_input("")
        assert ok is False
        assert expr is None