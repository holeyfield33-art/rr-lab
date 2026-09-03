"""Tests for the modular-order orbit benchmark."""

import numpy as np

from resonance_lab.modular_orbit import (
    autocorrelation_spectrum,
    equality_autocorrelation,
    generate_orbit,
)


def test_equality_autocorrelation_detects_known_order_lags():
    # 2 has order 4 modulo 15: 1, 2, 4, 8, 1, ...
    orbit = generate_orbit(N=15, base=2, K=13)
    autocorrelation = equality_autocorrelation(orbit, max_lag=8)

    assert np.array_equal(orbit[:5], np.array([1, 2, 4, 8, 1]))
    assert autocorrelation[4] == 1
    assert autocorrelation[8] == 1
    assert autocorrelation[1] == 0
    assert autocorrelation[2] == 0
    assert autocorrelation[3] == 0


def test_generate_orbit_avoids_int64_intermediate_overflow():
    N = 4_000_000_007
    base = N - 2

    orbit = generate_orbit(N=N, base=base, K=3)

    assert orbit[0] == 1
    assert orbit[1] == N - 2
    assert orbit[2] == 4


def test_autocorrelation_spectrum_returns_matching_real_frequency_grid():
    autocorrelation = np.array([1, 0, 0, 1, 0, 0, 1], dtype=np.int8)
    frequencies, spectrum = autocorrelation_spectrum(autocorrelation)

    assert frequencies.shape == spectrum.shape
    assert frequencies[0] == 0.0
    assert np.all(spectrum >= 0.0)