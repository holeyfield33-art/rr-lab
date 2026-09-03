"""Tests for circularity isolation."""

import pytest

from resonance_lab.circularity import (
    CircularityViolationError,
    audit_operator_config,
)


def test_circularity_audit_rejects_forbidden_keys():
    with pytest.raises(CircularityViolationError):
        audit_operator_config({"phi_N": 100140048, "mode": "standard"})


def test_circularity_audit_allows_n_computable_params():
    assert audit_operator_config({"base_a": 2, "exponent_bound": 1000}) is True