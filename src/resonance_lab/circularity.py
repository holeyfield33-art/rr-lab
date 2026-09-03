"""Circularity audit for factor-blind operator configuration."""

from typing import Any


class CircularityViolationError(Exception):
    """Raised when an operator configuration contains factor-derived data."""


FORBIDDEN_KEYS = {
    "p",
    "q",
    "p_true",
    "q_true",
    "phi_n",
    "lambda_n",
    "order_p",
    "order_q",
    "crt_coeff",
    "factor_list",
    "primes_tuple",
}


def audit_operator_config(config: dict[str, Any]) -> bool:
    """Reject configuration keys that require knowledge of the factors."""
    found_violations = [key for key in config if key.lower() in FORBIDDEN_KEYS]
    if found_violations:
        raise CircularityViolationError(
            "Circularity Audit Failed! Forbidden factor-derived keys found: "
            f"{found_violations}"
        )
    return True