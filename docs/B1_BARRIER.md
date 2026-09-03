# B1 Barrier

## Research State

- **B0: universal zeta negative control — PASS.**
- **Bpos: explicit divisibility positive control — PASS.**
- **Borbit: modular-order benchmark — PASS.**
- **B1: no defensible factor-selective zeta+N operator identified.**

B1 operator development is frozen pending a mathematically supported coupling.
The modular-order benchmark remains a standalone observable and is not promoted
into the `R_N(t)` operator interface.

## Four Information Channels

### Channel A: Divisibility / GCD

Examples include:

- direct gcd;
- the Jacobi zero branch; and
- Ramanujan gcd strata.

This channel is already represented by Bpos.

### Channel B: Group / Order Structure

Examples include:

- modular orbits;
- multiplicative order;
- Pollard p-1-like structure; and
- elliptic-curve group-order smoothness.

This channel is represented experimentally by Borbit where appropriate.

### Channel C: Universal Prime Spectrum

Zeta zeros and explicit formulas provide universal prime and prime-power
information.

The Riemann zero spectrum is independent of the supplied target N and
therefore contains no demonstrated factor selectivity by itself.

### Channel D: Smoothness / Relation Structure

Examples include:

- CFRAC;
- Dixon's method;
- the Quadratic Sieve; and
- the Number Field Sieve.

Relation matrices contain N-dependent modular and smoothness information
before the final gcd extraction. Channel D is not collapsed into Channel A
merely because factoring ends with a gcd.

## Channel D / Zeta Finding

Recent smooth-number theory provides approximate explicit-formula corrections
involving zeta zeros and prime powers for global smooth-number counts. The
relevant attribution is:

> Ofir Gorodetsky, “Smooth numbers and the Dickman ρ function,” *Journal
d’Analyse Mathématique* 151 (2023), 139–169.

The supported claims here are limited to the following:

- zeta zeros contribute to refined global smoothness estimates;
- these corrections are universal rather than target-N-specific;
- no derivation presently shows improvement to QS/NFS relation collection for a
  supplied N; and
- no change to either alpha or c in `L_N[alpha,c]` complexity has been
demonstrated.

This document does not claim O(1/log N) zero variance, C < 1.01 speedup, or a
proven reduction in the `L_N` constant c.

## Rejected Candidate Families

The following are currently rejected as B1 mechanisms:

- **Direct Jacobi coupling:** it is a divisibility test and belongs to Bpos,
  not a factor-blind zeta+N coupling.
- **Ramanujan weighting:** any factor-selective weighting must obtain its
  selectivity from an existing arithmetic channel rather than the universal
  spectrum.
- **Arbitrary modular-orbit to log-prime mapping:** no principled map from
  modular frequency to `t = log(p)` has been derived.
- **Unsupported Dirichlet-character factor selector:** a character with the
  required factor selectivity has not been derived without factor-equivalent
  input.
- **Arbitrary Mellin/Fourier rescaling:** a coordinate rescaling alone does not
  establish an N-specific factor coupling.
- **Unsupported Selberg/trace-formula analogy:** analogy is not a derivation of
  factor-selective information.
- **Zeta-weighted smoothness ranking without an N-specific derivation:** global
  smoothness corrections do not by themselves show improved relation
  collection for a supplied N.

## Barrier Statement

> Empirical/structural research finding: Every B1 proposal examined so far either obtains N-specificity from divisibility, group/order structure, or smoothness/relation structure, or remains a universal N-independent spectral observable. No mathematically derived coupling has been identified in which the universal Riemann-zeta spectrum adds new N-selective factor information.

**THIS IS NOT A THEOREM.** It does not claim that no possible fourth or fifth
channel can exist.

## Reopening Criteria

B1 operator development may resume only if a proposal provides at least one of:

1. a rigorous identity coupling N-specific arithmetic to zeta-zero data;
2. a genuinely new arithmetic information channel not reducible to the existing
   controls;
3. a derived prediction showing zeta information changes an N-specific relation
   probability; or
4. a complexity argument demonstrating more than universal prime-catalogue
   information.

Otherwise proposals remain theory notes only.
