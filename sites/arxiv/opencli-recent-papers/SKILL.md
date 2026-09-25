# arXiv recent papers by category

This proposed package retains OpenCLI `1.8.8` `arxiv recent` input and parser/mapping semantics behind a WebEnvoy-managed anonymous HTTPS read. Do not treat source indexing or installation as code admission or execution authorization.

Task: `read-recent-category-papers`. It accepts only the pinned fields in `schemas/input.schema.json`, is bound to `https://export.arxiv.org`, and emits the pinned output schema. The candidate target type is `public_http_origin`, so `task.submit` must omit `target`; WebEnvoy binds the task to the exact task origin and authorized Profile. It never uses browser state, account credentials, cookies, local files, a proxy, raw sockets, or arbitrary code loading. Query the original Run after unknown or missing results; do not replay.

The script broker v1.1 and `network_read` are pending cross-repository contract acceptance and implementation. Use this package only as review material until those gates are satisfied.
