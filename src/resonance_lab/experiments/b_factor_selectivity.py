"""Experiment B: N-selective factor oracle test with dual nulls."""

from typing import Any, Callable, Optional

import numpy as np


def evaluate_factor_score(
    p: int,
    q: int,
    operator: Callable[[float], float],
) -> float:
    """Compute the joint resonance score for a candidate prime pair."""
    return (operator(np.log(p)) + operator(np.log(q))) / 2.0


def evaluate_operator(
    operator: Callable[[float], float],
    p_true: int,
    q_true: int,
    prime_controls: list[int],
    M_samples: int = 5000,
    rng: Optional[np.random.Generator] = None,
) -> dict[str, Any]:
    """Evaluate factor selectivity against continuous and prime nulls."""
    if M_samples < 1:
        raise ValueError("M_samples must be positive.")
    if rng is None:
        rng = np.random.default_rng(42)

    N = p_true * q_true
    sqrt_N = np.sqrt(N)
    log_min, log_max = np.log(sqrt_N / 2.0), np.log(sqrt_N * 2.0)
    target_score = evaluate_factor_score(p_true, q_true, operator)

    continuous_scores = np.array(
        [
            (operator(log_x) + operator(log_y)) / 2.0
            for log_x, log_y in zip(
                rng.uniform(log_min, log_max, M_samples),
                rng.uniform(log_min, log_max, M_samples),
            )
        ]
    )
    p_hat_0a = float(
        (1 + np.sum(continuous_scores >= target_score)) / (M_samples + 1)
    )

    filtered_primes = [
        prime
        for prime in prime_controls
        if log_min <= np.log(prime) <= log_max
        and prime not in (p_true, q_true)
    ]
    if len(filtered_primes) < 2:
        raise ValueError(
            f"Insufficient prime controls in window [{log_min:.2f}, {log_max:.2f}]."
        )

    prime_scores = np.array(
        [
            evaluate_factor_score(first, second, operator)
            for first, second in (
                rng.choice(filtered_primes, size=2, replace=False)
                for _ in range(M_samples)
            )
        ]
    )
    p_hat_0b = float((1 + np.sum(prime_scores >= target_score)) / (M_samples + 1))

    return {
        "N": N,
        "p_true": p_true,
        "q_true": q_true,
        "S_factors": target_score,
        "p_hat_0a_continuous": p_hat_0a,
        "p_hat_0b_strict_prime": p_hat_0b,
        "mean_null_0b": float(np.mean(prime_scores)),
        "std_null_0b": float(np.std(prime_scores)),
        "n_prime_controls": len(filtered_primes),
    }