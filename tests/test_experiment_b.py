"""Tests for Experiment B's dual null evaluator."""

import numpy as np

from resonance_lab.experiments.b_factor_selectivity import evaluate_operator
from resonance_lab.operators import build_operator


def test_experiment_b_dual_null_execution():
    zeros = np.array([14.134725, 21.022040, 25.010858, 30.424876])
    p_true, q_true = 10007, 10009
    operator = build_operator(p_true * q_true, zeros, {})
    prime_controls = [
        9857, 9859, 9871, 9883, 9887, 9901, 9907, 9923, 9931, 9941,
        9967, 9973, 10007, 10009, 10037, 10039, 10061, 10067, 10069,
        10079, 10091, 10093, 10103, 10111, 10133, 10141, 10151, 10159,
    ]

    results = evaluate_operator(
        operator, p_true, q_true, prime_controls, M_samples=500
    )

    assert "p_hat_0a_continuous" in results
    assert "p_hat_0b_strict_prime" in results
    assert 0.0 <= results["p_hat_0a_continuous"] <= 1.0
    assert 0.0 <= results["p_hat_0b_strict_prime"] <= 1.0