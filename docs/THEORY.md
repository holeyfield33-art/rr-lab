# Theory Notes

This repository uses numerical observables inspired by zeta-zero/prime relationships.
Universal non-selectivity is treated as an empirical hypothesis tested across semiprime ensembles,
not as a proven theorem.

For a modular orbit `x_k = a^k mod N`, equality autocorrelation detects lags
that are multiples of the order `r = ord_N(a)` when those lags are in the
observation window. Straightforward orbit observation requires `O(r)` steps.
Classical specialized algorithms may improve particular cases, but birthday
collisions in a deterministic orbit do not by themselves establish a general
`O(sqrt(r))` exact order-finding algorithm or polynomial-time order finding in
`log(N)`.

The modular autocorrelation spectrum is a benchmark observable, not an
`R_N(t)` operator. No principled map to `t = log(p)` has been established, so
the B1 operator remains undefined.
