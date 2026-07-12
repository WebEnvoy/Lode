#!/usr/bin/env python3
"""Validate Core-readable runtime-boundary fields in the Lode registry."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


TARGET_REFS = {
    "lode://site-capability/xiaohongshu/search-notes@0.1.0",
    "lode://site-capability/xiaohongshu/read-note-detail@0.1.0",
    "lode://site-capability/xiaohongshu/publish-note-precheck@0.1.0",
    "lode://site-capability/boss/job-search@0.1.0",
    "lode://site-capability/boss/read-job-detail@0.1.1",
    "lode://site-capability/boss/greet-precheck@0.1.0",
}

REQUIRED_ENTRY_KEYS = {
    "site_slug",
    "task_kind",
    "capability_id",
    "operation_id",
    "operation_mode",
    "runtime_execution",
    "required_browser_session",
    "identity_profile_requirements",
    "evidence_requirements",
    "write_precheck_boundary",
    "failure_taxonomy_refs",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def issue(errors: list[dict[str, str]], path: str, message: str) -> None:
    errors.append({"path": path, "message": message})


def require_keys(errors: list[dict[str, str]], obj: dict[str, Any], keys: set[str], path: str) -> None:
    missing = sorted(keys - set(obj))
    if missing:
        issue(errors, path, f"missing keys: {', '.join(missing)}")


def validate_boundary(errors: list[dict[str, str]], item: dict[str, Any], path: str) -> None:
    require_keys(errors, item, REQUIRED_ENTRY_KEYS, path)
    if item.get("runtime_execution") != "out_of_scope":
        issue(errors, f"{path}.runtime_execution", "must be out_of_scope")

    session = item.get("required_browser_session")
    if not isinstance(session, dict) or session.get("required") is not True:
        issue(errors, f"{path}.required_browser_session", "must require a Harbor-owned browser session")
    elif not session.get("required_fact_keys"):
        issue(errors, f"{path}.required_browser_session.required_fact_keys", "must list required Harbor facts")

    identity = item.get("identity_profile_requirements")
    if not isinstance(identity, dict) or not identity.get("identity_profile_kind"):
        issue(errors, f"{path}.identity_profile_requirements", "must declare identity profile kind")

    evidence = item.get("evidence_requirements")
    if not isinstance(evidence, dict) or evidence.get("evidence_ref_policy") != "refs_only_no_inline_bodies":
        issue(errors, f"{path}.evidence_requirements", "must require refs-only evidence")

    failure_refs = item.get("failure_taxonomy_refs")
    if not isinstance(failure_refs, dict) or not failure_refs.get("classes"):
        issue(errors, f"{path}.failure_taxonomy_refs", "must expose failure classes")

    write_pre = item.get("write_precheck_boundary")
    if not isinstance(write_pre, dict) or write_pre.get("submitted") is not False:
        issue(errors, f"{path}.write_precheck_boundary.submitted", "must be false")
    if isinstance(write_pre, dict) and item.get("operation_mode") == "validate_only":
        if write_pre.get("no_submit_guard") != "active" or write_pre.get("true_write_execution") != "blocked":
            issue(errors, f"{path}.write_precheck_boundary", "validate_only packages must be no-submit and blocked")


def validate_query_fixture(errors: list[dict[str, str]], query: dict[str, Any]) -> None:
    seen: set[str] = set()
    for q_index, query_item in enumerate(query.get("queries", [])):
        for r_index, result in enumerate(query_item.get("results", [])):
            ref = result.get("package_ref")
            if ref not in TARGET_REFS:
                continue
            seen.add(ref)
            validate_boundary(errors, result, f"registry/local-query.fixture.json#queries[{q_index}].results[{r_index}]")
    missing = sorted(TARGET_REFS - seen)
    if missing:
        issue(errors, "registry/local-query.fixture.json", f"missing target results: {', '.join(missing)}")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    registry = load_json(root / "registry/local-packages.json")
    query = load_json(root / "registry/local-query.fixture.json")
    errors: list[dict[str, str]] = []

    entries = {entry.get("package_ref"): entry for entry in registry.get("entries", []) if isinstance(entry, dict)}
    for ref in sorted(TARGET_REFS):
        entry = entries.get(ref)
        if not isinstance(entry, dict):
            issue(errors, "registry/local-packages.json", f"missing target entry: {ref}")
            continue
        validate_boundary(errors, entry, f"registry/local-packages.json#{ref}")

    contract = registry.get("core_consumption_contract")
    if not isinstance(contract, dict) or contract.get("runtime_execution") != "out_of_scope":
        issue(errors, "registry/local-packages.json#core_consumption_contract", "must declare out-of-scope runtime execution")
    validate_query_fixture(errors, query)

    report = {
        "schema_version": "lode-runtime-boundary-validation.v0",
        "status": "failed" if errors else "passed",
        "checked_package_refs": sorted(TARGET_REFS),
        "errors": errors,
    }
    json.dump(report, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
