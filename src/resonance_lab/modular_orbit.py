"""Modular orbit and equality-autocorrelation benchmark observables."""

from __future__ import annotations

import numpy as np


def generate_orbit(N: int, base: int, K: int) -> np.ndarray:
    """Return ``[base**k mod N for k in range(K)]`` without order input."""
    if N <= 1:
        raise ValueError("N must be > 1.")
    if K < 1:
        raise ValueError("K must be positive.")

    orbit = np.empty(K, dtype=object)
    current = 1 % N
    base_mod = base % N
    orbit[0] = current
    for index in range(1, K):
        current = (current * base_mod) % N
        orbit[index] = current
    return orbit


def equality_autocorrelation(orbit: np.ndarray, max_lag: int) -> np.ndarray:
    """Measure equality at each lag across all available orbit pairs.

    ``result[lag]`` is one exactly when every observed pair separated by that
    lag is equal, and zero otherwise. The output includes lag zero.
    """
    values = np.asarray(orbit)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("orbit must be a non-empty one-dimensional array.")
    if max_lag < 0 or max_lag >= values.size:
        raise ValueError("max_lag must be between 0 and len(orbit) - 1.")

    return np.array(
        [np.all(values[lag:] == values[: values.size - lag]) for lag in range(max_lag + 1)],
        dtype=np.int8,
    )


def autocorrelation_spectrum(
    autocorrelation: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Return nonnegative FFT frequencies and the power spectrum of the lags."""
    values = np.asarray(autocorrelation, dtype=float)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("autocorrelation must be a non-empty one-dimensional array.")

    frequencies = np.fft.rfftfreq(values.size)
    spectrum = np.abs(np.fft.rfft(values)) ** 2
    return frequencies, spectrum