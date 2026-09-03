"""Factory functions for factor-blind spectral operators."""

from typing import Any, Callable

import numpy as np

from resonance_lab.circularity import audit_operator_config


def build_operator(
    N: int,
    zeros: np.ndarray,
    config: dict[str, Any],
) -> Callable[[float], float]:
    """Build an N-dependent spectral operator without factor access."""
    del N
    audit_operator_config(config)

    def operator(log_coordinate: float) -> float:
        weights = 1.0 / np.sqrt(0.25 + zeros**2)
        return float(np.sum(weights * np.cos(zeros * log_coordinate)))

    return operator