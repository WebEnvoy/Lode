#!/usr/bin/env python3
"""Validate the two lock-bound Lode read-operation admission entries offline."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST_PATH = Path("registry/runtime-consumption-allowlist.json")
REGISTRY_PATH = Path("registry/local-packages.json")
EXPECTED_OPERATIONS = {"xhs_search_notes", "boss_job_search"}
EXPECTED_CONSUMERS = [
    {
        "repository": "WebEnvoy/Harbor",
        "issue": "#245",
        "purpose": "allowlisted one-shot read-only operation admission",
    },
    {
        "repository": "WebEnvoy/WebEnvoy",
        "issue": "#267",
        "purpose": "lock-bound read-only task admission and run recording",
    },
]
EXPECTED_FAIL_CLOSED_CONDITIONS = {
    "unknown_operation",
    "package_lock_or_version_drift",
    "non_https_origin",
    "non_read_operation_mode",
    "missing_resource_requirements",
    "missing_failure_taxonomy",
    "missing_refs_only_evidence_or_post_check",
}
REQUIRED_ENTRY_KEYS = {
    "package_ref",
    "lock_ref",
    "version",
    "site_slug",
    "capability_id",
    "operation_id",
    "operation_mode",
    "lifecycle",
    "allowed_origins",
    "resource_requirements",
    "failure_taxonomy",
    "evidence_and_post_check",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def add_error(errors: list[str], path: str, message: str) -> None:
    errors.append(f"{path}: {message}")


def require_keys(errors: list[str], value: Any, keys: set[str], path: str) -> bool:
    if not isinstance(value, dict):
        add_error(errors, path, "must be an object")
        return False
    missing = sorted(keys - set(value))
    if missing:
        add_error(errors, path, f"missing keys: {', '.join(missing)}")
        return False
    return True


def is_https_origin(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc) and parsed.path in {"", "/"} and not parsed.params and not parsed.query and not parsed.fragment


def asset_ref(manifest: dict[str, Any], role: str) -> dict[str, Any] | None:
    refs = manifest.get("asset_refs")
    if not isinstance(refs, list):
        return None
    return next((item for item in refs if isinstance(item, dict) and item.get("role") == role), None)


def package_root(entry: dict[str, Any]) -> Path:
    return ROOT / str(entry["package_path"])


def validate_entry(errors: list[str], entry: Any, registry_entries: dict[str, dict[str, Any]]) -> None:
    if not require_keys(errors, entry, REQUIRED_ENTRY_KEYS, "entries[]"):
        return
    operation_id = entry["operation_id"]
    path = f"entries[{operation_id}]"
    registry_entry = registry_entries.get(operation_id)
    if registry_entry is None:
        add_error(errors, path, "unknown operation is not in the local registry")
        return
    for key in ["package_ref", "lock_ref", "version", "site_slug", "capability_id", "operation_id", "operation_mode", "lifecycle"]:
        if entry.get(key) != registry_entry.get(key):
            add_error(errors, f"{path}.{key}", "does not match local registry")
    if entry.get("operation_id") not in EXPECTED_OPERATIONS:
        add_error(errors, f"{path}.operation_id", "is not allowlisted")
    if entry.get("operation_mode") != "read":
        add_error(errors, f"{path}.operation_mode", "must be read")
    if entry.get("lifecycle") != "proposed":
        add_error(errors, f"{path}.lifecycle", "must remain proposed")

    root = package_root(registry_entry)
    manifest = load_json(root / "manifest.json")
    lock = load_json(root / "package-lock.json")
    capability = manifest.get("capability", {})
    for key in ["package_ref", "version"]:
        manifest_value = manifest.get(key) if key == "package_ref" else capability.get(key)
        if entry.get(key) != manifest_value:
            add_error(errors, f"{path}.{key}", "does not match manifest")
    for key, lock_key in [("lock_ref", "lock_ref"), ("version", "package_version"), ("operation_id", "operation_id"), ("operation_mode", "operation_mode"), ("lifecycle", "lifecycle")]:
        if entry.get(key) != lock.get(lock_key):
            add_error(errors, f"{path}.{key}", "does not match package lock")

    origins = entry.get("allowed_origins")
    manifest_origins = manifest.get("site", {}).get("supported_origins")
    if not isinstance(origins, list) or not origins or any(not is_https_origin(origin) for origin in origins):
        add_error(errors, f"{path}.allowed_origins", "must contain only canonical HTTPS origins")
    if origins != manifest_origins:
        add_error(errors, f"{path}.allowed_origins", "must exactly match manifest supported_origins")

    validate_resources(errors, path, entry, manifest, root)
    validate_failure_taxonomy(errors, path, entry, manifest, root)
    validate_evidence_and_post_check(errors, path, entry, manifest, root, registry_entry)


def validate_resources(errors: list[str], path: str, entry: dict[str, Any], manifest: dict[str, Any], root: Path) -> None:
    value = entry.get("resource_requirements")
    required = {"path", "resource_requirements_id", "resource_requirements_version", "required_harbor_fact_keys"}
    if not require_keys(errors, value, required, f"{path}.resource_requirements"):
        return
    ref = asset_ref(manifest, "resource_requirements")
    if ref is None or ref.get("status") != "present":
        add_error(errors, f"{path}.resource_requirements", "manifest resource requirements asset is missing")
        return
    if value["path"] != str(root.relative_to(ROOT) / ref["path"]):
        add_error(errors, f"{path}.resource_requirements.path", "does not match manifest asset path")
    for key in ["resource_requirements_id", "resource_requirements_version"]:
        if value.get(key) != ref.get(key):
            add_error(errors, f"{path}.resource_requirements.{key}", "does not match manifest asset")
    requirements = load_json(root / ref["path"])
    facts = [fact.get("fact_key") for profile in requirements.get("resource_requirement_profiles", []) for fact in profile.get("required_harbor_facts", []) if isinstance(fact, dict)]
    if value.get("required_harbor_fact_keys") != facts or not facts:
        add_error(errors, f"{path}.resource_requirements.required_harbor_fact_keys", "must exactly bind all required Harbor facts")


def validate_failure_taxonomy(errors: list[str], path: str, entry: dict[str, Any], manifest: dict[str, Any], root: Path) -> None:
    value = entry.get("failure_taxonomy")
    required = {"path", "failure_mapping_id", "failure_mapping_version", "required_classes"}
    if not require_keys(errors, value, required, f"{path}.failure_taxonomy"):
        return
    ref = asset_ref(manifest, "failure_mapping")
    if ref is None or ref.get("status") != "present":
        add_error(errors, f"{path}.failure_taxonomy", "manifest failure mapping asset is missing")
        return
    if value["path"] != str(root.relative_to(ROOT) / ref["path"]):
        add_error(errors, f"{path}.failure_taxonomy.path", "does not match manifest asset path")
    for key in ["failure_mapping_id", "failure_mapping_version"]:
        if value.get(key) != ref.get(key):
            add_error(errors, f"{path}.failure_taxonomy.{key}", "does not match manifest asset")
    mapping = load_json(root / ref["path"])
    classes = [item.get("lode_failure_class") for item in mapping.get("classes", []) if isinstance(item, dict)]
    if value.get("required_classes") != classes or not classes:
        add_error(errors, f"{path}.failure_taxonomy.required_classes", "must exactly bind the failure taxonomy")


def validate_evidence_and_post_check(errors: list[str], path: str, entry: dict[str, Any], manifest: dict[str, Any], root: Path, registry_entry: dict[str, Any]) -> None:
    value = entry.get("evidence_and_post_check")
    required = {"source_ref_policy", "evidence_ref_policy", "required_ref_kinds", "post_check_path", "post_check_id", "post_check_version", "required_post_check_fields"}
    if not require_keys(errors, value, required, f"{path}.evidence_and_post_check"):
        return
    registry_evidence = registry_entry.get("evidence_requirements")
    if not isinstance(registry_evidence, dict) or registry_evidence.get("source_ref_policy") != value.get("source_ref_policy") or registry_evidence.get("evidence_ref_policy") != "refs_only_no_inline_bodies" or registry_evidence.get("required_ref_kinds") != value.get("required_ref_kinds"):
        add_error(errors, f"{path}.evidence_and_post_check", "must exactly bind the registry refs-only evidence requirement")
    ref = asset_ref(manifest, "post_check")
    if ref is None or ref.get("status") != "present":
        add_error(errors, f"{path}.evidence_and_post_check", "manifest post-check asset is missing")
        return
    if value.get("post_check_path") != str(root.relative_to(ROOT) / ref["path"]):
        add_error(errors, f"{path}.evidence_and_post_check.post_check_path", "does not match manifest asset path")
    for key in ["post_check_id", "post_check_version"]:
        if value.get(key) != ref.get(key):
            add_error(errors, f"{path}.evidence_and_post_check.{key}", "does not match manifest asset")
    post_check = load_json(root / ref["path"])
    required_fields = post_check.get("result_contract", {}).get("required_fields")
    if value.get("required_post_check_fields") != required_fields or not required_fields:
        add_error(errors, f"{path}.evidence_and_post_check.required_post_check_fields", "must exactly bind the post-check result contract")


def validate(data: Any) -> list[str]:
    errors: list[str] = []
    if not require_keys(errors, data, {"schema_version", "allowlist_id", "allowlist_version", "asset_owner", "consumer_boundary", "entries", "fail_closed", "non_goals"}, "allowlist"):
        return errors
    if data.get("schema_version") != "lode.runtime-consumption-allowlist.v0":
        add_error(errors, "allowlist.schema_version", "is unsupported")
    if data.get("asset_owner") != "Lode":
        add_error(errors, "allowlist.asset_owner", "must be Lode")
    boundary = data.get("consumer_boundary")
    if not isinstance(boundary, dict) or boundary.get("runtime_execution") != "out_of_scope" or "does not prove" not in str(boundary.get("admission_meaning", "")):
        add_error(errors, "allowlist.consumer_boundary", "must preserve the admission-only, non-runner boundary")
    elif boundary.get("allowed_consumers") != EXPECTED_CONSUMERS:
        add_error(errors, "allowlist.consumer_boundary.allowed_consumers", "must exactly and exclusively bind Harbor #245 and Core #267 with their declared purposes")
    fail_closed = data.get("fail_closed")
    if not isinstance(fail_closed, dict) or set(fail_closed) != EXPECTED_FAIL_CLOSED_CONDITIONS or any(
        fail_closed.get(condition) != "reject" for condition in EXPECTED_FAIL_CLOSED_CONDITIONS
    ):
        add_error(errors, "allowlist.fail_closed", "must contain exactly the expected failure conditions and reject every one")
    entries = data.get("entries")
    if not isinstance(entries, list) or len(entries) != len(EXPECTED_OPERATIONS):
        add_error(errors, "allowlist.entries", "must contain exactly the two allowlisted operations")
        return errors
    operation_ids = [entry.get("operation_id") for entry in entries if isinstance(entry, dict)]
    if set(operation_ids) != EXPECTED_OPERATIONS or len(operation_ids) != len(set(operation_ids)):
        add_error(errors, "allowlist.entries", "must contain each known operation exactly once")
        return errors
    registry = load_json(ROOT / REGISTRY_PATH)
    registry_entries = {entry.get("operation_id"): entry for entry in registry.get("entries", []) if isinstance(entry, dict) and entry.get("operation_id") in EXPECTED_OPERATIONS}
    for entry in entries:
        validate_entry(errors, entry, registry_entries)
    return errors


def self_test(data: dict[str, Any]) -> list[str]:
    cases = [
        ("unknown operation", lambda value: value["entries"][0].__setitem__("operation_id", "unknown")),
        ("lock drift", lambda value: value["entries"][0].__setitem__("lock_ref", "lode://lock/drift")),
        ("non HTTPS origin", lambda value: value["entries"][0].__setitem__("allowed_origins", ["http://www.xiaohongshu.com"])),
        ("write mode", lambda value: value["entries"][0].__setitem__("operation_mode", "write")),
        ("missing evidence", lambda value: value["entries"][0].__setitem__("evidence_and_post_check", {})),
        ("arbitrary consumer", lambda value: value["consumer_boundary"]["allowed_consumers"].append({"repository": "WebEnvoy/App", "issue": "#999", "purpose": "unauthorized"})),
        ("missing reject map", lambda value: value.pop("fail_closed")),
        ("empty reject map", lambda value: value.__setitem__("fail_closed", {})),
        ("non-reject failure condition", lambda value: value["fail_closed"].__setitem__("unknown_operation", "allow")),
        ("active lifecycle", lambda value: value["entries"][0].__setitem__("lifecycle", "active")),
    ]
    failures: list[str] = []
    for name, mutate in cases:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        if not validate(candidate):
            failures.append(f"self-test did not reject {name}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="Run in-memory fail-closed mutation checks.")
    args = parser.parse_args()
    data = load_json(ROOT / ALLOWLIST_PATH)
    errors = validate(data)
    if args.self_test and not errors:
        errors.extend(self_test(data))
    report = {
        "schema_version": "lode-runtime-consumption-allowlist-validation.v0",
        "status": "failed" if errors else "passed",
        "allowlist": str(ALLOWLIST_PATH),
        "operations": sorted(EXPECTED_OPERATIONS),
        "errors": errors,
    }
    print(json.dumps(report, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
