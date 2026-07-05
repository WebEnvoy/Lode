# Plan

## Steps

1. Add refs-only repair draft and overlay/fork metadata fixtures to the sample read-only package.
2. Extend manifest, package lock, catalog metadata, and registry entry so App/Core can discover those assets through Lode-owned facts.
3. Extend failure mapping with post-check and evidence freshness classes needed by repair attribution.
4. Extend the offline validator for repair draft lifecycle, failure-to-repair mapping, overlay/fork boundary, package update acceptance, and sensitive material exclusion.
5. Run local package validation, batch registry validation, diff check, Loom validation, PR metadata preflight, hosted gate, merge, and closeout.

## Dependency Handling

- Hard dependency: Lode remains package/repair truth owner.
- Hard dependency: no raw or private runtime material enters Lode assets.
- Soft dependency: Core/App consume these facts later through fixtures and status projections.
- Convergence dependency: parent FR closeout must consume child Work Item issue states and merged PR evidence.

## Out of Scope

- Hosted registry, marketplace, hosted sync, crawler queue, real browser runtime execution, App install truth, Core run truth, Harbor session/evidence payload, and true write behavior.
