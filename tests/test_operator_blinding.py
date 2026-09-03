import numpy as np
import pytest

from resonance_lab.circularity import CircularityViolationError
from resonance_lab.operators import build_operator


def test_operator_builder_blinded_signature_works_without_factors():
    zeros = np.array([14.134725, 21.022040, 25.010858])
    op = build_operator(100160063, zeros, {"truncation_cutoff": 3})
    assert callable(op)
    assert isinstance(op(np.log(10007)), float)


def test_operator_builder_rejects_factor_injected_config():
    zeros = np.array([14.134725])
    with pytest.raises(CircularityViolationError):
        build_operator(100160063, zeros, {"p": 10007})
