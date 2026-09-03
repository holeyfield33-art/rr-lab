"""KNOWN DIVISIBILITY POSITIVE CONTROL for Experiment B calibration."""

import math

import numpy as np

from resonance_lab.experiments.b_factor_selectivity import run_experiment_b_single


def _jacobi_symbol(value: int, odd_modulus: int) -> int:
    """Compute the Jacobi symbol using the standard reciprocity algorithm."""
    if odd_modulus <= 0 or odd_modulus % 2 == 0:
        raise ValueError("odd_modulus must be positive and odd.")
    value %= odd_modulus
    result = 1
    while value:
        while value % 2 == 0:
            value //= 2
            if odd_modulus % 8 in (3, 5):
                result = -result
        value, odd_modulus = odd_modulus, value
        if value % 4 == odd_modulus % 4 == 3:
            result = -result
        value %= odd_modulus
    return result if odd_modulus == 1 else 0


def test_jacobi_zero_divisibility_control_is_strongly_selective():
    # Deliberately factor-aware calibration observable, not a candidate operator.
    p_true, q_true = 10007, 10009
    N = p_true * q_true

    assert _jacobi_symbol(p_true, N) == 0
    assert _jacobi_symbol(2 * p_true, N) == 0
    assert _jacobi_symbol(10037, N) != 0
    assert math.gcd(10037, N) == 1

    def known_divisibility_control(log_coordinate: float) -> float:
        value = int(round(np.exp(log_coordinate)))
        return float(_jacobi_symbol(value, N) == 0)

    result = run_experiment_b_single(
        operator=known_divisibility_control,
        p_true=p_true,
        q_true=q_true,
        candidate_primes=[
            10037,
            10039,
            10061,
            10067,
            10069,
            10079,
            10091,
            10093,
        ],
        M_samples=256,
        rng=np.random.default_rng(17),
    )

    assert result["S_factors"] == 1.0
    assert result["p_hat_0b_strict_prime"] == 1 / 257