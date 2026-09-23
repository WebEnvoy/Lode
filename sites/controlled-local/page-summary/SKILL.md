# Controlled Local Catalog page summary

This package declares one read-only, no-input task for an unauthenticated page served by the local WebEnvoy acceptance harness.

Use `read-page-summary` only when the current page is the controlled catalog at `http://127.0.0.1:4173/catalog`. The task uses the existing managed page snapshot capability. It has no package script, accepts no URL or page content as input, and performs no external egress.

Report the canonical URL, page title, and visible summary derived from the current Harbor snapshot. The package's post-check must pass for the task to be reported as available. If the current page, title, summary, or snapshot evidence does not match, stop and report the check failure. Do not navigate to another site, infer missing page content, or replace snapshot text with the expected phrase.
