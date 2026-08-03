#!/usr/bin/env python3
"""Validate the Core-consumable Xiaohongshu search version/hash pin."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
TRUTH_PATH = ROOT / "registry/search-runtime-consumption.json"
SCHEMA_PATH = ROOT / "registry/search-runtime-consumption.schema.json"
REGISTRY_PATH = ROOT / "registry/local-packages.json"
ALLOWLIST_PATH = ROOT / "registry/runtime-consumption-allowlist.json"
OPERATION = "xhs_search_notes"
PACKAGE_ROOT = ROOT / "sites/xiaohongshu/search-notes"
EXPECTED_ADMISSION = {"enabled": True, "status": "current", "recheck_condition": "not_applicable"}
EXPECTED_ASSET_PATHS = {
    "manifest": "sites/xiaohongshu/search-notes/manifest.json",
    "package_lock": "sites/xiaohongshu/search-notes/package-lock.json",
    "input_schema": "sites/xiaohongshu/search-notes/schemas/input.schema.json",
    "output_schema": "sites/xiaohongshu/search-notes/schemas/output.schema.json",
    "resource_requirements": "sites/xiaohongshu/search-notes/resource-requirements.json",
    "failure_mapping": "sites/xiaohongshu/search-notes/failure-mapping.json",
    "post_check": "sites/xiaohongshu/search-notes/checks/post-check.json",
    "runtime_consumption_allowlist": "registry/runtime-consumption-allowlist.json",
}
EXPECTED_FIELDS = ["canonical_url", "title", "summary", "source_status", "keyword", "result_count", "notes"]
EXPECTED_REFS = ["pinia_store_summary", "network_summary", "dom_snapshot_summary", "snapshot_ref", "post_check_ref"]
FORBIDDEN_KEYS = {"cookie", "cookies", "token", "tokens", "profile", "profile_state", "runtime_session", "raw_dom", "raw_evidence_body", "network_response_body", "production_payload", "user_business_data"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def schema_errors(data: Any) -> list[str]:
    try:
        import jsonschema
        validator = jsonschema.Draft202012Validator(load_json(SCHEMA_PATH), format_checker=jsonschema.FormatChecker())
        return [error.message for error in validator.iter_errors(data)]
    except ImportError:
        return ["jsonschema dependency is unavailable"]
    except (OSError, json.JSONDecodeError) as exc:
        return [f"schema unavailable: {exc}"]


def add(errors: list[str], path: str, message: str) -> None:
    errors.append(f"{path}: {message}")


def forbidden_keys(value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_KEYS:
                errors.append(f"{path}.{key}: forbidden sensitive/runtime material")
            errors.extend(forbidden_keys(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(forbidden_keys(child, f"{path}[{index}]"))
    return errors


def registry_entries(registry: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    registry = registry if registry is not None else load_json(REGISTRY_PATH)
    if not isinstance(registry, dict):
        return []
    return [entry for entry in registry.get("entries", []) if isinstance(entry, dict) and entry.get("operation_id") == OPERATION]


def validate_assets(errors: list[str], entry: dict[str, Any]) -> None:
    assets = entry.get("assets", {})
    if not isinstance(assets, dict):
        add(errors, "entries[0].assets", "must be an object")
        return
    if set(assets) != set(EXPECTED_ASSET_PATHS):
        add(errors, "entries[0].assets", "must pin exactly the Core asset roles")
        return
    for role, expected_path in EXPECTED_ASSET_PATHS.items():
        value = assets.get(role)
        if not isinstance(value, list) or len(value) != 2:
            add(errors, f"entries[0].assets.{role}", "must be [repo-relative path, SHA-256]")
            continue
        path, expected_hash = value
        if path != expected_path:
            add(errors, f"entries[0].assets.{role}[0]", "path is not the expected hard-pinned asset")
            continue
        candidate = ROOT / path
        try:
            candidate.resolve().relative_to(ROOT.resolve())
        except ValueError:
            add(errors, f"entries[0].assets.{role}[0]", "asset path escapes repository root")
            continue
        if not candidate.is_file():
            add(errors, f"entries[0].assets.{role}", "asset file is missing")
            continue
        if sha256(candidate) != expected_hash:
            add(errors, f"entries[0].assets.{role}[1]", "content SHA-256 drifted")


def validate_package_identity(errors: list[str], entry: dict[str, Any], registry: dict[str, Any] | None = None) -> None:
    try:
        matches = registry_entries(registry)
    except (OSError, json.JSONDecodeError) as exc:
        add(errors, "registry", f"local registry unavailable: {exc}")
        return
    if len(matches) != 1:
        add(errors, "registry", f"xhs_search_notes must have exactly one local registry entry (found {len(matches)})")
        return
    current = matches[0]
    for key in ("package_ref", "lock_ref", "version", "site_slug", "capability_id", "operation_id", "operation_mode", "lifecycle"):
        if entry.get(key) != current.get(key):
            add(errors, f"entries[0].{key}", "does not match local registry")
    if current.get("runtime_admission") != EXPECTED_ADMISSION or entry.get("runtime_admission") != EXPECTED_ADMISSION:
        add(errors, "entries[0].runtime_admission", "does not match current search admission policy")
    ref = current.get("runtime_consumption_ref")
    if ref != "registry/search-runtime-consumption.json":
        add(errors, "registry.runtime_consumption_ref", "does not discover this declaration")


def validate_assets_content(errors: list[str], entry: dict[str, Any]) -> None:
    try:
        manifest = load_json(PACKAGE_ROOT / "manifest.json")
        lock = load_json(PACKAGE_ROOT / "package-lock.json")
    except (OSError, json.JSONDecodeError) as exc:
        add(errors, "package", f"manifest/lock unavailable: {exc}")
        return
    if not isinstance(manifest, dict) or not isinstance(lock, dict):
        add(errors, "package", "manifest and lock must be JSON objects")
        return
    expected = {
        "package_ref": manifest.get("package_ref"),
        "lock_ref": lock.get("lock_ref"),
        "version": manifest.get("capability", {}).get("version"),
        "operation_id": manifest.get("capability", {}).get("operation_id"),
        "operation_mode": manifest.get("capability", {}).get("operation_mode"),
        "lifecycle": manifest.get("capability", {}).get("lifecycle"),
    }
    for key, value in expected.items():
        if entry.get(key) != value:
            add(errors, f"entries[0].{key}", "does not match package manifest/lock")
    if lock.get("package_ref") != manifest.get("package_ref") or lock.get("package_version") != manifest.get("capability", {}).get("version"):
        add(errors, "package-lock.json", "package identity is inconsistent")
    refs_value = manifest.get("asset_refs", [])
    refs = {item.get("role"): item for item in refs_value if isinstance(item, dict)} if isinstance(refs_value, list) else {}
    if not isinstance(refs_value, list):
        add(errors, "manifest.asset_refs", "must be an array")
    package_roles = {"input_schema": "schemas/input.schema.json", "normalized_output_schema": "schemas/output.schema.json", "resource_requirements": "resource-requirements.json", "failure_mapping": "failure-mapping.json", "post_check": "checks/post-check.json", "package_lock": "package-lock.json"}
    for role, path in package_roles.items():
        ref = refs.get(role)
        if not isinstance(ref, dict) or ref.get("status") != "present" or ref.get("path") != path:
            add(errors, f"manifest.asset_refs.{role}", "does not match the pinned package asset")
    try:
        input_schema = load_json(PACKAGE_ROOT / "schemas/input.schema.json")
        output_schema = load_json(PACKAGE_ROOT / "schemas/output.schema.json")
        resource = load_json(PACKAGE_ROOT / "resource-requirements.json")
        failures = load_json(PACKAGE_ROOT / "failure-mapping.json")
        post_check = load_json(PACKAGE_ROOT / "checks/post-check.json")
        allowlist = load_json(ALLOWLIST_PATH)
    except (OSError, json.JSONDecodeError) as exc:
        add(errors, "assets", f"pinned JSON unavailable: {exc}")
        return
    if not isinstance(input_schema, dict) or input_schema.get("required") != ["url", "keyword"]:
        add(errors, "input_schema.required", "must bind url and keyword")
    output_defs = output_schema.get("$defs", {}) if isinstance(output_schema, dict) else {}
    content_detail = output_defs.get("content_detail", {}) if isinstance(output_defs, dict) else {}
    if not isinstance(content_detail, dict) or content_detail.get("required") != EXPECTED_FIELDS:
        add(errors, "output_schema.content_detail.required", "public fields drifted")
    profiles = resource.get("resource_requirement_profiles", []) if isinstance(resource, dict) else []
    profile_facts: list[Any] = []
    if isinstance(profiles, list):
        for profile in profiles:
            if not isinstance(profile, dict) or not isinstance(profile.get("required_harbor_facts"), list):
                continue
            profile_facts.extend(fact.get("fact_key") for fact in profile["required_harbor_facts"] if isinstance(fact, dict))
    if not profile_facts:
        add(errors, "resource_requirements", "must declare Harbor fact requirements")
    classes = failures.get("classes", []) if isinstance(failures, dict) else []
    if [item.get("lode_failure_class") for item in classes if isinstance(item, dict)] != ["invalid_contract", "resource_unavailable", "site_changed", "empty_result", "not_logged_in", "login_expired", "page_not_ready", "signed_ref_missing", "safety_challenge", "field_missing", "network_resource_unavailable"]:
        add(errors, "failure_mapping.classes", "failure taxonomy drifted")
    result_contract = post_check.get("result_contract", {}) if isinstance(post_check, dict) else {}
    if not isinstance(result_contract, dict) or result_contract.get("required_fields") != ["status", "reason", "source_refs", "evidence_refs"]:
        add(errors, "post_check.result_contract.required_fields", "post-check fields drifted")
    allowlist_entries = allowlist.get("entries", []) if isinstance(allowlist, dict) else []
    allowlisted = [item for item in allowlist_entries if isinstance(item, dict) and item.get("operation_id") == OPERATION] if isinstance(allowlist_entries, list) else []
    if len(allowlisted) != 1:
        add(errors, "runtime-consumption-allowlist", "must contain exactly one xhs_search_notes entry")
    elif entry.get("required_ref_kinds") != allowlisted[0].get("evidence_and_post_check", {}).get("required_ref_kinds"):
        add(errors, "entries[0].required_ref_kinds", "does not match existing allowlist evidence requirements")
    for asset_path in EXPECTED_ASSET_PATHS:
        assets = entry.get("assets", {})
        path = assets.get(asset_path, [None])[0] if isinstance(assets, dict) else None
        if isinstance(path, str) and path.endswith(".json"):
            try:
                errors.extend(forbidden_keys(load_json(ROOT / path), path))
            except (OSError, json.JSONDecodeError):
                pass


def validate(data: dict[str, Any]) -> list[str]:
    errors = [f"schema: {message}" for message in schema_errors(data)]
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, list) or len(entries) != 1 or not isinstance(entries[0], dict):
        add(errors, "entries", "must contain exactly one search entry")
        return errors
    entry = entries[0]
    validate_package_identity(errors, entry)
    validate_assets(errors, entry)
    validate_assets_content(errors, entry)
    return errors


def self_test(data: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("asset_digest_drift", lambda candidate: candidate["entries"][0]["assets"]["manifest"].__setitem__(1, "0" * 64)),
        ("asset_path_drift", lambda candidate: candidate["entries"][0]["assets"]["manifest"].__setitem__(0, "sites/xiaohongshu/search-notes/fixtures/search-notes.fixture.json")),
        ("lock_drift", lambda candidate: candidate["entries"][0].__setitem__("lock_ref", "lode://lock/drift")),
        ("extra_fixture_pin", lambda candidate: candidate["entries"][0]["assets"].__setitem__("fixture", ["sites/xiaohongshu/search-notes/fixtures/search-notes.fixture.json", "0" * 64])),
        ("malformed_assets", lambda candidate: candidate["entries"][0].__setitem__("assets", [])),
    ]
    failures: list[str] = []
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        if not validate(candidate):
            failures.append(f"self-test did not reject {name}")
    try:
        registry = load_json(REGISTRY_PATH)
        matches = registry_entries(registry)
        if matches:
            registry["entries"].append(copy.deepcopy(matches[0]))
            duplicate_errors: list[str] = []
            validate_package_identity(duplicate_errors, data["entries"][0], registry)
            if not any("exactly one local registry entry" in error for error in duplicate_errors):
                failures.append("self-test did not reject duplicate local registry entry")
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"self-test registry fixture unavailable: {exc}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    data = load_json(TRUTH_PATH)
    errors = validate(data)
    if args.self_test and not errors:
        errors.extend(self_test(data))
    print(json.dumps({"status": "failed" if errors else "passed", "operation": OPERATION, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
