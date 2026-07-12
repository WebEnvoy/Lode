# Implementation Contract

- Write ownership: registry runtime-consumption truths, their published schemas/fixtures/validators, and LODE-273 carriers.
- Required invariant: XHS enabled/current; BOSS disabled/deferred; all mismatches fail closed.
- Forbidden: capability asset deletion or relock, runtime implementation, production access, external write, sensitive material, or bypass.
- Verification: three self-tests, package validation, runtime-boundary validation, Python compile, JSON parse, diff and Loom checks.
