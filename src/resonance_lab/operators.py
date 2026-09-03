"""Operator construction with structural blinding."""

from __future__ import annotations

from typing import Any, Callable

import numpy as np

from resonance_lab.circularity import audit_operator_config


def build_operator(N: int, zeros: np.ndarray, config: dict[str, Any]) -> Callable[[float], float]:
    """Build a blinded operator R_N(t) from N and zeta zero data only."""
    return build_universal_zeta_operator(N=N, zeros=zeros, config=config)


def build_universal_zeta_operator(
    N: int,
    zeros: np.ndarray,
    config: dict[str, Any],
) -> Callable[[float], float]:
    """Build a baseline universal operator inspired by a zeta-zero cosine transform."""
    if N <= 1:
        raise ValueError("N must be > 1.")

    audit_operator_config(config)

    zeros = np.asarray(zeros, dtype=float)
    if zeros.size == 0:
        raise ValueError("zeros must be non-empty.")

    cutoff = int(config.get("truncation_cutoff", zeros.size))
    if cutoff <= 0:
        raise ValueError("truncation_cutoff must be positive.")

    active_zeros = zeros[: min(cutoff, zeros.size)]
    weights = 1.0 / np.sqrt(0.25 + active_zeros**2)

    def R_N(t: float) -> float:
        return float(np.sum(weights * np.cos(active_zeros * float(t))))

    return R_N
