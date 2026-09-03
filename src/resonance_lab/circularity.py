"""Circularity audit for factor leakage.

Allows N-computable operations (for example modular arithmetic modulo N),
while forbidding factor-equivalent leakage such as phi/lambda/order/CRT data
or factor-parameterized inputs.
"""

from __future__ import annotations

from typing import Any


class CircularityViolationError(Exception):
    """Raised when operator configuration contains factor-derived information."""


_FORBIDDEN_CANONICAL_KEYS = {
    "p",
    "q",
    "phi_n",
    "phin",
    "lambda_n",
    "lambdan",
    "order",
    "order_n",
    "order_p",
    "order_q",
    "modular_order",
    "crt",
    "crt_coeff",
    "crt_coeffs",
    "crt_decomposition",
    "factor",
    "factors",
    "factor_list",
    "prime_factors",
    "primes_tuple",
    "pq",
    "factor_seed",
    "factor_init",
}


def _normalize_key(name: str) -> str:
    return "".join(ch.lower() for ch in name if ch.isalnum() or ch == "_")


def _scan_keys(value: Any, path: str = "") -> list[str]:
    found: list[str] = []

    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            normalized = _normalize_key(key_text)
            current_path = f"{path}.{key_text}" if path else key_text
            if normalized in _FORBIDDEN_CANONICAL_KEYS:
                found.append(current_path)
            found.extend(_scan_keys(item, current_path))
    elif isinstance(value, (list, tuple, set)):
        for idx, item in enumerate(value):
            current_path = f"{path}[{idx}]"
            found.extend(_scan_keys(item, current_path))

    return found


def audit_operator_config(config: dict[str, Any]) -> bool:
    """Validate that operator config does not contain factor-derived leakage."""
    violations = _scan_keys(config)
    if violations:
        raise CircularityViolationError(
            "Circularity audit failed; forbidden factor-derived keys found: "
            + ", ".join(violations)
        )
    return True
