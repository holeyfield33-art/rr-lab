# riemann-resonance-lab

Minimal scaffold for reproducible resonance experiments with strict circularity controls.

## Current scope

- Treat **A1 prime-resonance** as an open hypothesis until verified by run artifacts.
- Implement **Experiment B** with dual nulls:
  - `H0a`: factors vs random continuous log-coordinates
  - `H0b`: factors vs random prime controls in the same log-window
- Enforce architectural blinding: operator builders receive `N`, never hidden factors `p, q`.
- Use verified balanced benchmark semiprime: `100160063 = 10007 * 10009`.

## Package layout

- `src/resonance_lab/circularity.py` — factor-leakage audit
- `src/resonance_lab/operators.py` — blinded operator factory
- `src/resonance_lab/experiments/b_factor_selectivity.py` — Experiment B harness
- `tests/` — focused validation tests
- `configs/experiment_b.toml` — baseline config
