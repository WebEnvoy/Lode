#!/usr/bin/env python3
"""Offline validator for a single Lode site-capability package."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SUPPORTED_MANIFEST_VERSION = "lode.site-capability.manifest.v0"
SUPPORTED_LOCAL_REGISTRY_VERSION = "lode.local-package-index.v0"
SUPPORTED_PACKAGE_LOCK_VERSION = "lode.package-lock.v0"
SUPPORTED_PACKAGE_TYPE = "site-capability"
DEFAULT_LOCAL_REGISTRY = Path("registry/local-packages.json")
SUPPORTED_OPERATION_MODES = {"read", "validate_only", "draft", "preview", "write"}
POST_CHECK_STATUSES = {"passed", "failed", "skipped"}
REQUIRED_FAILURE_CLASSES = {"invalid_contract", "resource_unavailable", "site_changed", "empty_result"}
REQUIRED_ASSET_ROLES = {
    "input_schema",
    "normalized_output_schema",
    "resource_requirements",
    "version_lifecycle_metadata",
    "fixture",
    "write_deferred_guardrail",
    "failure_mapping",
    "package_lock",
}
FORBIDDEN_KEYS = {
    "cookie",
    "cookies",
    "token",
    "tokens",
    "profile_state",
    "runtime_session",
    "runtime_session_id",
    "live_tab_state",
    "provider_key",
    "harbor_profile_id",
    "local_path",
    "storage_url",
    "proxy",
    "raw_evidence_body",
    "full_dom",
    "har",
    "screenshot_body",
    "network_response_body",
    "production_payload",
    "user_business_data",
}


class Report:
    def __init__(self, package_root: Path) -> None:
        self.package_root = package_root
        self.package_ref: str | None = None
        self.errors: list[dict[str, Any]] = []
        self.warnings: list[dict[str, Any]] = []
        self.checked_refs: list[dict[str, Any]] = []

    def ref(self, role: str, path: Path | str, status: str) -> None:
        self.checked_refs.append({"role": role, "path": str(path), "status": status})

    def issue(
        self,
        severity: str,
        code: str,
        path: Path | str,
        message: str,
        recovery_hint: str,
    ) -> None:
        issue = {
            "severity": severity,
            "code": code,
            "path": str(path),
            "message": message,
            "recovery_hint": recovery_hint,
        }
        if severity == "error":
            self.errors.append(issue)
        else:
            self.warnings.append(issue)

    def to_dict(self) -> dict[str, Any]:
        if self.errors:
            status = "failed"
        elif self.warnings:
            status = "passed_with_warnings"
        else:
            status = "passed"
        return {
            "schema_version": "lode-validator-report.v0",
            "status": status,
            "package_root": str(self.package_root),
            "package_ref": self.package_ref,
            "errors": self.errors,
            "warnings": self.warnings,
            "checked_refs": self.checked_refs,
        }


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def load_json(report: Report, root: Path, path: Path, role: str, display_path: str | None = None) -> Any | None:
    display_path = display_path or rel(root, path)
    if not path.exists():
        report.ref(role, display_path, "missing")
        report.issue("error", "asset_missing", display_path, "Referenced file is missing.", "Create the referenced package asset or mark it planned.")
        return None
    report.ref(role, display_path, "present")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.issue("error", "invalid_contract", display_path, f"Invalid JSON: {exc}", "Fix JSON syntax before package validation.")
        return None


def add_error(report: Report, code: str, path: str, message: str, hint: str) -> None:
    report.issue("error", code, path, message, hint)


def add_warning(report: Report, code: str, path: str, message: str, hint: str) -> None:
    report.issue("warning", code, path, message, hint)


def require_keys(report: Report, obj: dict[str, Any], keys: list[str], path: str) -> None:
    for key in keys:
        if key not in obj:
            add_error(report, "invalid_contract", path, f"Missing required key `{key}`.", f"Add `{key}` to the package contract.")


def scan_forbidden_keys(report: Report, value: Any, path: str, pointer: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_pointer = f"{pointer}.{key}"
            if key in FORBIDDEN_KEYS:
                add_error(
                    report,
                    "forbidden_field",
                    path,
                    f"Forbidden field key `{key}` appears at `{child_pointer}`.",
                    "Keep runtime identity, credentials, raw evidence, and production data out of Lode packages.",
                )
            scan_forbidden_keys(report, child, path, child_pointer)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            scan_forbidden_keys(report, child, path, f"{pointer}[{index}]")


def asset_index(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    refs = manifest.get("asset_refs", [])
    if not isinstance(refs, list):
        return {}
    return {ref.get("role"): ref for ref in refs if isinstance(ref, dict) and ref.get("role")}


def discover_repo_root(path: Path) -> Path | None:
    for candidate in [path, *path.parents]:
        if (candidate / ".git").exists() or (candidate / DEFAULT_LOCAL_REGISTRY).exists():
            return candidate
    return None


def discover_local_registry(package_root: Path) -> Path | None:
    repo_root = discover_repo_root(package_root)
    if repo_root is None:
        return None
    candidate = repo_root / DEFAULT_LOCAL_REGISTRY
    return candidate if candidate.exists() else None


def validate_manifest(report: Report, root: Path, manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    report.package_ref = manifest.get("package_ref")
    require_keys(report, manifest, ["manifest_version", "package_ref", "package_type", "site", "capability", "asset_refs"], "manifest.json")
    if manifest.get("manifest_version") != SUPPORTED_MANIFEST_VERSION:
        add_error(report, "unsupported_version", "manifest.json", "Unsupported manifest version.", f"Use `{SUPPORTED_MANIFEST_VERSION}`.")
    if manifest.get("package_type") != SUPPORTED_PACKAGE_TYPE:
        add_error(report, "invalid_contract", "manifest.json", "Unsupported package type.", f"Use `{SUPPORTED_PACKAGE_TYPE}` for GH-96 validation.")

    site = manifest.get("site") if isinstance(manifest.get("site"), dict) else {}
    capability = manifest.get("capability") if isinstance(manifest.get("capability"), dict) else {}
    require_keys(report, site, ["slug", "supported_origins"], "manifest.json#site")
    require_keys(report, capability, ["capability_id", "operation_id", "operation_mode", "version", "lifecycle"], "manifest.json#capability")
    if capability.get("operation_mode") not in SUPPORTED_OPERATION_MODES:
        add_error(report, "invalid_contract", "manifest.json#capability.operation_mode", "Unknown operation mode.", "Use an accepted v0 operation mode.")

    refs = asset_index(manifest)
    missing_roles = sorted(REQUIRED_ASSET_ROLES - set(refs))
    for role in missing_roles:
        add_error(report, "asset_missing", "manifest.json#asset_refs", f"Missing asset ref role `{role}`.", "Add the required asset reference.")
    for role, asset in refs.items():
        validate_asset_ref(report, root, role, asset, capability.get("lifecycle"))
    scan_forbidden_keys(report, manifest, "manifest.json")
    return refs


def validate_asset_ref(report: Report, root: Path, role: str, asset: dict[str, Any], lifecycle: str | None) -> None:
    status = asset.get("status")
    path = asset.get("path")
    if status == "present" and path:
        if not (root / path).exists():
            add_error(report, "asset_missing", path, f"Asset ref `{role}` is marked present but file is missing.", "Create the file or mark the ref planned.")
    elif status == "planned":
        if role == "post_check":
            return
        severity = "error" if lifecycle == "stable" else "warning"
        report.issue(severity, "asset_missing", path or f"manifest.json#asset_refs.{role}", f"Asset ref `{role}` is planned, not present.", "Present this asset before stable admission.")
    else:
        add_error(report, "invalid_contract", f"manifest.json#asset_refs.{role}", "Asset ref must declare status `present` or `planned`.", "Declare a valid asset status.")


def load_present_assets(report: Report, root: Path, refs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    assets: dict[str, Any] = {}
    for role, asset in refs.items():
        if role == "post_check":
            continue
        if asset.get("status") != "present":
            if role != "post_check":
                report.ref(role, asset.get("path") or f"manifest.json#asset_refs.{role}", "planned")
            continue
        asset_path = root / str(asset.get("path", ""))
        loaded = load_json(report, root, asset_path, role)
        if loaded is not None:
            assets[role] = loaded
    return assets


def validate_schema(report: Report, role: str, schema: dict[str, Any], asset: dict[str, Any], manifest: dict[str, Any]) -> None:
    path = str(asset.get("path"))
    require_keys(report, schema, ["$schema", "$id", "type", "properties"], path)
    if schema.get("$id") != asset.get("schema_id"):
        add_error(report, "invalid_contract", path, "Schema `$id` does not match manifest asset ref.", "Keep manifest schema_id and schema `$id` identical.")
    x_lode = schema.get("x-lode") if isinstance(schema.get("x-lode"), dict) else {}
    if x_lode.get("package_ref") != manifest.get("package_ref"):
        add_error(report, "invalid_contract", path, "`x-lode.package_ref` does not match manifest.", "Bind schema metadata to the package ref.")
    if x_lode.get("schema_version") != asset.get("schema_version"):
        add_error(report, "invalid_contract", path, "`x-lode.schema_version` does not match manifest asset ref.", "Keep schema versions aligned.")
    if role == "input_schema":
        validate_input_schema(report, schema, path)
    if role == "normalized_output_schema":
        validate_output_schema(report, schema, path)
    scan_forbidden_keys(report, schema, path)


def validate_input_schema(report: Report, schema: dict[str, Any], path: str) -> None:
    properties = schema.get("properties") if isinstance(schema.get("properties"), dict) else {}
    required = schema.get("required") if isinstance(schema.get("required"), list) else []
    if "url" not in properties or "url" not in required:
        add_error(report, "invalid_contract", path, "Input schema must require `url` for the sample read package.", "Declare `url` in properties and required.")


def validate_output_schema(report: Report, schema: dict[str, Any], path: str) -> None:
    required = schema.get("required") if isinstance(schema.get("required"), list) else []
    expected = {"result_kind", "status", "classification", "normalized", "source_refs", "evidence_refs"}
    missing = sorted(expected - set(required))
    if missing:
        add_error(report, "invalid_contract", path, f"Output schema missing required fields: {', '.join(missing)}.", "Require the normalized result fields consumed by Core/App.")


def validate_resource_requirements(report: Report, resource: dict[str, Any], asset: dict[str, Any], manifest: dict[str, Any]) -> None:
    path = str(asset.get("path"))
    require_keys(report, resource, ["schema_version", "resource_requirements_id", "package_ref", "resource_requirement_profiles"], path)
    if resource.get("resource_requirements_id") != asset.get("resource_requirements_id"):
        add_error(report, "invalid_contract", path, "Resource requirements id does not match manifest asset ref.", "Keep resource requirement identity aligned.")
    if resource.get("package_ref") != manifest.get("package_ref"):
        add_error(report, "invalid_contract", path, "Resource requirements package_ref does not match manifest.", "Bind resource requirements to the package ref.")
    profiles = resource.get("resource_requirement_profiles")
    if not isinstance(profiles, list) or not profiles:
        add_error(report, "invalid_contract", path, "Resource requirements must declare at least one profile.", "Declare one offline-checkable resource requirement profile.")
    scan_forbidden_keys(report, resource, path)


def validate_lifecycle(report: Report, lifecycle: dict[str, Any], asset: dict[str, Any], manifest: dict[str, Any]) -> None:
    path = str(asset.get("path"))
    require_keys(report, lifecycle, ["schema_version", "lifecycle_metadata_id", "package_ref", "package_version", "lifecycle", "lock_input"], path)
    if lifecycle.get("lifecycle_metadata_id") != asset.get("lifecycle_metadata_id"):
        add_error(report, "invalid_contract", path, "Lifecycle metadata id does not match manifest asset ref.", "Keep lifecycle metadata identity aligned.")
    if lifecycle.get("package_ref") != manifest.get("package_ref"):
        add_error(report, "invalid_contract", path, "Lifecycle package_ref does not match manifest.", "Bind lifecycle metadata to the package ref.")
    state = nested_get(lifecycle, ["lifecycle", "state"])
    manifest_state = nested_get(manifest, ["capability", "lifecycle"])
    if state != manifest_state:
        add_error(report, "invalid_contract", path, "Lifecycle state does not match manifest capability lifecycle.", "Keep lifecycle state aligned.")
    scan_forbidden_keys(report, lifecycle, path)


def validate_failure_mapping(report: Report, failure_mapping: dict[str, Any], asset: dict[str, Any], manifest: dict[str, Any]) -> None:
    path = str(asset.get("path"))
    require_keys(
        report,
        failure_mapping,
        [
            "schema_version",
            "failure_mapping_id",
            "failure_mapping_version",
            "package_ref",
            "capability_id",
            "operation_id",
            "operation_mode",
            "classes",
        ],
        path,
    )
    if failure_mapping.get("schema_version") != "lode.failure-mapping.v0":
        add_error(report, "unsupported_version", path, "Unsupported failure mapping schema version.", "Use `lode.failure-mapping.v0`.")
    if failure_mapping.get("failure_mapping_id") != asset.get("failure_mapping_id") or failure_mapping.get("failure_mapping_version") != asset.get("failure_mapping_version"):
        add_error(report, "invalid_contract", path, "Failure mapping identity/version does not match manifest asset ref.", "Keep failure mapping metadata aligned.")
    if failure_mapping.get("package_ref") != manifest.get("package_ref"):
        add_error(report, "invalid_contract", path, "Failure mapping package_ref does not match manifest.", "Bind failure mapping to the package ref.")
    for key in ["capability_id", "operation_id", "operation_mode"]:
        if failure_mapping.get(key) != nested_get(manifest, ["capability", key]):
            add_error(report, "invalid_contract", path, f"Failure mapping `{key}` does not match manifest capability.", "Bind failure mapping to the package capability.")
    classes = failure_mapping.get("classes")
    if not isinstance(classes, list) or not classes:
        add_error(report, "invalid_contract", path, "Failure mapping must declare classes.", "Add failure class mapping entries.")
    else:
        class_ids = {item.get("lode_failure_class") for item in classes if isinstance(item, dict)}
        missing = sorted(REQUIRED_FAILURE_CLASSES - class_ids)
        if missing:
            add_error(report, "invalid_contract", path, f"Failure mapping missing required classes: {', '.join(missing)}.", "Declare the GH-98 required failure classes.")
        for item in classes:
            if isinstance(item, dict):
                require_keys(report, item, ["lode_failure_class", "trigger", "owner", "core_mapping", "app_mapping"], f"{path}#classes")
                validate_mapping_consumer(report, item.get("core_mapping"), path, "core_mapping")
                validate_mapping_consumer(report, item.get("app_mapping"), path, "app_mapping")
    scan_forbidden_keys(report, failure_mapping, path)


def validate_write_deferred_guardrail(report: Report, guardrail_doc: dict[str, Any], asset: dict[str, Any], manifest: dict[str, Any]) -> None:
    path = str(asset.get("path"))
    require_keys(
        report,
        guardrail_doc,
        [
            "schema_version",
            "guardrail_id",
            "guardrail_version",
            "package_ref",
            "capability_id",
            "operation_id",
            "operation_mode",
            "guardrail",
            "validate_only_boundary",
            "draft_preview_boundary",
            "true_write_boundary",
            "admission_guardrail",
        ],
        path,
    )
    if guardrail_doc.get("schema_version") != "lode.write-deferred-guardrail.v0":
        add_error(report, "unsupported_version", path, "Unsupported write deferred guardrail schema version.", "Use `lode.write-deferred-guardrail.v0`.")
    if guardrail_doc.get("guardrail_id") != asset.get("guardrail_id") or guardrail_doc.get("guardrail_version") != asset.get("guardrail_version"):
        add_error(report, "invalid_contract", path, "Guardrail identity/version does not match manifest asset ref.", "Keep guardrail metadata aligned.")
    if guardrail_doc.get("package_ref") != manifest.get("package_ref"):
        add_error(report, "invalid_contract", path, "Guardrail package_ref does not match manifest.", "Bind guardrail to the package ref.")
    for key in ["capability_id", "operation_id", "operation_mode"]:
        if guardrail_doc.get(key) != nested_get(manifest, ["capability", key]):
            add_error(report, "invalid_contract", path, f"Guardrail `{key}` does not match manifest capability.", "Bind guardrail to the package capability.")

    guardrail = guardrail_doc.get("guardrail") if isinstance(guardrail_doc.get("guardrail"), dict) else {}
    require_keys(report, guardrail, ["status", "applies_to_operation_modes", "current_package_allowed_modes", "blocked_claims"], f"{path}#guardrail")
    if guardrail.get("status") != "deferred":
        add_error(report, "invalid_contract", f"{path}#guardrail.status", "Write-side guardrail must remain deferred.", "Keep write-side behavior deferred until future write contracts are accepted.")
    modes = guardrail.get("applies_to_operation_modes")
    required_modes = {"validate_only", "draft", "preview", "write"}
    if not isinstance(modes, list) or not required_modes.issubset(set(modes)):
        add_error(report, "invalid_contract", f"{path}#guardrail.applies_to_operation_modes", "Guardrail must cover validate_only, draft, preview, and write modes.", "Declare every deferred write-side mode.")
    allowed_modes = guardrail.get("current_package_allowed_modes")
    if not isinstance(allowed_modes, list) or set(allowed_modes) != {"read"}:
        add_error(report, "invalid_contract", f"{path}#guardrail.current_package_allowed_modes", "Current sample package must allow only read mode.", "Keep the sample package read-only.")

    true_write = guardrail_doc.get("true_write_boundary") if isinstance(guardrail_doc.get("true_write_boundary"), dict) else {}
    require_keys(report, true_write, ["execution_status", "deferred_until"], f"{path}#true_write_boundary")
    if true_write.get("execution_status") != "deferred":
        add_error(report, "invalid_contract", f"{path}#true_write_boundary.execution_status", "True write execution must be deferred.", "Do not claim executable write capability in this package.")

    admission = guardrail_doc.get("admission_guardrail") if isinstance(guardrail_doc.get("admission_guardrail"), dict) else {}
    require_keys(report, admission, ["write_execution", "must_reject_if"], f"{path}#admission_guardrail")
    if admission.get("write_execution") != "blocked":
        add_error(report, "invalid_contract", f"{path}#admission_guardrail.write_execution", "Admission guardrail must block write execution.", "Keep write execution out of the package admission surface.")
    scan_forbidden_keys(report, guardrail_doc, path)


def validate_mapping_consumer(report: Report, mapping: Any, path: str, field: str) -> None:
    if not isinstance(mapping, dict):
        add_error(report, "invalid_contract", f"{path}#{field}", "Failure mapping consumer entry must be an object.", "Declare consumer mapping details.")
        return
    required = ["category"] if field == "core_mapping" else ["display"]
    require_keys(report, mapping, required, f"{path}#{field}")


def validate_local_registry_index(report: Report, package_root: Path, registry_path: Path, manifest: dict[str, Any]) -> None:
    registry_path = registry_path.resolve()
    repo_root = discover_repo_root(registry_path.parent) or registry_path.parent
    display_path = rel(repo_root, registry_path)
    index = load_json(report, repo_root, registry_path, "local_registry_index", display_path)
    if not isinstance(index, dict):
        return

    require_keys(report, index, ["schema_version", "index_scope", "entries"], display_path)
    if index.get("schema_version") != SUPPORTED_LOCAL_REGISTRY_VERSION:
        add_error(report, "unsupported_version", display_path, "Unsupported local registry index version.", f"Use `{SUPPORTED_LOCAL_REGISTRY_VERSION}`.")
    if index.get("index_scope") != "repo-local":
        add_error(report, "invalid_contract", display_path, "Local registry index must declare `repo-local` scope.", "Keep GH-99 resolution local to this repository.")

    entries = index.get("entries")
    if not isinstance(entries, list) or not entries:
        add_error(report, "registry_unavailable", display_path, "Local registry index has no entries.", "Add the package entry to the repo-local index.")
        scan_forbidden_keys(report, index, display_path)
        return

    matches = [(idx, entry) for idx, entry in enumerate(entries) if isinstance(entry, dict) and entry.get("package_ref") == manifest.get("package_ref")]
    if len(matches) != 1:
        add_error(report, "registry_unavailable", display_path, "Local registry index must contain exactly one entry for the package_ref.", "Add one repo-local package entry for this manifest.")
    else:
        idx, entry = matches[0]
        validate_registry_entry(report, repo_root, package_root, display_path, idx, entry, manifest)
    scan_forbidden_keys(report, index, display_path)


def validate_registry_entry(
    report: Report,
    repo_root: Path,
    package_root: Path,
    index_path: str,
    index: int,
    entry: dict[str, Any],
    manifest: dict[str, Any],
) -> None:
    entry_path = f"{index_path}#entries[{index}]"
    require_keys(
        report,
        entry,
        [
            "package_ref",
            "package_type",
            "package_path",
            "manifest_path",
            "lock_ref",
            "lock_path",
            "site_slug",
            "capability_id",
            "operation_id",
            "operation_mode",
            "version",
            "lifecycle",
            "asset_roles",
            "resolution",
        ],
        entry_path,
    )

    expected = {
        "package_type": manifest.get("package_type"),
        "site_slug": nested_get(manifest, ["site", "slug"]),
        "capability_id": nested_get(manifest, ["capability", "capability_id"]),
        "operation_id": nested_get(manifest, ["capability", "operation_id"]),
        "operation_mode": nested_get(manifest, ["capability", "operation_mode"]),
        "version": nested_get(manifest, ["capability", "version"]),
        "lifecycle": nested_get(manifest, ["capability", "lifecycle"]),
    }
    for key, value in expected.items():
        if entry.get(key) != value:
            add_error(report, "invalid_contract", f"{entry_path}.{key}", f"Registry `{key}` does not match manifest.", "Keep local registry identity aligned with the manifest.")

    package_path = entry.get("package_path")
    manifest_path = entry.get("manifest_path")
    lock_path = entry.get("lock_path")
    if not isinstance(package_path, str) or Path(package_path).is_absolute():
        add_error(report, "invalid_contract", f"{entry_path}.package_path", "Registry package_path must be repo-relative.", "Use a repo-relative package path.")
    else:
        resolved_package = (repo_root / package_path).resolve()
        if resolved_package != package_root.resolve():
            add_error(report, "invalid_contract", f"{entry_path}.package_path", "Registry package_path does not resolve to the validated package root.", "Point the entry at this package root.")

    if not isinstance(manifest_path, str) or Path(manifest_path).is_absolute():
        add_error(report, "invalid_contract", f"{entry_path}.manifest_path", "Registry manifest_path must be repo-relative.", "Use a repo-relative manifest path.")
    elif package_path and manifest_path != f"{package_path}/manifest.json":
        add_error(report, "invalid_contract", f"{entry_path}.manifest_path", "Registry manifest_path must point to the package manifest.", "Point manifest_path at the package manifest.")

    package_lock = asset_index(manifest).get("package_lock")
    if isinstance(package_lock, dict):
        expected_lock_ref = package_lock.get("lock_ref")
        expected_lock_path = f"{package_path}/{package_lock.get('path')}" if isinstance(package_path, str) and isinstance(package_lock.get("path"), str) else None
        if entry.get("lock_ref") != expected_lock_ref:
            add_error(report, "invalid_contract", f"{entry_path}.lock_ref", "Registry lock_ref does not match manifest package_lock asset ref.", "Keep local registry lock identity aligned with the manifest.")
        if lock_path != expected_lock_path:
            add_error(report, "invalid_contract", f"{entry_path}.lock_path", "Registry lock_path must point to the package lock file.", "Point lock_path at the package lock file.")

    roles = entry.get("asset_roles")
    manifest_roles = set(asset_index(manifest))
    if not isinstance(roles, list) or set(roles) != manifest_roles:
        add_error(report, "invalid_contract", f"{entry_path}.asset_roles", "Registry asset_roles must match manifest asset_refs roles.", "Keep local index discoverability aligned with the manifest.")

    resolution = entry.get("resolution") if isinstance(entry.get("resolution"), dict) else {}
    require_keys(report, resolution, ["strategy", "freshness_rule", "failure_mapping"], f"{entry_path}.resolution")
    if resolution.get("strategy") != "repo_relative_manifest":
        add_error(report, "invalid_contract", f"{entry_path}.resolution.strategy", "Registry resolution strategy must be repo_relative_manifest.", "Use local manifest resolution for GH-99.")


def validate_package_lock(report: Report, lock: dict[str, Any], asset: dict[str, Any], manifest: dict[str, Any], refs: dict[str, dict[str, Any]]) -> None:
    path = str(asset.get("path"))
    require_keys(
        report,
        lock,
        [
            "schema_version",
            "lock_id",
            "lock_version",
            "lock_ref",
            "package_ref",
            "package_version",
            "capability_id",
            "operation_id",
            "operation_mode",
            "lifecycle",
            "resolution",
            "locked_assets",
            "invalidation_behavior",
        ],
        path,
    )
    if lock.get("schema_version") != SUPPORTED_PACKAGE_LOCK_VERSION:
        add_error(report, "unsupported_version", path, "Unsupported package lock schema version.", f"Use `{SUPPORTED_PACKAGE_LOCK_VERSION}`.")
    for key in ["lock_id", "lock_version", "lock_ref"]:
        if lock.get(key) != asset.get(key):
            add_error(report, "invalid_contract", path, f"Package lock `{key}` does not match manifest asset ref.", "Keep package lock identity aligned with the manifest.")
    if lock.get("package_ref") != manifest.get("package_ref"):
        add_error(report, "invalid_contract", path, "Package lock package_ref does not match manifest.", "Bind package lock to the package ref.")
    expected = {
        "package_version": nested_get(manifest, ["capability", "version"]),
        "capability_id": nested_get(manifest, ["capability", "capability_id"]),
        "operation_id": nested_get(manifest, ["capability", "operation_id"]),
        "operation_mode": nested_get(manifest, ["capability", "operation_mode"]),
        "lifecycle": nested_get(manifest, ["capability", "lifecycle"]),
    }
    for key, value in expected.items():
        if lock.get(key) != value:
            add_error(report, "invalid_contract", f"{path}#{key}", f"Package lock `{key}` does not match manifest.", "Keep lock identity aligned with the manifest capability.")
    validate_lock_resolution(report, lock.get("resolution"), path)
    validate_locked_assets(report, lock.get("locked_assets"), refs, path)
    validate_lock_invalidation(report, lock.get("invalidation_behavior"), path)
    scan_forbidden_keys(report, lock, path)


def validate_lock_resolution(report: Report, resolution: Any, path: str) -> None:
    if not isinstance(resolution, dict):
        add_error(report, "invalid_contract", f"{path}#resolution", "Package lock resolution must be an object.", "Declare repo-local lock resolution.")
        return
    require_keys(report, resolution, ["resolution_mode", "registry_index", "package_path", "manifest_path"], f"{path}#resolution")
    if resolution.get("resolution_mode") != "repo-local":
        add_error(report, "invalid_contract", f"{path}#resolution.resolution_mode", "Package lock resolution_mode must be repo-local.", "Keep GH-100 lock resolution local.")
    if resolution.get("registry_index") != str(DEFAULT_LOCAL_REGISTRY):
        add_error(report, "invalid_contract", f"{path}#resolution.registry_index", "Package lock registry_index must point at the repo-local index.", "Use the repo-local registry index.")
    if resolution.get("package_path") != "sites/example/read-public-page" or resolution.get("manifest_path") != "sites/example/read-public-page/manifest.json":
        add_error(report, "invalid_contract", f"{path}#resolution", "Package lock resolution paths do not point at the sample package.", "Keep lock resolution aligned with the package root and manifest.")


def validate_locked_assets(report: Report, locked_assets: Any, refs: dict[str, dict[str, Any]], path: str) -> None:
    if not isinstance(locked_assets, list) or not locked_assets:
        add_error(report, "invalid_contract", f"{path}#locked_assets", "Package lock must declare locked assets.", "Lock the package asset refs consumed by Core admission.")
        return
    locked_by_role = {item.get("role"): item for item in locked_assets if isinstance(item, dict) and item.get("role")}
    expected_roles = set(refs) - {"package_lock"}
    missing = sorted(expected_roles - set(locked_by_role))
    extra = sorted(set(locked_by_role) - expected_roles)
    if missing or extra:
        add_error(report, "invalid_contract", f"{path}#locked_assets", f"Locked asset roles do not match manifest asset refs: missing={missing}, extra={extra}.", "Keep package lock asset roles aligned with the manifest.")
    for role in sorted(expected_roles & set(locked_by_role)):
        locked = locked_by_role[role]
        asset = refs[role]
        expected_ref, expected_version = asset_ref_identity(asset)
        if locked.get("path") != asset.get("path"):
            add_error(report, "invalid_contract", f"{path}#locked_assets.{role}.path", "Locked asset path does not match manifest asset ref.", "Keep locked paths aligned with manifest asset refs.")
        if locked.get("ref") != expected_ref or locked.get("version") != expected_version:
            add_error(report, "invalid_contract", f"{path}#locked_assets.{role}", "Locked asset ref/version does not match manifest asset ref.", "Keep locked asset identity aligned with manifest asset refs.")


def asset_ref_identity(asset: dict[str, Any]) -> tuple[Any, Any]:
    for ref_key, version_key in [
        ("schema_id", "schema_version"),
        ("resource_requirements_id", "resource_requirements_version"),
        ("lifecycle_metadata_id", "lifecycle_metadata_version"),
        ("fixture_id", "fixture_version"),
        ("guardrail_id", "guardrail_version"),
        ("post_check_id", "post_check_version"),
        ("failure_mapping_id", "failure_mapping_version"),
        ("lock_ref", "lock_version"),
    ]:
        if ref_key in asset or version_key in asset:
            return asset.get(ref_key), asset.get(version_key)
    return None, None


def validate_lock_invalidation(report: Report, invalidation: Any, path: str) -> None:
    if not isinstance(invalidation, dict):
        add_error(report, "invalid_contract", f"{path}#invalidation_behavior", "Package lock invalidation_behavior must be an object.", "Declare lock invalidation behavior.")
        return
    require_keys(report, invalidation, ["invalidates_lock_on", "requires_relock_on", "failure_mapping"], f"{path}#invalidation_behavior")
    for key in ["invalidates_lock_on", "requires_relock_on", "failure_mapping"]:
        value = invalidation.get(key)
        if not isinstance(value, list) or not value:
            add_error(report, "invalid_contract", f"{path}#invalidation_behavior.{key}", f"Package lock `{key}` must be a non-empty list.", "Declare concrete lock invalidation semantics.")


def validate_fixture(
    report: Report,
    fixture: dict[str, Any],
    asset: dict[str, Any],
    manifest: dict[str, Any],
    output_schema_asset: dict[str, Any],
) -> None:
    path = str(asset.get("path"))
    require_keys(report, fixture, ["schema_version", "fixture_id", "fixture_version", "package_ref", "normalized_fixture", "binding_requirements"], path)
    if fixture.get("fixture_id") != asset.get("fixture_id") or fixture.get("fixture_version") != asset.get("fixture_version"):
        add_error(report, "fixture_invalid", path, "Fixture identity/version does not match manifest asset ref.", "Keep fixture metadata aligned.")
    for key in ["package_ref", "capability_id", "operation_id", "operation_mode"]:
        if fixture.get(key) != nested_get(manifest, ["capability", key]) and key != "package_ref":
            add_error(report, "fixture_invalid", path, f"Fixture `{key}` does not match manifest capability.", "Bind fixture to the package capability.")
    if fixture.get("package_ref") != manifest.get("package_ref"):
        add_error(report, "fixture_invalid", path, "Fixture package_ref does not match manifest.", "Bind fixture to the package ref.")
    validate_fixture_payload(report, fixture, output_schema_asset, path)
    scan_forbidden_keys(report, fixture, path)


def validate_fixture_payload(report: Report, fixture: dict[str, Any], output_schema_asset: dict[str, Any], path: str) -> None:
    normalized_fixture = fixture.get("normalized_fixture") if isinstance(fixture.get("normalized_fixture"), dict) else {}
    if normalized_fixture.get("output_schema") != output_schema_asset.get("schema_id"):
        add_error(report, "fixture_invalid", path, "Fixture output_schema does not match normalized output schema ref.", "Bind fixture output to the declared output schema.")
    data = normalized_fixture.get("data") if isinstance(normalized_fixture.get("data"), dict) else {}
    validate_normalized_data(report, data, path)
    source_ids = ref_ids(fixture.get("source_refs"))
    evidence_ids = ref_ids(fixture.get("evidence_refs"))
    validate_fixture_refs(report, data, source_ids, evidence_ids, path)
    validate_bindings(report, fixture, data, source_ids, evidence_ids, path)


def validate_normalized_data(report: Report, data: dict[str, Any], path: str) -> None:
    required = ["result_kind", "status", "classification", "normalized", "source_refs", "evidence_refs"]
    missing = [key for key in required if key not in data]
    if missing:
        add_error(report, "fixture_invalid", path, f"Normalized fixture data missing: {', '.join(missing)}.", "Match the output schema required fields.")
        return
    if data.get("status") == "available":
        normalized = data.get("normalized")
        if data.get("classification") not in {"success_result", "partial_result"} or not isinstance(normalized, dict):
            add_error(report, "output_invalid", path, "Available fixture must have success/partial classification and normalized data.", "Make fixture output match the available-result schema branch.")
        else:
            missing = [key for key in ["canonical_url", "title", "summary", "source_status"] if key not in normalized]
            if missing:
                add_error(report, "output_invalid", path, f"Normalized available data missing: {', '.join(missing)}.", "Provide required public fields.")
    elif data.get("status") == "empty" and data.get("classification") != "empty_result":
        add_error(report, "output_invalid", path, "Empty fixture must use `empty_result` classification.", "Align empty-result classification.")
    elif data.get("status") == "unavailable" and data.get("classification") != "not_normalizable":
        add_error(report, "output_invalid", path, "Unavailable fixture must use `not_normalizable` classification.", "Align unavailable-result classification.")


def validate_fixture_refs(report: Report, data: dict[str, Any], source_ids: set[str], evidence_ids: set[str], path: str) -> None:
    for ref in data.get("source_refs", []):
        if isinstance(ref, dict) and ref.get("ref_id") not in source_ids:
            add_error(report, "fixture_invalid", path, f"Normalized source_ref `{ref.get('ref_id')}` is not declared.", "Declare fixture source refs before using them.")
    for ref in data.get("evidence_refs", []):
        if isinstance(ref, dict) and ref.get("ref_id") not in evidence_ids:
            add_error(report, "fixture_invalid", path, f"Normalized evidence_ref `{ref.get('ref_id')}` is not declared.", "Declare fixture evidence refs before using them.")


def validate_bindings(report: Report, fixture: dict[str, Any], data: dict[str, Any], source_ids: set[str], evidence_ids: set[str], path: str) -> None:
    requirements = fixture.get("binding_requirements") if isinstance(fixture.get("binding_requirements"), dict) else {}
    bindings = requirements.get("normalized_field_sources")
    if not isinstance(bindings, list) or not bindings:
        add_error(report, "fixture_invalid", path, "Fixture must bind normalized fields to source/evidence refs.", "Declare normalized_field_sources.")
        return
    for binding in bindings:
        if not isinstance(binding, dict):
            continue
        field = binding.get("field")
        if not isinstance(field, str) or not dotted_exists(data, field):
            add_error(report, "fixture_invalid", path, f"Binding field `{field}` is absent from normalized data.", "Bind only fields present in normalized fixture data.")
        if binding.get("source_ref") not in source_ids:
            add_error(report, "fixture_invalid", path, f"Binding source_ref `{binding.get('source_ref')}` is not declared.", "Bind to declared source refs.")
        if binding.get("evidence_ref") not in evidence_ids:
            add_error(report, "fixture_invalid", path, f"Binding evidence_ref `{binding.get('evidence_ref')}` is not declared.", "Bind to declared evidence refs.")


def validate_post_check(
    report: Report,
    root: Path,
    asset: dict[str, Any],
    manifest: dict[str, Any],
    fixture: dict[str, Any] | None,
) -> None:
    path = asset.get("path") or "manifest.json#asset_refs.post_check"
    if asset.get("status") == "planned":
        report.ref("post_check", str(path), "planned")
        add_warning(report, "asset_missing", str(path), "Post-check asset is planned until GH-97.", "Keep the package proposed until post-check requirements are present.")
        return
    loaded = load_json(report, root, root / str(path), "post_check")
    if not isinstance(loaded, dict):
        return
    require_keys(
        report,
        loaded,
        [
            "schema_version",
            "post_check_id",
            "post_check_version",
            "package_ref",
            "capability_id",
            "operation_id",
            "operation_mode",
            "result_contract",
            "requirements",
            "fixture_post_check_output",
        ],
        str(path),
    )
    if loaded.get("schema_version") != "lode.post-check.v0":
        add_error(report, "unsupported_version", str(path), "Unsupported post-check schema version.", "Use `lode.post-check.v0`.")
    if loaded.get("post_check_id") != asset.get("post_check_id") or loaded.get("post_check_version") != asset.get("post_check_version"):
        add_error(report, "invalid_contract", str(path), "Post-check identity/version does not match manifest asset ref.", "Keep post-check metadata aligned.")
    if loaded.get("package_ref") != manifest.get("package_ref"):
        add_error(report, "invalid_contract", str(path), "Post-check package_ref does not match manifest.", "Bind post-check to the package ref.")
    for key in ["capability_id", "operation_id", "operation_mode"]:
        if loaded.get(key) != nested_get(manifest, ["capability", key]):
            add_error(report, "invalid_contract", str(path), f"Post-check `{key}` does not match manifest capability.", "Bind post-check to the package capability.")
    validate_post_check_payload(report, loaded, str(path), fixture)
    scan_forbidden_keys(report, loaded, str(path))


def validate_post_check_payload(report: Report, post_check: dict[str, Any], path: str, fixture: dict[str, Any] | None) -> None:
    contract = post_check.get("result_contract") if isinstance(post_check.get("result_contract"), dict) else {}
    status_values = contract.get("status_values") if isinstance(contract.get("status_values"), list) else []
    if set(status_values) != POST_CHECK_STATUSES:
        add_error(report, "invalid_contract", path, "Post-check result_contract must declare passed/failed/skipped statuses.", "Declare the v0 post-check status vocabulary.")
    required_fields = set(contract.get("required_fields") if isinstance(contract.get("required_fields"), list) else [])
    missing_fields = sorted({"status", "reason", "source_refs", "evidence_refs"} - required_fields)
    if missing_fields:
        add_error(report, "invalid_contract", path, f"Post-check result_contract missing required fields: {', '.join(missing_fields)}.", "Require the v0 post-check output fields.")

    source_ids = ref_ids(fixture.get("source_refs")) if isinstance(fixture, dict) else set()
    evidence_ids = ref_ids(fixture.get("evidence_refs")) if isinstance(fixture, dict) else set()
    requirements = post_check.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        add_error(report, "post_check_failed", path, "Post-check must declare requirements.", "Add declarative post-check requirements.")
    else:
        for requirement in requirements:
            if isinstance(requirement, dict):
                require_keys(report, requirement, ["requirement_id", "description", "on_failure", "required_source_refs"], f"{path}#requirements")
                validate_ref_list(report, requirement.get("required_source_refs"), source_ids, path, "required_source_refs")
                validate_ref_list(report, requirement.get("required_evidence_refs", []), evidence_ids, path, "required_evidence_refs")

    fixture_output = post_check.get("fixture_post_check_output") if isinstance(post_check.get("fixture_post_check_output"), dict) else {}
    require_keys(report, fixture_output, ["status", "reason", "source_refs", "evidence_refs"], f"{path}#fixture_post_check_output")
    if fixture_output.get("status") not in POST_CHECK_STATUSES:
        add_error(report, "post_check_failed", path, "Fixture post-check output uses an unknown status.", "Use passed, failed, or skipped.")
    if not isinstance(fixture_output.get("reason"), str) or not fixture_output.get("reason"):
        add_error(report, "post_check_failed", path, "Fixture post-check output must include a reason.", "Add a human-readable reason.")
    validate_ref_list(report, fixture_output.get("source_refs"), source_ids, path, "source_refs")
    validate_ref_list(report, fixture_output.get("evidence_refs"), evidence_ids, path, "evidence_refs")


def validate_ref_list(report: Report, refs: Any, declared_ids: set[str], path: str, field: str) -> None:
    if not isinstance(refs, list):
        add_error(report, "invalid_contract", f"{path}#{field}", "Reference list must be an array.", "Declare refs as an array of ids or objects with ref_id.")
        return
    for ref in refs:
        ref_id = ref.get("ref_id") if isinstance(ref, dict) else ref
        if not isinstance(ref_id, str):
            add_error(report, "invalid_contract", f"{path}#{field}", "Reference entries must be ids or objects with ref_id.", "Use declared fixture source/evidence ref ids.")
        elif declared_ids and ref_id not in declared_ids:
            add_error(report, "post_check_failed", f"{path}#{field}", f"Post-check ref `{ref_id}` is not declared by the fixture.", "Bind post-check output to declared fixture refs.")


def nested_get(value: Any, keys: list[str]) -> Any:
    current = value
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def ref_ids(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {item.get("ref_id") for item in value if isinstance(item, dict) and isinstance(item.get("ref_id"), str)}


def dotted_exists(value: Any, dotted: str) -> bool:
    current = value
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return False
        current = current[part]
    return True


def validate_package(root: Path, registry_index: Path | None = None) -> Report:
    report = Report(root)
    manifest_path = root / "manifest.json"
    manifest = load_json(report, root, manifest_path, "manifest")
    if not isinstance(manifest, dict):
        return report
    refs = validate_manifest(report, root, manifest)
    assets = load_present_assets(report, root, refs)

    for role in ["input_schema", "normalized_output_schema"]:
        if isinstance(assets.get(role), dict):
            validate_schema(report, role, assets[role], refs[role], manifest)
    if isinstance(assets.get("resource_requirements"), dict):
        validate_resource_requirements(report, assets["resource_requirements"], refs["resource_requirements"], manifest)
    if isinstance(assets.get("version_lifecycle_metadata"), dict):
        validate_lifecycle(report, assets["version_lifecycle_metadata"], refs["version_lifecycle_metadata"], manifest)
    if isinstance(assets.get("write_deferred_guardrail"), dict):
        validate_write_deferred_guardrail(report, assets["write_deferred_guardrail"], refs["write_deferred_guardrail"], manifest)
    if isinstance(assets.get("failure_mapping"), dict):
        validate_failure_mapping(report, assets["failure_mapping"], refs["failure_mapping"], manifest)
    if isinstance(assets.get("package_lock"), dict):
        validate_package_lock(report, assets["package_lock"], refs["package_lock"], manifest, refs)
    if isinstance(assets.get("fixture"), dict) and "normalized_output_schema" in refs:
        validate_fixture(report, assets["fixture"], refs["fixture"], manifest, refs["normalized_output_schema"])
    if "post_check" in refs:
        fixture = assets.get("fixture") if isinstance(assets.get("fixture"), dict) else None
        validate_post_check(report, root, refs["post_check"], manifest, fixture)
    registry_path = registry_index or discover_local_registry(root)
    if registry_path is not None:
        validate_local_registry_index(report, root, registry_path, manifest)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate one Lode site-capability package.")
    parser.add_argument("package_root", type=Path, help="Path to a package root containing manifest.json.")
    parser.add_argument("--registry-index", type=Path, help="Optional repo-local package index to validate with the package.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report. This is the default output format.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print the JSON report.")
    args = parser.parse_args()

    root = args.package_root.resolve()
    registry_index = args.registry_index.resolve() if args.registry_index else None
    report = validate_package(root, registry_index)
    json.dump(report.to_dict(), sys.stdout, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
