#!/usr/bin/env python3
"""Validate the two lock-bound validate-only runtime-consumption entries offline."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError
except ImportError:  # Reported as a validation failure below.
    Draft202012Validator = None
    SchemaError = Exception


ROOT = Path(__file__).resolve().parents[1]
TRUTH_PATH = ROOT / "registry/validate-only-runtime-consumption.json"
SCHEMA_PATH = ROOT / "registry/validate-only-runtime-consumption.schema.json"
FIXTURE_PATH = ROOT / "registry/validate-only-runtime-consumption.fixture.json"
REGISTRY_PATH = ROOT / "registry/local-packages.json"
EXPECTED_OPERATIONS = {"xhs_publish_note_precheck", "boss_greet_precheck"}
EXPECTED_ADMISSION = {
    "xhs_publish_note_precheck": {"enabled": True, "status": "current", "recheck_condition": "not_applicable"},
    "boss_greet_precheck": {"enabled": False, "status": "deferred_experimental", "recheck_condition": "deferred_milestone_scope_restored_with_current_head_review_and_runtime_live_evidence"},
}
EXPECTED_CONSUMERS = [
    {"repository": "WebEnvoy/Harbor", "purpose": "provide current page, identity, session, resource, and evidence refs"},
    {"repository": "WebEnvoy/WebEnvoy", "purpose": "admit and record an exact validate-only precheck"},
]
EXPECTED_REJECTIONS = {
    "unknown_operation", "package_lock_or_version_drift", "origin_or_page_drift",
    "non_validate_only_mode", "write_or_submit_requested", "missing_or_stale_resource_facts",
    "missing_or_stale_field_source_refs", "missing_evidence_or_post_check_refs",
    "missing_runtime_result_refs", "submitted_not_false", "challenge_or_risk_control",
    "disabled_or_deferred_operation",
}
REQUIRED_RUNTIME_REFS = [
    "merged_head_ref", "identity_ref", "session_ref", "run_ref", "result_ref",
    "evidence_refs", "post_check_ref",
]
REQUIRED_FRESH_REFS = [
    "merged_head_ref", "page_ref", "identity_ref", "session_ref", "run_ref",
    "result_ref", "resource_refs", "field_source_refs", "evidence_refs",
    "post_check_ref", "submitted_result_ref",
]
EXPECTED_LOCK_ROLES = {
    "input_schema", "normalized_output_schema", "resource_requirements",
    "version_lifecycle_metadata", "write_deferred_guardrail", "fixture",
    "core_consumption_fixture", "post_check", "failure_mapping",
    "catalog_metadata", "repair_draft", "overlay_fork_metadata",
}
EXPECTED_ENTRY_KEYS = {
    "package_ref", "lock_ref", "lock_version", "version", "site_slug",
    "capability_id", "operation_id", "operation_mode", "lifecycle",
    "allowed_origins", "page_requirement", "resource_requirements", "freshness",
    "field_sources", "failure_taxonomy", "evidence_and_post_check",
    "runtime_result_requirements", "safety_boundary", "locked_asset_sha256",
    "runtime_admission",
}
EXPECTED_OPERATION_DETAILS = {
    "xhs_publish_note_precheck": {
        "target_kind": "creator_publish_page",
        "page_fact": "snapshot.creator_publish_page.available",
        "visible_fields": ["title_input", "content_editor", "publish_control"],
        "source_kinds": ["creator_publish_page_summary", "dom_snapshot_summary"],
        "blocked_actions": ["publish", "save", "upload", "submit", "schedule"],
    },
    "boss_greet_precheck": {
        "target_kind": "job_or_recruiter_communication_target",
        "page_fact": "snapshot.job_or_recruiter_target.available",
        "visible_fields": ["job_target", "recruiter_target", "greet_editor", "send_control"],
        "source_kinds": ["job_recruiter_target_summary", "dom_snapshot_summary"],
        "blocked_actions": ["greet", "chat", "send", "apply", "submit"],
    },
}
def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def error(errors: list[str], path: str, message: str) -> None:
    errors.append(f"{path}: {message}")


def exact_keys(errors: list[str], value: Any, expected: set[str], path: str) -> bool:
    if not isinstance(value, dict) or set(value) != expected:
        actual = set(value) if isinstance(value, dict) else set()
        error(errors, path, f"keys must be exact; missing={sorted(expected - actual)}, extra={sorted(actual - expected)}")
        return False
    return True


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_nested_lock_refs(errors: list[str], value: Any, prefix: str, expected: str, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            validate_nested_lock_refs(errors, child, prefix, expected, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            validate_nested_lock_refs(errors, child, prefix, expected, f"{path}[{index}]")
    elif isinstance(value, str) and value.startswith(prefix) and value != expected:
        error(errors, path, f"nested consumer or rollback lock ref must equal {expected}")


def validate_json_schema(errors: list[str], data: Any) -> None:
    if Draft202012Validator is None:
        error(errors, "schema", "jsonschema dependency is unavailable; install requirements-validator.txt")
        return
    schema = load_json(SCHEMA_PATH)
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        error(errors, "schema", f"invalid JSON Schema: {exc.message}")
        return
    validator = Draft202012Validator(schema)
    for finding in sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path)):
        pointer = ".".join(str(part) for part in finding.absolute_path) or "$"
        error(errors, f"schema.{pointer}", finding.message)


def schema_rejects(data: Any) -> bool:
    errors: list[str] = []
    validate_json_schema(errors, data)
    return bool(errors)


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
    if not exact_keys(errors, entry, EXPECTED_ENTRY_KEYS, path):
        return
    for key in ("package_ref", "lock_ref", "version", "site_slug", "capability_id", "operation_id", "operation_mode", "lifecycle"):
        if entry.get(key) != registry_entry.get(key):
            error(errors, f"{path}.{key}", "does not match local registry")
    if operation_id not in EXPECTED_OPERATIONS or entry.get("operation_mode") != "validate_only" or entry.get("lifecycle") != "proposed":
        error(errors, path, "must be an expected proposed validate-only operation")
    if entry.get("runtime_admission") != EXPECTED_ADMISSION[operation_id]:
        error(errors, f"{path}.runtime_admission", "does not match the site production admission policy")
    if registry_entry.get("runtime_admission") != EXPECTED_ADMISSION[operation_id]:
        error(errors, f"{path}.registry.runtime_admission", "does not match the site production admission policy")

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
    if entry.get("lock_version") != lock.get("lock_version") or lock.get("lock_version") != "0.1.1":
        error(errors, f"{path}.lock_version", "must bind the current relock version")
    manifest_lock = asset_ref(manifest, "package_lock") or {}
    if manifest_lock.get("lock_ref") != lock.get("lock_ref") or manifest_lock.get("lock_version") != lock.get("lock_version"):
        error(errors, f"{path}.lock_ref", "manifest package-lock identity drifted")
    lock_prefix = f"lode://lock/site-capability/{entry['site_slug']}/{entry['capability_id']}@"
    expected_lock_ref = str(lock.get("lock_ref"))
    validate_nested_lock_refs(errors, registry_entry, lock_prefix, expected_lock_ref, f"{path}.registry")
    validate_nested_lock_refs(errors, manifest, lock_prefix, expected_lock_ref, f"{path}.manifest")
    locked_assets = lock.get("locked_assets")
    if not isinstance(locked_assets, list) or {item.get("role") for item in locked_assets if isinstance(item, dict)} != EXPECTED_LOCK_ROLES:
        error(errors, f"{path}.locked_asset_sha256", "package lock must contain the exact critical asset roles")
    else:
        lock_hashes = {}
        for asset in locked_assets:
            exact_keys(errors, asset, {"role", "path", "ref", "version", "sha256"}, f"{path}.package_lock.locked_assets[{asset.get('role')}]")
            asset_path = root / str(asset.get("path"))
            actual_hash = sha256(asset_path) if asset_path.is_file() else None
            if asset.get("sha256") != actual_hash:
                error(errors, f"{path}.locked_asset_sha256.{asset.get('role')}", "content digest drifted from package lock")
            lock_hashes[asset["role"]] = asset.get("sha256")
            if asset_path.suffix == ".json" and asset_path.is_file():
                validate_nested_lock_refs(errors, load_json(asset_path), lock_prefix, expected_lock_ref, f"{path}.{asset['role']}")
        if entry.get("locked_asset_sha256") != lock_hashes:
            error(errors, f"{path}.locked_asset_sha256", "truth must exactly bind every package-lock digest")

    origins = entry.get("allowed_origins")
    if origins != manifest.get("site", {}).get("supported_origins") or not origins or any(not https_origin(origin) for origin in origins):
        error(errors, f"{path}.allowed_origins", "must exactly bind canonical HTTPS manifest origins")

    page = entry.get("page_requirement", {})
    exact_keys(errors, page, {"target_kind", "required_page_fact", "required_visible_fields", "challenge_fact", "page_change_policy"}, f"{path}.page_requirement")
    resources = bind_asset(errors, entry, root, manifest, "resource_requirements", "resource_requirements", "resource_requirements_id", "resource_requirements_version")
    exact_keys(errors, entry.get("resource_requirements"), {"path", "resource_requirements_id", "resource_requirements_version", "required_harbor_fact_keys"}, f"{path}.resource_requirements")
    if resources:
        profile = resources.get("resource_requirement_profiles", [None])[0] or {}
        facts = [item.get("fact_key") for item in profile.get("required_harbor_facts", [])]
        if entry["resource_requirements"].get("required_harbor_fact_keys") != facts:
            error(errors, f"{path}.resource_requirements", "must bind every required Harbor fact")
        details = EXPECTED_OPERATION_DETAILS[operation_id]
        if page.get("target_kind") != details["target_kind"] or page.get("required_page_fact") != details["page_fact"] or page.get("required_page_fact") not in facts or page.get("challenge_fact") != "safety.challenge.absent" or page.get("page_change_policy") != "reject" or page.get("required_visible_fields") != details["visible_fields"]:
            error(errors, f"{path}.page_requirement", "must bind the package page fact, visible fields, and reject page drift")

    freshness = entry.get("freshness", {})
    exact_keys(errors, freshness, {"policy", "applies_to", "stale_policy"}, f"{path}.freshness")
    if freshness.get("policy") != "current_execution_window" or freshness.get("stale_policy") != "reject" or freshness.get("applies_to") != REQUIRED_FRESH_REFS:
        error(errors, f"{path}.freshness", "must reject every stale ownership, runtime, evidence, post-check, and submitted-result ref")

    fields = entry.get("field_sources", {})
    exact_keys(errors, fields, {"source_ref_policy", "required_fields", "missing_or_unreferenced_field_policy"}, f"{path}.field_sources")
    details = EXPECTED_OPERATION_DETAILS[operation_id]
    expected_sources = {field: details["source_kinds"] for field in details["visible_fields"]}
    if fields.get("source_ref_policy") != "summary_refs_only" or fields.get("required_fields") != expected_sources or fields.get("missing_or_unreferenced_field_policy") != "reject":
        error(errors, f"{path}.field_sources", "must bind every visible field to summary refs and reject missing refs")

    mapping = bind_asset(errors, entry, root, manifest, "failure_taxonomy", "failure_mapping", "failure_mapping_id", "failure_mapping_version")
    exact_keys(errors, entry.get("failure_taxonomy"), {"path", "failure_mapping_id", "failure_mapping_version", "required_classes"}, f"{path}.failure_taxonomy")
    if mapping:
        classes = [item.get("lode_failure_class") for item in mapping.get("classes", [])]
        if entry["failure_taxonomy"].get("required_classes") != classes:
            error(errors, f"{path}.failure_taxonomy", "must bind the complete package taxonomy")

    post_check = bind_asset(errors, entry, root, manifest, "evidence_and_post_check", "post_check", "post_check_id", "post_check_version")
    evidence = entry.get("evidence_and_post_check", {})
    exact_keys(errors, evidence, {"evidence_ref_policy", "required_ref_kinds", "post_check_path", "post_check_id", "post_check_version", "required_post_check_fields"}, f"{path}.evidence_and_post_check")
    registry_evidence = registry_entry.get("evidence_requirements", {})
    if evidence.get("evidence_ref_policy") != "refs_only_no_inline_bodies" or evidence.get("required_ref_kinds") != registry_evidence.get("required_ref_kinds"):
        error(errors, f"{path}.evidence_and_post_check", "must bind exact refs-only registry evidence kinds")
    if post_check and evidence.get("required_post_check_fields") != post_check.get("result_contract", {}).get("required_fields"):
        error(errors, f"{path}.evidence_and_post_check", "must bind the complete post-check result contract")

    runtime = entry.get("runtime_result_requirements", {})
    safety = entry.get("safety_boundary", {})
    exact_keys(errors, runtime, {"required_refs", "result_field", "required_result_value"}, f"{path}.runtime_result_requirements")
    exact_keys(errors, safety, {"no_submit_guard", "submitted", "submitted_must_remain_false", "blocked_external_actions"}, f"{path}.safety_boundary")
    if runtime.get("required_refs") != REQUIRED_RUNTIME_REFS or runtime.get("result_field") != "submitted" or runtime.get("required_result_value") is not False:
        error(errors, f"{path}.runtime_result_requirements", "must require current merged-head/runtime/evidence refs and submitted=false")
    if safety.get("no_submit_guard") != "active" or safety.get("submitted") is not False or safety.get("submitted_must_remain_false") is not True or safety.get("blocked_external_actions") != details["blocked_actions"]:
        error(errors, f"{path}.safety_boundary", "must preserve active no-submit and submitted=false")
    registry_boundary = registry_entry.get("write_precheck_boundary", {})
    if registry_boundary.get("submitted") is not False or registry_boundary.get("true_write_execution") != "blocked":
        error(errors, f"{path}.safety_boundary", "local registry does not preserve the write-precheck block")


def validate(data: Any) -> list[str]:
    errors: list[str] = []
    validate_json_schema(errors, data)
    if not isinstance(data, dict):
        return ["truth: must be an object"]
    exact_keys(errors, data, {"$schema", "schema_version", "truth_id", "truth_version", "asset_owner", "consumer_boundary", "entries", "fail_closed", "non_goals"}, "truth")
    if data.get("$schema") != "./validate-only-runtime-consumption.schema.json" or data.get("schema_version") != "lode.validate-only-runtime-consumption.v0" or data.get("truth_id") != "lode.xhs-boss.write-precheck.runtime-consumption" or data.get("truth_version") != "0.1.0" or data.get("asset_owner") != "Lode":
        error(errors, "truth", "schema or owner is unsupported")
    boundary = data.get("consumer_boundary", {})
    exact_keys(errors, boundary, {"allowed_consumers", "admission_meaning", "runtime_execution", "live_success"}, "consumer_boundary")
    for index, consumer in enumerate(boundary.get("allowed_consumers", [])):
        exact_keys(errors, consumer, {"repository", "purpose"}, f"consumer_boundary.allowed_consumers[{index}]")
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


def mutation_cases() -> dict[str, Callable[[dict[str, Any]], None]]:
    mutations: dict[str, Callable[[dict[str, Any]], None]] = {
        "unknown_operation": lambda value: value["entries"][0].__setitem__("operation_id", "unknown"),
        "lock_drift": lambda value: value["entries"][0].__setitem__("lock_ref", "lode://lock/drift"),
        "asset_digest_drift": lambda value: value["entries"][0]["locked_asset_sha256"].__setitem__("post_check", "0" * 64),
        "version_drift": lambda value: value["entries"][0].__setitem__("version", "0.2.0"),
        "origin_drift": lambda value: value["entries"][0].__setitem__("allowed_origins", ["http://example.com"]),
        "page_drift": lambda value: value["entries"][0]["page_requirement"].__setitem__("required_page_fact", "page.changed"),
        "challenge_present": lambda value: value["entries"][0]["page_requirement"].__setitem__("challenge_fact", "safety.challenge.present"),
        "write_mode": lambda value: value["entries"][0].__setitem__("operation_mode", "write"),
        "stale_facts": lambda value: value["entries"][0]["freshness"].__setitem__("policy", "stale_allowed"),
        "missing_field_source_ref": lambda value: value["entries"][0]["field_sources"]["required_fields"].__setitem__("title_input", []),
        "missing_evidence_ref": lambda value: value["entries"][0]["evidence_and_post_check"].__setitem__("required_ref_kinds", []),
        "missing_post_check_ref": lambda value: value["entries"][0]["evidence_and_post_check"].__setitem__("post_check_path", ""),
        "missing_runtime_result_ref": lambda value: value["entries"][0]["runtime_result_requirements"]["required_refs"].pop(),
        "submitted_true": lambda value: value["entries"][0]["safety_boundary"].__setitem__("submitted", True),
        "submit_requested": lambda value: value["entries"][0]["safety_boundary"].__setitem__("no_submit_guard", "inactive"),
        "missing_blocked_action": lambda value: value["entries"][0]["safety_boundary"]["blocked_external_actions"].pop(),
        "unknown_source_kind": lambda value: value["entries"][0]["field_sources"]["required_fields"]["title_input"].append("unknown_summary"),
        "unknown_nested_key": lambda value: value["entries"][0]["freshness"].__setitem__("unknown", True),
        "XHS_disabled": lambda value: value["entries"][0]["runtime_admission"].__setitem__("enabled", False),
        "XHS_inverted_to_BOSS": lambda value: value["entries"][0].__setitem__("runtime_admission", copy.deepcopy(EXPECTED_ADMISSION["boss_greet_precheck"])),
        "BOSS_enabled": lambda value: value["entries"][1]["runtime_admission"].__setitem__("enabled", True),
        "BOSS_inverted_to_XHS": lambda value: value["entries"][1].__setitem__("runtime_admission", copy.deepcopy(EXPECTED_ADMISSION["xhs_publish_note_precheck"])),
        "BOSS_current": lambda value: value["entries"][1]["runtime_admission"].__setitem__("status", "current"),
    }
    for ref in REQUIRED_FRESH_REFS:
        mutations[f"missing_freshness_{ref}"] = lambda value, ref=ref: value["entries"][0]["freshness"]["applies_to"].remove(ref)
        mutations[f"drift_freshness_{ref}"] = lambda value, ref=ref: value["entries"][0]["freshness"]["applies_to"].__setitem__(value["entries"][0]["freshness"]["applies_to"].index(ref), f"{ref}.drift")
    return mutations


def self_test(data: dict[str, Any], declared_cases: list[str]) -> list[str]:
    mutations = mutation_cases()
    failures: list[str] = []
    if declared_cases != list(mutations):
        failures.append(f"fixture rejection_cases do not exactly map executable mutations: declared={declared_cases}, actual={list(mutations)}")
        return failures
    for name, mutate in mutations.items():
        candidate = copy.deepcopy(data)
        mutate(candidate)
        if name in {"XHS_disabled", "XHS_inverted_to_BOSS", "BOSS_enabled", "BOSS_inverted_to_XHS", "BOSS_current"} and not schema_rejects(candidate):
            failures.append(f"published schema did not reject {name}")
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
    fixture_keys = {"schema_version", "truth_ref", "accepted_operations", "expected_mode", "expected_submitted", "required_runtime_refs", "rejection_cases"}
    if not exact_keys(errors, fixture, fixture_keys, "fixture") or fixture.get("schema_version") != "lode.validate-only-runtime-consumption-fixture.v0" or fixture.get("truth_ref") != "registry/validate-only-runtime-consumption.json" or fixture.get("accepted_operations") != ["xhs_publish_note_precheck"] or fixture.get("expected_mode") != "validate_only" or fixture.get("expected_submitted") is not False or fixture.get("required_runtime_refs") != REQUIRED_RUNTIME_REFS or fixture.get("rejection_cases") != list(mutation_cases()):
        errors.append("fixture: acceptance identity drifted")
    if args.self_test and not errors:
        errors.extend(self_test(data, fixture["rejection_cases"]))
    if errors:
        for item in errors:
            print(item)
        return 1
    print("validate-only runtime-consumption truth: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
