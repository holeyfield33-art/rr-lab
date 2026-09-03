import numpy as np

from resonance_lab.experiments.b_factor_selectivity import (
    evaluate_operator,
    run_experiment_b_single,
    run_experiment_b_suite,
)


def test_run_experiment_b_single_returns_dual_null_metrics():
    operator = lambda t: float(np.cos(t))
    result = run_experiment_b_single(
        operator=operator,
        p_true=10007,
        q_true=10009,
        candidate_primes=[
            10007,
            10009,
            10037,
            10039,
            10061,
            10067,
            10069,
            10079,
            10091,
            10093,
            10099,
        ],
        M_samples=256,
        rng=np.random.default_rng(7),
    )

    assert result["N"] == 100160063
    assert 0.0 <= result["p_hat_0a_continuous"] <= 1.0
    assert 0.0 <= result["p_hat_0b_strict_prime"] <= 1.0


def test_evaluate_operator_matches_single_run_contract():
    operator = lambda t: float(np.sin(0.5 * t))
    result = evaluate_operator(
        operator=operator,
        p_true=10007,
        q_true=10009,
        prime_controls=[10037, 10039, 10061, 10067, 10069, 10079],
        M_samples=128,
        rng=np.random.default_rng(9),
    )
    assert set(["p_hat_0a_continuous", "p_hat_0b_strict_prime", "S_factors"]).issubset(result)


def test_run_experiment_b_suite_reports_uniformity_statistic():
    def operator_factory(_N: int):
        return lambda t: float(np.cos(t) + 0.25 * np.sin(t))

    result = run_experiment_b_suite(
        operator_factory=operator_factory,
        semiprime_cases=[(10007, 10009), (10037, 10039)],
        prime_controls=[10061, 10067, 10069, 10079, 10091, 10093, 10099, 10103],
        M_samples=64,
        seed=5,
    )

    assert len(result["cases"]) == 2
    assert len(result["p_values_h0b"]) == 2
    assert result["seed"] == 5
    assert 0.0 <= result["ks_statistic_h0b_uniformity"] <= 1.0
    assert 0.0 <= result["ks_pvalue_h0b_uniformity"] <= 1.0
