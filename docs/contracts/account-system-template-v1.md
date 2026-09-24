# AccountSystem Public Template V1

Status: Lode-owned public template asset format. WebEnvoy's canonical product contract owns the AccountSystem concept and its required facts. This file owns only the shape and provenance requirements for public template assets stored in Lode; it does not define user-local definitions or their import, merge, identity binding, storage, or Runtime semantics.

The JSON Schema is [`schemas/account-system-template-v1.schema.json`](../../schemas/account-system-template-v1.schema.json). The first fixed template is [`account-systems/github/1.0.0.json`](../../account-systems/github/1.0.0.json), referenced as `lode://account-system/github@1.0.0`. [`registry/account-system-templates.json`](../../registry/account-system-templates.json), validated by [`schemas/account-system-template-index-v1.schema.json`](../../schemas/account-system-template-index-v1.schema.json), resolves that ref to its repository-relative file and pins the template bytes with SHA-256; consumers must verify the hash before import. A changed template requires a new version and index entry.

## Template contents

A template supplies an immutable, versioned starting point: stable `account_system_id`, `display_name`, related domains, products and administrative entry points, a login entry, optional evidence-backed identity guidance, known shared-login relationships, and template source/version. `identity_method` is omitted where Lode lacks a reviewed, bounded method; an empty `known_shared_login_relationships` list means no relationship is established by this template.

Entry points are informational HTTPS URLs. They do not authorize navigation, identity binding, account reads, or writes. `identity_method` may contain descriptive references only; it must not contain executable selectors, scripts, credentials, session data, Profile data, or runtime handles.

## Consumer boundary

WebEnvoy Core owns every user-local definition and its current revision. Import creates a local copy. Runtime behavior uses the local definition, never this public template directly. Accepting an update must preserve local changes unless the owner explicitly selects them for merge. Lode does not receive local definitions, account identifiers, account bindings, or merge decisions.

The `template_ref` and `version` identify Lode's public source only. A consumer must retain the selected template revision alongside its own local-definition identity; it must not turn a template update into a silent local overwrite. Changes to account-system identity or domain/product relationships require a new template version and owner-side conflict checks.

## GitHub template scope

The initial GitHub template is deliberately limited to `github.com`. It records the public sign-in route and account profile settings entry point as references; it does not infer enterprise-hosted domains, GitHub products on other domains, an identity extraction method, or shared login relationships. The `known_shared_login_relationships` list is empty. The source references support entry-point provenance and GitHub account creation context; they are not evidence of authenticated identity at Runtime.

No authentication, page observation, account operation, or live verification was performed to create this template. A site package can reference `lode://account-system/github@1.0.0`; only WebEnvoy Core can create and use a corresponding local definition.
