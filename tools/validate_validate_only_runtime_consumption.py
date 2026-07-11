#!/usr/bin/env python3
"""Validate the two lock-bound validate-only runtime-consumption entries offline."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
TRUTH_PATH = ROOT / "registry/validate-only-runtime-consumption.json"
FIXTURE_PATH = ROOT / "registry/validate-only-runtime-consumption.fixture.json"
REGISTRY_PATH = ROOT / "registry/local-packages.json"
EXPECTED_OPERATIONS = {"xhs_publish_note_precheck", "boss_greet_precheck"}
EXPECTED_CONSUMERS = [
    {"repository": "WebEnvoy/Harbor", "purpose": "provide current page, identity, session, resource, and evidence refs"},
    {"repository": "WebEnvoy/WebEnvoy", "purpose": "admit and record an exact validate-only precheck"},
]
EXPECTED_REJECTIONS = {
    "unknown_operation", "package_lock_or_version_drift", "origin_or_page_drift",
    "non_validate_only_mode", "write_or_submit_requested", "missing_or_stale_resource_facts",
    "missing_or_stale_field_source_refs", "missing_evidence_or_post_check_refs",
    "missing_runtime_result_refs", "submitted_not_false", "challenge_or_risk_control",
}
REQUIRED_RUNTIME_REFS = [
    "merged_head_ref", "identity_ref", "session_ref", "run_ref", "result_ref",
    "evidence_refs", "post_check_ref",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def error(errors: list[str], path: str, message: str) -> None:
    errors.append(f"{path}: {message}")


def https_origin(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc) and parsed.path in {"", "/"} and not parsed.query and not parsed.fragment


def asset_ref(manifest: dict[str, Any], role: str) -> dict[str, Any] | None:
    return next((item for item in manifest.get("asset_refs", []) if item.get("role") == role), None)


def bind_asset(errors: list[str], entry: dict[str, Any], root: Path, manifest: dict[str, Any], section: str, role: str, id_key: str, version_key: str) -> dict[str, Any] | None:
    value = entry.get(section)
    ref = asset_ref(manifest, role)
    path = f"entries[{entry.get('operation_id')}].{section}"
    if not isinstance(value, dict) or ref is None or ref.get("status") != "present":
        error(errors, path, "required bound asset is missing")
        return None
    expected_path = str(root.relative_to(ROOT) / ref["path"])
    if value.get("path" if section != "evidence_and_post_check" else "post_check_path") != expected_path:
        error(errors, path, "asset path drifted from manifest")
    if value.get(id_key) != ref.get(id_key) or value.get(version_key) != ref.get(version_key):
        error(errors, path, "asset identity or version drifted from manifest")
    return load_json(root / ref["path"])


def validate_entry(errors: list[str], entry: dict[str, Any], registry_entry: dict[str, Any]) -> None:
    operation_id = entry.get("operation_id")
    path = f"entries[{operation_id}]"
    for key in ("package_ref", "lock_ref", "version", "site_slug", "capability_id", "operation_id", "operation_mode", "lifecycle"):
        if entry.get(key) != registry_entry.get(key):
            error(errors, f"{path}.{key}", "does not match local registry")
    if operation_id not in EXPECTED_OPERATIONS or entry.get("operation_mode") != "validate_only" or entry.get("lifecycle") != "proposed":
        error(errors, path, "must be an expected proposed validate-only operation")

    root = ROOT / registry_entry["package_path"]
    manifest = load_json(root / "manifest.json")
    lock = load_json(root / "package-lock.json")
    capability = manifest.get("capability", {})
    expected = {
        "package_ref": manifest.get("package_ref"), "lock_ref": lock.get("lock_ref"),
        "version": capability.get("version"), "operation_id": capability.get("operation_id"),
        "operation_mode": capability.get("operation_mode"), "lifecycle": capability.get("lifecycle"),
    }
    lock_values = {
        "package_ref": lock.get("package_ref"), "lock_ref": lock.get("lock_ref"),
        "version": lock.get("package_version"), "operation_id": lock.get("operation_id"),
        "operation_mode": lock.get("operation_mode"), "lifecycle": lock.get("lifecycle"),
    }
    for key, value in expected.items():
        if entry.get(key) != value or lock_values.get(key) != value:
            error(errors, f"{path}.{key}", "does not match pinned manifest and lock")

    origins = entry.get("allowed_origins")
    if origins != manifest.get("site", {}).get("supported_origins") or not origins or any(not https_origin(origin) for origin in origins):
        error(errors, f"{path}.allowed_origins", "must exactly bind canonical HTTPS manifest origins")

    page = entry.get("page_requirement", {})
    resources = bind_asset(errors, entry, root, manifest, "resource_requirements", "resource_requirements", "resource_requirements_id", "resource_requirements_version")
    if resources:
        profile = resources.get("resource_requirement_profiles", [None])[0] or {}
        facts = [item.get("fact_key") for item in profile.get("required_harbor_facts", [])]
        if entry["resource_requirements"].get("required_harbor_fact_keys") != facts:
            error(errors, f"{path}.resource_requirements", "must bind every required Harbor fact")
        if page.get("required_page_fact") not in facts or page.get("challenge_fact") != "safety.challenge.absent" or page.get("page_change_policy") != "reject" or not page.get("required_visible_fields"):
            error(errors, f"{path}.page_requirement", "must bind the package page fact, visible fields, and reject page drift")

    freshness = entry.get("freshness", {})
    if freshness.get("policy") != "current_execution_window" or freshness.get("stale_policy") != "reject" or set(freshness.get("applies_to", [])) != {"page_ref", "identity_ref", "session_ref", "resource_refs", "field_source_refs", "evidence_refs"}:
        error(errors, f"{path}.freshness", "must reject stale page, identity, session, resource, field, or evidence refs")

    fields = entry.get("field_sources", {})
    visible = page.get("required_visible_fields", [])
    if fields.get("source_ref_policy") != "summary_refs_only" or set(fields.get("required_fields", {})) != set(visible) or any(not refs for refs in fields.get("required_fields", {}).values()) or fields.get("missing_or_unreferenced_field_policy") != "reject":
        error(errors, f"{path}.field_sources", "must bind every visible field to summary refs and reject missing refs")

    mapping = bind_asset(errors, entry, root, manifest, "failure_taxonomy", "failure_mapping", "failure_mapping_id", "failure_mapping_version")
    if mapping:
        classes = [item.get("lode_failure_class") for item in mapping.get("classes", [])]
        if entry["failure_taxonomy"].get("required_classes") != classes:
            error(errors, f"{path}.failure_taxonomy", "must bind the complete package taxonomy")

    post_check = bind_asset(errors, entry, root, manifest, "evidence_and_post_check", "post_check", "post_check_id", "post_check_version")
    evidence = entry.get("evidence_and_post_check", {})
    registry_evidence = registry_entry.get("evidence_requirements", {})
    if evidence.get("evidence_ref_policy") != "refs_only_no_inline_bodies" or evidence.get("required_ref_kinds") != registry_evidence.get("required_ref_kinds"):
        error(errors, f"{path}.evidence_and_post_check", "must bind exact refs-only registry evidence kinds")
    if post_check and evidence.get("required_post_check_fields") != post_check.get("result_contract", {}).get("required_fields"):
        error(errors, f"{path}.evidence_and_post_check", "must bind the complete post-check result contract")

    runtime = entry.get("runtime_result_requirements", {})
    safety = entry.get("safety_boundary", {})
    if runtime.get("required_refs") != REQUIRED_RUNTIME_REFS or runtime.get("result_field") != "submitted" or runtime.get("required_result_value") is not False:
        error(errors, f"{path}.runtime_result_requirements", "must require current merged-head/runtime/evidence refs and submitted=false")
    if safety.get("no_submit_guard") != "active" or safety.get("submitted") is not False or safety.get("submitted_must_remain_false") is not True or not safety.get("blocked_external_actions"):
        error(errors, f"{path}.safety_boundary", "must preserve active no-submit and submitted=false")
    registry_boundary = registry_entry.get("write_precheck_boundary", {})
    if registry_boundary.get("submitted") is not False or registry_boundary.get("true_write_execution") != "blocked":
        error(errors, f"{path}.safety_boundary", "local registry does not preserve the write-precheck block")


def validate(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["truth: must be an object"]
    if data.get("schema_version") != "lode.validate-only-runtime-consumption.v0" or data.get("asset_owner") != "Lode":
        error(errors, "truth", "schema or owner is unsupported")
    boundary = data.get("consumer_boundary", {})
    if boundary.get("allowed_consumers") != EXPECTED_CONSUMERS or boundary.get("runtime_execution") != "out_of_scope" or boundary.get("live_success") != "not_proven_by_lode":
        error(errors, "consumer_boundary", "must preserve exact consumers and Lode non-runner/non-live-success boundary")
    fail_closed = data.get("fail_closed")
    if not isinstance(fail_closed, dict) or set(fail_closed) != EXPECTED_REJECTIONS or any(value != "reject" for value in fail_closed.values()):
        error(errors, "fail_closed", "must contain exactly the required reject conditions")
    entries = data.get("entries")
    if not isinstance(entries, list) or len(entries) != 2 or {item.get("operation_id") for item in entries if isinstance(item, dict)} != EXPECTED_OPERATIONS:
        error(errors, "entries", "must contain exactly both known operations")
        return errors
    registry = load_json(REGISTRY_PATH)
    registry_entries = {item.get("operation_id"): item for item in registry.get("entries", []) if item.get("operation_id") in EXPECTED_OPERATIONS}
    if set(registry_entries) != EXPECTED_OPERATIONS:
        error(errors, "registry", "both operations must exist exactly once")
        return errors
    for entry in entries:
        validate_entry(errors, entry, registry_entries[entry["operation_id"]])
    return errors


def self_test(data: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("unknown operation", lambda value: value["entries"][0].__setitem__("operation_id", "unknown")),
        ("lock drift", lambda value: value["entries"][0].__setitem__("lock_ref", "lode://lock/drift")),
        ("version drift", lambda value: value["entries"][0].__setitem__("version", "0.2.0")),
        ("origin drift", lambda value: value["entries"][0].__setitem__("allowed_origins", ["http://example.com"])),
        ("page drift", lambda value: value["entries"][0]["page_requirement"].__setitem__("required_page_fact", "page.changed")),
        ("challenge present", lambda value: value["entries"][0]["page_requirement"].__setitem__("challenge_fact", "safety.challenge.present")),
        ("write mode", lambda value: value["entries"][0].__setitem__("operation_mode", "write")),
        ("stale facts", lambda value: value["entries"][0]["freshness"].__setitem__("policy", "stale_allowed")),
        ("missing field refs", lambda value: value["entries"][0]["field_sources"]["required_fields"].__setitem__("title_input", [])),
        ("missing evidence", lambda value: value["entries"][0]["evidence_and_post_check"].__setitem__("required_ref_kinds", [])),
        ("missing runtime ref", lambda value: value["entries"][0]["runtime_result_requirements"]["required_refs"].pop()),
        ("submitted true", lambda value: value["entries"][0]["safety_boundary"].__setitem__("submitted", True)),
        ("submit requested", lambda value: value["entries"][0]["safety_boundary"].__setitem__("no_submit_guard", "inactive")),
        ("arbitrary consumer", lambda value: value["consumer_boundary"]["allowed_consumers"].append({"repository": "other", "purpose": "run"})),
    ]
    failures: list[str] = []
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        if not validate(candidate):
            failures.append(f"self-test did not reject {name}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    data = load_json(TRUTH_PATH)
    errors = validate(data)
    fixture = load_json(FIXTURE_PATH)
    if fixture.get("accepted_operations") != sorted(EXPECTED_OPERATIONS) or fixture.get("expected_mode") != "validate_only" or fixture.get("expected_submitted") is not False or fixture.get("required_runtime_refs") != REQUIRED_RUNTIME_REFS:
        errors.append("fixture: acceptance identity drifted")
    if args.self_test and not errors:
        errors.extend(self_test(data))
    if errors:
        for item in errors:
            print(item)
        return 1
    print("validate-only runtime-consumption truth: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
