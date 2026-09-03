"""Tests for the blinded operator factory."""

import numpy as np

from resonance_lab.operators import build_operator


def test_operator_builder_blinding():
    zeros = np.array([14.134725, 21.022040, 25.010858])
    operator = build_operator(100160063, zeros, {"truncation_cutoff": 3})
    assert callable(operator)