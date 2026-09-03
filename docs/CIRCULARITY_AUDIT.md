# Circularity Audit

The operator builder is structurally blinded:

- allowed inputs: `N`, zero spectrum, and audited config
- disallowed leakage: `p`, `q`, `phi(N)`, `lambda(N)`, known orders, CRT/factor-derived initializations
- explicitly allowed: `N`-computable operations such as modular arithmetic modulo `N`
