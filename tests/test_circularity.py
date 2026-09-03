import pytest

from resonance_lab.circularity import CircularityViolationError, audit_operator_config


def test_circularity_audit_rejects_factor_derived_keys():
    config = {"window": {"phi_N": 100140048}, "mode": "baseline"}
    with pytest.raises(CircularityViolationError):
        audit_operator_config(config)


def test_circularity_audit_allows_n_computable_modular_arithmetic_fields():
    config = {
        "operation": "modular_exponentiation",
        "base": 2,
        "exponent_grid": [2, 4, 8],
        "modulus": "N",
    }
    assert audit_operator_config(config) is True
