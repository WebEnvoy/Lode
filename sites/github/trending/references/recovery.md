# Recovery

- Wrong origin, language-filtered path, non-daily interval, stale target, or changed page shape: stop and keep the Run's failure/partial result. Owner may open the public daily Trending page and submit a new read task with a new idempotency key after fresh authorization.
- Truncated or incomplete snapshot text: retain `partial`/`unknown`; do not infer the omitted row, language, or star count.
- A dispatched Run with an unknown result: query/reconcile the original Run only. This task performs no external write, navigation, or retry.
- To repair a parser mismatch, save only a synthetic or appropriately redacted fixture, create a new package revision, rerun schema/script checks, and obtain owner code/source admission again. Never write page text, raw DOM, screenshots, account data, or Profile material into this package.
