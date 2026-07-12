# LODE-268 Implementation Contract

The public runtime input is only an opaque `detail_ref`. Core owns persisted provenance, freshness, single-use enforcement, and internal material resolution; Harbor owns browser, session, page, and evidence facts. Existing package input schemas are internal resolved-material contracts and are digest-bound, not caller-facing inputs. Lode runs neither component.
