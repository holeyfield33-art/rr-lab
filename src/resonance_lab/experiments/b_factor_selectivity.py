"""Experiment B: factor-selectivity test with dual null hypotheses."""

from __future__ import annotations

from typing import Any, Callable, Iterable, Sequence

import numpy as np


def evaluate_factor_score(p: int, q: int, operator: Callable[[float], float]) -> float:
    """Compute S_factors = (R_N(ln p) + R_N(ln q)) / 2."""
    return float((operator(np.log(p)) + operator(np.log(q))) / 2.0)


def _prepare_prime_controls(
    p_true: int,
    q_true: int,
    candidate_primes: Sequence[int],
    log_min: float,
    log_max: float,
) -> list[int]:
    controls = [
        int(pr)
        for pr in candidate_primes
        if pr > 1 and log_min <= np.log(pr) <= log_max and pr not in (p_true, q_true)
    ]
    if len(controls) < 2:
        raise ValueError("Insufficient candidate prime controls in window I_N.")
    return controls


def run_experiment_b_single(
    operator: Callable[[float], float],
    p_true: int,
    q_true: int,
    candidate_primes: Sequence[int],
    M_samples: int = 5000,
    rng: np.random.Generator | None = None,
) -> dict[str, Any]:
    """Run Experiment B for one semiprime with H0a and H0b."""
    if rng is None:
        rng = np.random.default_rng(42)

    N = int(p_true) * int(q_true)
    sqrt_N = np.sqrt(N)
    log_min, log_max = np.log(sqrt_N / 2.0), np.log(sqrt_N * 2.0)

    S_target = evaluate_factor_score(p_true, q_true, operator)

    log_x = rng.uniform(log_min, log_max, size=M_samples)
    log_y = rng.uniform(log_min, log_max, size=M_samples)
    null_scores_0a = np.array([(operator(x) + operator(y)) / 2.0 for x, y in zip(log_x, log_y)])
    p_hat_0a = float((1 + np.sum(null_scores_0a >= S_target)) / (M_samples + 1))

    controls = _prepare_prime_controls(p_true, q_true, candidate_primes, log_min, log_max)
    null_scores_0b = np.empty(M_samples, dtype=float)
    for idx in range(M_samples):
        p_rand, q_rand = rng.choice(controls, size=2, replace=False)
        null_scores_0b[idx] = evaluate_factor_score(int(p_rand), int(q_rand), operator)
    p_hat_0b = float((1 + np.sum(null_scores_0b >= S_target)) / (M_samples + 1))

    return {
        "N": N,
        "p_true": int(p_true),
        "q_true": int(q_true),
        "S_factors": float(S_target),
        "p_hat_0a_continuous": p_hat_0a,
        "p_hat_0b_strict_prime": p_hat_0b,
        "mean_null_0b": float(np.mean(null_scores_0b)),
        "std_null_0b": float(np.std(null_scores_0b)),
    }


def evaluate_operator(
    operator: Callable[[float], float],
    p_true: int,
    q_true: int,
    prime_controls: Sequence[int],
    M_samples: int = 5000,
    rng: np.random.Generator | None = None,
) -> dict[str, Any]:
    """Evaluate a pre-built blinded operator against hidden factors."""
    return run_experiment_b_single(
        operator=operator,
        p_true=p_true,
        q_true=q_true,
        candidate_primes=prime_controls,
        M_samples=M_samples,
        rng=rng,
    )


def _ks_uniform_statistic(p_values: Iterable[float]) -> tuple[float, float]:
    """Return KS statistic and asymptotic p-value against Uniform[0,1]."""
    sample = np.sort(np.array(list(p_values), dtype=float))
    n = sample.size
    if n == 0:
        raise ValueError("Need at least one p-value for KS test.")

    i = np.arange(1, n + 1, dtype=float)
    d_plus = np.max(i / n - sample)
    d_minus = np.max(sample - (i - 1) / n)
    d_stat = float(max(d_plus, d_minus))

    en = np.sqrt(n)
    lam = (en + 0.12 + 0.11 / en) * d_stat
    terms = np.array([(-1) ** (k - 1) * np.exp(-2 * (k**2) * (lam**2)) for k in range(1, 101)])
    p_val = float(np.clip(2 * np.sum(terms), 0.0, 1.0))
    return d_stat, p_val


def run_experiment_b_suite(
    operator_factory: Callable[[int], Callable[[float], float]],
    semiprime_cases: Sequence[tuple[int, int]],
    prime_controls: Sequence[int],
    M_samples: int = 5000,
    seed: int = 42,
) -> dict[str, Any]:
    """Run Experiment B over a preregistered semiprime suite and test p-value uniformity."""
    if not semiprime_cases:
        raise ValueError("semiprime_cases must be non-empty.")

    rng = np.random.default_rng(seed)
    case_results: list[dict[str, Any]] = []
    p_values: list[float] = []

    for p_true, q_true in semiprime_cases:
        op = operator_factory(int(p_true) * int(q_true))
        result = evaluate_operator(
            operator=op,
            p_true=p_true,
            q_true=q_true,
            prime_controls=prime_controls,
            M_samples=M_samples,
            rng=rng,
        )
        case_results.append(result)
        p_values.append(result["p_hat_0b_strict_prime"])

    ks_stat, ks_pvalue = _ks_uniform_statistic(p_values)
    return {
        "cases": case_results,
        "p_values_h0b": p_values,
        "ks_statistic_h0b_uniformity": ks_stat,
        "ks_pvalue_h0b_uniformity": ks_pvalue,
    }
