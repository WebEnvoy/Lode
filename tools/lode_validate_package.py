#!/usr/bin/env python3
"""Offline validator for a single Lode site-capability package."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SUPPORTED_MANIFEST_VERSION = "lode.site-capability.manifest.v0"
SUPPORTED_LOCAL_REGISTRY_VERSION = "lode.local-package-index.v0"
SUPPORTED_PACKAGE_LOCK_VERSION = "lode.package-lock.v0"
SUPPORTED_PACKAGE_TYPE = "site-capability"
DEFAULT_LOCAL_REGISTRY = Path("registry/local-packages.json")
ACTION_DECLARATION_SCHEMA = Path("schemas/capability-action-declaration.schema.json")
RESULT_VIEW_DECLARATION_SCHEMA = Path("schemas/result-view-declaration.schema.json")
ACTION_DECLARATION_REQUIRED_SITES = {"xiaohongshu"}  # ponytail: expand when another site's packages migrate.
SUPPORTED_OPERATION_MODES = {"read", "validate_only", "draft", "preview", "write"}
SUPPORTED_LIFECYCLE_STATES = {"proposed", "active", "suspected_broken", "broken", "deprecated"}
POST_CHECK_STATUSES = {"passed", "failed", "skipped"}
REQUIRED_FAILURE_CLASSES = {"invalid_contract", "resource_unavailable", "site_changed", "empty_result"}
REQUIRED_PREVIEW_FAILURE_CLASSES = {"preview_unavailable", "page_changed", "user_cancelled"}
REQUIRED_ASSET_ROLES = {
    "input_schema",
    "normalized_output_schema",
    "resource_requirements",
    "version_lifecycle_metadata",
    "fixture",
    "write_deferred_guardrail",
    "failure_mapping",
    "catalog_metadata",
    "package_lock",
    "repair_draft",
    "overlay_fork_metadata",
}
REQUIRED_REPAIR_FAILURE_CLASSES = {"invalid_contract", "site_changed", "post_check_failed", "evidence_expired"}
REPAIR_DRAFT_STATES = {"candidate", "validated", "promoted", "rejected"}
OVERLAY_ASSET_KINDS = {"user_overlay", "fork", "repair_draft"}
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
    x_lode = schema.get("x-lode") if isinstance(schema.get("x-lode"), dict) else {}
    if x_lode.get("operation_ref") == "lode://operation/contact_form_preview":
        preview_def = nested_get(schema, ["$defs", "contact_form_preview"]) or {}
        preview_required = set(preview_def.get("required") if isinstance(preview_def.get("required"), list) else [])
        missing_preview = sorted({"expected_change", "risk_hints", "no_submit_guard_status"} - preview_required)
        if missing_preview:
            add_error(report, "invalid_contract", path, f"Preview output schema missing fields: {', '.join(missing_preview)}.", "Declare structured expected change, risk hints, and no-submit guard status.")
        taxonomy = x_lode.get("risk_hint_taxonomy")
        required_hints = {"requires_user_review", "target_may_change", "evidence_may_stale", "no_submit_guard_required"}
        if not isinstance(taxonomy, list) or not required_hints.issubset(set(taxonomy)):
            add_error(report, "invalid_contract", f"{path}#x-lode.risk_hint_taxonomy", "Preview schema must declare risk hint taxonomy.", "Expose the Stage 6 risk hints consumed by Core/App.")


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


def validate_action_declaration(report: Report, root: Path, manifest: dict[str, Any], resource: Any) -> None:
    declaration = manifest.get("action_declaration")
    site_slug = nested_get(manifest, ["site", "slug"])
    if not isinstance(declaration, dict):
        if site_slug in ACTION_DECLARATION_REQUIRED_SITES:
            add_error(report, "invalid_contract", "manifest.json#action_declaration", "Action declaration is required for this site package.", "Declare read, prepare, commit, or destructive actions explicitly.")
        return

    repo_root = discover_repo_root(root)
    if repo_root is None:
        add_error(report, "invalid_contract", "manifest.json#action_declaration", "Repository root is unavailable for action declaration validation.", "Validate the package from a Lode repository checkout.")
        return
    schema = load_json(report, repo_root, repo_root / ACTION_DECLARATION_SCHEMA, "action_declaration_schema", str(ACTION_DECLARATION_SCHEMA))
    if not isinstance(schema, dict):
        return
    try:
        import jsonschema
    except ImportError as exc:
        add_error(report, "invalid_contract", str(ACTION_DECLARATION_SCHEMA), f"Action declaration schema validation is unavailable: {exc}", "Install requirements-validator.txt.")
        return
    try:
        jsonschema.Draft202012Validator.check_schema(schema)
        errors = sorted(jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).iter_errors(declaration), key=lambda item: list(item.absolute_path))
    except jsonschema.SchemaError as exc:
        add_error(report, "invalid_contract", str(ACTION_DECLARATION_SCHEMA), f"Action declaration schema validation is unavailable: {exc}", "Install requirements-validator.txt and fix the shared schema.")
        return
    for error in errors:
        pointer = ".".join(str(part) for part in error.absolute_path)
        path = "manifest.json#action_declaration" + (f".{pointer}" if pointer else "")
        add_error(report, "invalid_contract", path, error.message, "Conform to the shared capability action declaration schema.")
    if errors:
        return

    action_ids = [action["action_id"] for action in declaration["actions"]]
    if len(action_ids) != len(set(action_ids)):
        add_error(report, "invalid_contract", "manifest.json#action_declaration.actions", "Action ids must be unique within a capability.", "Give every concrete business action a stable action_id.")

    resource_ref = asset_index(manifest).get("resource_requirements", {})
    profiles = resource.get("resource_requirement_profiles", []) if isinstance(resource, dict) else []
    known_profile_ids = {profile.get("requirement_profile_id") for profile in profiles if isinstance(profile, dict)}
    manifest_origins = set(nested_get(manifest, ["site", "supported_origins"]) or [])
    manifest_target = nested_get(manifest, ["capability", "target_type"])
    operation_id = nested_get(manifest, ["capability", "operation_id"])
    for index, action in enumerate(declaration["actions"]):
        path = f"manifest.json#action_declaration.actions[{index}]"
        target = action["target_scope"]
        requirements = action["resource_requirements"]
        if action["action_id"] != operation_id and not action["action_id"].startswith(f"{operation_id}."):
            add_error(report, "invalid_contract", f"{path}.action_id", "Action id is outside the capability operation namespace.", "Use the operation_id or a stable operation_id suffix.")
        if target["site_slug"] != site_slug:
            add_error(report, "invalid_contract", f"{path}.target_scope.site_slug", "Target site does not match the package site.", "Bind the action to the manifest site slug.")
        if manifest_target not in target["target_types"]:
            add_error(report, "invalid_contract", f"{path}.target_scope.target_types", "Target scope does not include the package target type.", "Include the manifest capability target_type.")
        if not set(target["supported_origins"]).issubset(manifest_origins):
            add_error(report, "invalid_contract", f"{path}.target_scope.supported_origins", "Target scope widens the package supported origins.", "Use only origins declared by the manifest.")
        if requirements["path"] != resource_ref.get("path") or requirements["id"] != resource_ref.get("resource_requirements_id"):
            add_error(report, "invalid_contract", f"{path}.resource_requirements", "Action resource requirements do not match the package asset reference.", "Bind the action to the manifest resource_requirements asset.")
        if not set(requirements["profile_ids"]).issubset(known_profile_ids):
            add_error(report, "invalid_contract", f"{path}.resource_requirements.profile_ids", "Action references an unknown resource requirement profile.", "Use profile ids declared by resource-requirements.json.")


def validate_lifecycle(report: Report, lifecycle: dict[str, Any], asset: dict[str, Any], manifest: dict[str, Any]) -> None:
    path = str(asset.get("path"))
    require_keys(
        report,
        lifecycle,
        [
            "schema_version",
            "lifecycle_metadata_id",
            "package_ref",
            "package_version",
            "lifecycle_state_vocabulary",
            "lifecycle",
            "version_identity",
            "rollback",
            "lock_input",
        ],
        path,
    )
    if lifecycle.get("lifecycle_metadata_id") != asset.get("lifecycle_metadata_id"):
        add_error(report, "invalid_contract", path, "Lifecycle metadata id does not match manifest asset ref.", "Keep lifecycle metadata identity aligned.")
    if lifecycle.get("package_ref") != manifest.get("package_ref"):
        add_error(report, "invalid_contract", path, "Lifecycle package_ref does not match manifest.", "Bind lifecycle metadata to the package ref.")
    state = nested_get(lifecycle, ["lifecycle", "state"])
    manifest_state = nested_get(manifest, ["capability", "lifecycle"])
    if state != manifest_state:
        add_error(report, "invalid_contract", path, "Lifecycle state does not match manifest capability lifecycle.", "Keep lifecycle state aligned.")
    validate_lifecycle_vocabulary(report, lifecycle, path)
    validate_version_identity(report, lifecycle.get("version_identity"), manifest, path)
    validate_lifecycle_rollback(report, lifecycle.get("rollback"), manifest, path)
    scan_forbidden_keys(report, lifecycle, path)


def validate_lifecycle_vocabulary(report: Report, lifecycle: dict[str, Any], path: str) -> None:
    vocabulary = lifecycle.get("lifecycle_state_vocabulary") if isinstance(lifecycle.get("lifecycle_state_vocabulary"), dict) else {}
    states = vocabulary.get("states")
    if not isinstance(states, list) or set(states) != SUPPORTED_LIFECYCLE_STATES:
        add_error(
            report,
            "invalid_contract",
            f"{path}#lifecycle_state_vocabulary.states",
            "Lifecycle vocabulary must declare proposed, active, suspected_broken, broken, and deprecated.",
            "Expose the Stage 5 lifecycle states consumed by Core and App.",
        )
    transitions = vocabulary.get("allowed_transitions")
    if not isinstance(transitions, list) or not transitions:
        add_error(report, "invalid_contract", f"{path}#lifecycle_state_vocabulary.allowed_transitions", "Lifecycle vocabulary must declare state transitions.", "Declare promotion, suspected broken, broken, recovery, and deprecation transitions.")


def validate_version_identity(report: Report, version_identity: Any, manifest: dict[str, Any], path: str) -> None:
    if not isinstance(version_identity, dict):
        add_error(report, "invalid_contract", f"{path}#version_identity", "Lifecycle version_identity must be an object.", "Declare current/latest/default versions and compatibility range.")
        return
    require_keys(
        report,
        version_identity,
        ["version_scheme", "current_version", "latest_version", "default_locked_version", "compatibility_range", "breaking_change_requires_new_version"],
        f"{path}#version_identity",
    )
    manifest_version = nested_get(manifest, ["capability", "version"])
    if version_identity.get("current_version") != manifest_version:
        add_error(report, "invalid_contract", f"{path}#version_identity.current_version", "Lifecycle current_version does not match manifest capability version.", "Keep lifecycle version facts aligned with manifest.")
    if not isinstance(version_identity.get("compatibility_range"), str) or not version_identity.get("compatibility_range"):
        add_error(report, "invalid_contract", f"{path}#version_identity.compatibility_range", "Lifecycle compatibility_range must be a non-empty string.", "Expose a consumer-readable compatibility range.")


def validate_lifecycle_rollback(report: Report, rollback: Any, manifest: dict[str, Any], path: str) -> None:
    if not isinstance(rollback, dict):
        add_error(report, "invalid_contract", f"{path}#rollback", "Lifecycle rollback must be an object.", "Declare previous known good and rollback candidates.")
        return
    require_keys(report, rollback, ["previous_known_good", "rollback_candidates"], f"{path}#rollback")
    known_good = rollback.get("previous_known_good") if isinstance(rollback.get("previous_known_good"), dict) else {}
    require_keys(report, known_good, ["package_ref", "package_version", "lock_ref", "status"], f"{path}#rollback.previous_known_good")
    expected_package_ref = previous_patch_ref(manifest.get("package_ref"), nested_get(manifest, ["capability", "version"]))
    if known_good.get("package_ref") != expected_package_ref:
        add_error(report, "invalid_contract", f"{path}#rollback.previous_known_good.package_ref", "Previous known good package_ref does not match the preceding patch version.", "Use the current ref for an initial version and the preceding patch ref after a relock.")
    candidates = rollback.get("rollback_candidates")
    if not isinstance(candidates, list) or not candidates:
        add_error(report, "invalid_contract", f"{path}#rollback.rollback_candidates", "Rollback must declare at least one candidate.", "Expose rollback candidates as package/version/lock refs.")


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
        if failure_mapping.get("operation_id") == "contact_form_preview":
            missing_preview = sorted(REQUIRED_PREVIEW_FAILURE_CLASSES - class_ids)
            if missing_preview:
                add_error(report, "invalid_contract", path, f"Preview failure mapping missing classes: {', '.join(missing_preview)}.", "Declare preview unavailable, page changed, and user cancelled classes.")
        for item in classes:
            if isinstance(item, dict):
                require_keys(report, item, ["lode_failure_class", "trigger", "owner", "core_mapping", "app_mapping"], f"{path}#classes")
                validate_mapping_consumer(report, item.get("core_mapping"), path, "core_mapping")
                validate_mapping_consumer(report, item.get("app_mapping"), path, "app_mapping")
    scan_forbidden_keys(report, failure_mapping, path)


def validate_repair_draft(report: Report, repair: dict[str, Any], asset: dict[str, Any], manifest: dict[str, Any]) -> None:
    path = str(asset.get("path"))
    require_keys(
        report,
        repair,
        [
            "schema_version",
            "repair_draft_id",
            "repair_draft_version",
            "package_ref",
            "capability_id",
            "operation_id",
            "operation_mode",
            "failure_to_repair",
            "draft_lifecycle",
            "validation_and_promotion",
            "repair_drafts",
            "forbidden_material_policy",
        ],
        path,
    )
    if repair.get("schema_version") != "lode.repair-draft.v0":
        add_error(report, "unsupported_version", path, "Unsupported repair draft schema version.", "Use `lode.repair-draft.v0`.")
    if repair.get("repair_draft_id") != asset.get("repair_draft_id") or repair.get("repair_draft_version") != asset.get("repair_draft_version"):
        add_error(report, "invalid_contract", path, "Repair draft identity/version does not match manifest asset ref.", "Keep repair draft metadata aligned.")
    if repair.get("package_ref") != manifest.get("package_ref"):
        add_error(report, "invalid_contract", path, "Repair draft package_ref does not match manifest.", "Bind repair draft facts to the package ref.")
    for key in ["capability_id", "operation_id", "operation_mode"]:
        if repair.get(key) != nested_get(manifest, ["capability", key]):
            add_error(report, "invalid_contract", path, f"Repair draft `{key}` does not match manifest capability.", "Bind repair draft facts to the package capability.")

    mapping = repair.get("failure_to_repair")
    if not isinstance(mapping, list) or not mapping:
        add_error(report, "invalid_contract", f"{path}#failure_to_repair", "Repair draft must map failures to repair actions.", "Declare failure-to-repair mapping for App/Core.")
    else:
        classes = {item.get("failure_class") for item in mapping if isinstance(item, dict)}
        missing = sorted(REQUIRED_REPAIR_FAILURE_CLASSES - classes)
        if missing:
            add_error(report, "invalid_contract", f"{path}#failure_to_repair", f"Repair mapping missing classes: {', '.join(missing)}.", "Expose repair mappings for capability, site, post-check, and evidence failures.")
        for item in mapping:
            if isinstance(item, dict):
                require_keys(report, item, ["failure_class", "repair_owner", "draft_action", "app_summary"], f"{path}#failure_to_repair")

    lifecycle = repair.get("draft_lifecycle") if isinstance(repair.get("draft_lifecycle"), dict) else {}
    states = lifecycle.get("states")
    if not isinstance(states, list) or set(states) != REPAIR_DRAFT_STATES:
        add_error(report, "invalid_contract", f"{path}#draft_lifecycle.states", "Repair draft lifecycle must declare candidate, validated, promoted, and rejected.", "Expose the Stage 5 repair draft lifecycle.")
    transitions = lifecycle.get("allowed_transitions")
    if not isinstance(transitions, list) or not transitions:
        add_error(report, "invalid_contract", f"{path}#draft_lifecycle.allowed_transitions", "Repair draft lifecycle must declare transitions.", "Declare validation and promotion transitions.")

    validation = repair.get("validation_and_promotion") if isinstance(repair.get("validation_and_promotion"), dict) else {}
    require_keys(report, validation, ["draft_validation_checks", "promotion_checks", "promotion_target"], f"{path}#validation_and_promotion")
    promotion_target = validation.get("promotion_target") if isinstance(validation.get("promotion_target"), dict) else {}
    require_keys(report, promotion_target, ["target_kind", "package_ref", "requires_new_version"], f"{path}#validation_and_promotion.promotion_target")
    if promotion_target.get("target_kind") != "package_update":
        add_error(report, "invalid_contract", f"{path}#validation_and_promotion.promotion_target.target_kind", "Promotion target must be package_update.", "Keep repair promotion tied to Lode package update truth.")

    drafts = repair.get("repair_drafts")
    if not isinstance(drafts, list) or not drafts:
        add_error(report, "invalid_contract", f"{path}#repair_drafts", "Repair draft fixture must declare at least one draft.", "Expose an App/Core-consumable repair draft fixture.")
    else:
        for draft in drafts:
            if isinstance(draft, dict):
                require_keys(report, draft, ["draft_ref", "source_failure_class", "status", "summary", "source_refs", "asset_boundary"], f"{path}#repair_drafts")
                if draft.get("status") not in REPAIR_DRAFT_STATES:
                    add_error(report, "invalid_contract", f"{path}#repair_drafts.status", "Repair draft status is outside the lifecycle vocabulary.", "Use candidate, validated, promoted, or rejected.")
                boundary = draft.get("asset_boundary") if isinstance(draft.get("asset_boundary"), dict) else {}
                require_keys(report, boundary, ["allowed_asset_kinds", "forbidden_material"], f"{path}#repair_drafts.asset_boundary")

    policy = repair.get("forbidden_material_policy") if isinstance(repair.get("forbidden_material_policy"), dict) else {}
    require_keys(report, policy, ["raw_runtime_material", "sensitive_user_material", "private_browser_material"], f"{path}#forbidden_material_policy")
    scan_forbidden_keys(report, repair, path)


def validate_overlay_fork_metadata(report: Report, overlay: dict[str, Any], asset: dict[str, Any], manifest: dict[str, Any]) -> None:
    path = str(asset.get("path"))
    require_keys(
        report,
        overlay,
        [
            "schema_version",
            "overlay_metadata_id",
            "overlay_metadata_version",
            "package_ref",
            "capability_id",
            "operation_id",
            "operation_mode",
            "asset_boundary",
            "private_invalidation_boundary",
            "overlay_fork_examples",
            "update_acceptance",
        ],
        path,
    )
    if overlay.get("schema_version") != "lode.overlay-fork-metadata.v0":
        add_error(report, "unsupported_version", path, "Unsupported overlay/fork metadata schema version.", "Use `lode.overlay-fork-metadata.v0`.")
    if overlay.get("overlay_metadata_id") != asset.get("overlay_metadata_id") or overlay.get("overlay_metadata_version") != asset.get("overlay_metadata_version"):
        add_error(report, "invalid_contract", path, "Overlay metadata identity/version does not match manifest asset ref.", "Keep overlay/fork metadata aligned.")
    if overlay.get("package_ref") != manifest.get("package_ref"):
        add_error(report, "invalid_contract", path, "Overlay metadata package_ref does not match manifest.", "Bind overlay facts to the package ref.")
    for key in ["capability_id", "operation_id", "operation_mode"]:
        if overlay.get(key) != nested_get(manifest, ["capability", key]):
            add_error(report, "invalid_contract", path, f"Overlay metadata `{key}` does not match manifest capability.", "Bind overlay metadata to the package capability.")

    boundary = overlay.get("asset_boundary") if isinstance(overlay.get("asset_boundary"), dict) else {}
    require_keys(report, boundary, ["allowed_asset_kinds", "truth_owner", "forbidden_material"], f"{path}#asset_boundary")
    kinds = boundary.get("allowed_asset_kinds")
    if not isinstance(kinds, list) or not OVERLAY_ASSET_KINDS.issubset(set(kinds)):
        add_error(report, "invalid_contract", f"{path}#asset_boundary.allowed_asset_kinds", "Overlay boundary must declare user_overlay, fork, and repair_draft.", "Expose Stage 5 overlay/fork/draft asset kinds.")
    if boundary.get("truth_owner") != "Lode":
        add_error(report, "invalid_contract", f"{path}#asset_boundary.truth_owner", "Overlay/fork asset truth owner must be Lode.", "Do not move package truth into App/Core/Harbor.")

    invalidation = overlay.get("private_invalidation_boundary") if isinstance(overlay.get("private_invalidation_boundary"), dict) else {}
    require_keys(report, invalidation, ["private_report_status", "platform_report_status", "forbidden_private_material"], f"{path}#private_invalidation_boundary")
    if invalidation.get("private_report_status") != "local_signal_only":
        add_error(report, "invalid_contract", f"{path}#private_invalidation_boundary.private_report_status", "Private invalidation must stay local_signal_only.", "Do not store private browser material in Lode assets.")

    examples = overlay.get("overlay_fork_examples")
    if not isinstance(examples, list) or not examples:
        add_error(report, "invalid_contract", f"{path}#overlay_fork_examples", "Overlay/fork metadata must include at least one example.", "Expose a fixture App/Core can render.")
    else:
        for example in examples:
            if isinstance(example, dict):
                require_keys(report, example, ["asset_kind", "asset_ref", "source", "status", "boundary"], f"{path}#overlay_fork_examples")
                if example.get("asset_kind") not in OVERLAY_ASSET_KINDS:
                    add_error(report, "invalid_contract", f"{path}#overlay_fork_examples.asset_kind", "Overlay example asset_kind is outside the allowed vocabulary.", "Use user_overlay, fork, or repair_draft.")

    acceptance = overlay.get("update_acceptance") if isinstance(overlay.get("update_acceptance"), dict) else {}
    require_keys(report, acceptance, ["acceptance_checks", "promotion_requires", "reject_if"], f"{path}#update_acceptance")
    scan_forbidden_keys(report, overlay, path)


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
    manifest_mode = nested_get(manifest, ["capability", "operation_mode"])
    expected_status = "deferred" if manifest_mode == "read" else "active"
    if guardrail.get("status") != expected_status:
        add_error(report, "invalid_contract", f"{path}#guardrail.status", "Write-side guardrail status must match the package operation boundary.", "Use deferred for read packages and active no-submit guardrails for validate-only/draft/preview packages.")
    modes = guardrail.get("applies_to_operation_modes")
    required_modes = {"validate_only", "draft", "preview", "write"}
    if not isinstance(modes, list) or not required_modes.issubset(set(modes)):
        add_error(report, "invalid_contract", f"{path}#guardrail.applies_to_operation_modes", "Guardrail must cover validate_only, draft, preview, and write modes.", "Declare every deferred write-side mode.")
    allowed_modes = guardrail.get("current_package_allowed_modes")
    allowed_mode_set = {manifest_mode} if manifest_mode in {"read", "validate_only", "draft", "preview"} else set()
    if not isinstance(allowed_modes, list) or set(allowed_modes) != allowed_mode_set:
        add_error(report, "invalid_contract", f"{path}#guardrail.current_package_allowed_modes", "Current package allowed modes must match the manifest operation mode.", "Keep executable write out of package allowed modes.")

    true_write = guardrail_doc.get("true_write_boundary") if isinstance(guardrail_doc.get("true_write_boundary"), dict) else {}
    require_keys(report, true_write, ["execution_status", "deferred_until"], f"{path}#true_write_boundary")
    if true_write.get("execution_status") != "deferred":
        add_error(report, "invalid_contract", f"{path}#true_write_boundary.execution_status", "True write execution must be deferred.", "Do not claim executable write capability in this package.")

    admission = guardrail_doc.get("admission_guardrail") if isinstance(guardrail_doc.get("admission_guardrail"), dict) else {}
    require_keys(report, admission, ["write_execution", "must_reject_if"], f"{path}#admission_guardrail")
    if admission.get("write_execution") != "blocked":
        add_error(report, "invalid_contract", f"{path}#admission_guardrail.write_execution", "Admission guardrail must block write execution.", "Keep write execution out of the package admission surface.")
    if manifest_mode in {"validate_only", "draft", "preview"} and admission.get("no_submit_guard") != "active":
        add_error(report, "invalid_contract", f"{path}#admission_guardrail.no_submit_guard", "Write-precheck packages must declare an active no-submit guard.", "Declare no_submit_guard: active for validate-only/draft/preview packages.")
    scan_forbidden_keys(report, guardrail_doc, path)


def validate_catalog_metadata(report: Report, catalog: dict[str, Any], asset: dict[str, Any], manifest: dict[str, Any], refs: dict[str, dict[str, Any]]) -> None:
    path = str(asset.get("path"))
    require_keys(
        report,
        catalog,
        [
            "schema_version",
            "catalog_metadata_id",
            "catalog_metadata_version",
            "package_ref",
            "lock_ref",
            "capability_id",
            "operation_id",
            "operation_mode",
            "source",
            "display",
            "version",
            "status",
            "risk",
            "test_summary",
            "core_admission_fields",
            "consumer_boundary",
        ],
        path,
    )
    if catalog.get("schema_version") != "lode.catalog-metadata.v0":
        add_error(report, "unsupported_version", path, "Unsupported catalog metadata schema version.", "Use `lode.catalog-metadata.v0`.")
    if catalog.get("catalog_metadata_id") != asset.get("catalog_metadata_id") or catalog.get("catalog_metadata_version") != asset.get("catalog_metadata_version"):
        add_error(report, "invalid_contract", path, "Catalog metadata identity/version does not match manifest asset ref.", "Keep catalog metadata aligned with the manifest.")
    if catalog.get("package_ref") != manifest.get("package_ref"):
        add_error(report, "invalid_contract", path, "Catalog package_ref does not match manifest.", "Bind catalog metadata to the package ref.")
    package_lock = refs.get("package_lock") if isinstance(refs.get("package_lock"), dict) else {}
    if catalog.get("lock_ref") != package_lock.get("lock_ref"):
        add_error(report, "invalid_contract", path, "Catalog lock_ref does not match package lock asset ref.", "Expose the package lock ref App/Core must pass around.")
    for key in ["capability_id", "operation_id", "operation_mode"]:
        if catalog.get(key) != nested_get(manifest, ["capability", key]):
            add_error(report, "invalid_contract", path, f"Catalog `{key}` does not match manifest capability.", "Bind catalog metadata to the package capability.")

    display = catalog.get("display") if isinstance(catalog.get("display"), dict) else {}
    require_keys(report, display, ["name", "summary", "site_name", "category"], f"{path}#display")
    version = catalog.get("version") if isinstance(catalog.get("version"), dict) else {}
    require_keys(report, version, ["current", "latest", "default_locked", "lifecycle"], f"{path}#version")
    if version.get("current") != nested_get(manifest, ["capability", "version"]) or version.get("lifecycle") != nested_get(manifest, ["capability", "lifecycle"]):
        add_error(report, "invalid_contract", f"{path}#version", "Catalog version/lifecycle does not match manifest capability.", "Keep App-visible version facts owned by Lode.")
    if "lifecycle_state_vocabulary" in version and set(version.get("lifecycle_state_vocabulary", [])) != SUPPORTED_LIFECYCLE_STATES:
        add_error(report, "invalid_contract", f"{path}#version.lifecycle_state_vocabulary", "Catalog lifecycle_state_vocabulary must match Lode lifecycle vocabulary.", "Expose the same Stage 5 lifecycle states to App.")
    for key in ["compatibility_range", "previous_known_good", "rollback_candidates"]:
        if key not in version:
            add_error(report, "invalid_contract", f"{path}#version.{key}", f"Catalog version missing `{key}`.", "Expose lifecycle facts needed by App without storing App UI truth.")
    status = catalog.get("status") if isinstance(catalog.get("status"), dict) else {}
    require_keys(report, status, ["catalog_state", "installability", "source_health", "updated_at"], f"{path}#status")
    if status.get("installability") != "intent_only":
        add_error(report, "invalid_contract", f"{path}#status.installability", "Catalog installability must stay intent_only.", "Do not put App install truth in Lode catalog metadata.")
    risk = catalog.get("risk") if isinstance(catalog.get("risk"), dict) else {}
    require_keys(report, risk, ["level", "operation", "reason"], f"{path}#risk")
    manifest_mode = nested_get(manifest, ["capability", "operation_mode"])
    expected_risk_operation = "read" if manifest_mode == "read" else "write-precheck"
    if risk.get("operation") != expected_risk_operation:
        add_error(report, "invalid_contract", f"{path}#risk.operation", "Catalog risk operation must match the package operation boundary.", "Use read for read packages and write-precheck for validate-only/draft/preview packages.")
    admission = catalog.get("core_admission_fields") if isinstance(catalog.get("core_admission_fields"), dict) else {}
    require_keys(report, admission, ["package_ref", "version", "lock_ref", "manifest_path", "input_schema_id", "output_schema_id", "resource_requirements_id", "post_check_id", "lifecycle", "operation_mode"], f"{path}#core_admission_fields")
    if admission.get("package_ref") != manifest.get("package_ref") or admission.get("version") != nested_get(manifest, ["capability", "version"]):
        add_error(report, "invalid_contract", f"{path}#core_admission_fields", "Core admission package/version fields do not match manifest.", "Keep Core admission facts aligned with Lode package truth.")
    scan_forbidden_keys(report, catalog, path)


def validate_result_view_schema(report: Report, root: Path, declaration: Any, path: str) -> bool:
    repo_root = discover_repo_root(root)
    if repo_root is None:
        add_error(report, "invalid_contract", path, "Repository root is unavailable for result-view declaration validation.", "Validate the package from a Lode repository checkout.")
        return False
    schema = load_json(report, repo_root, repo_root / RESULT_VIEW_DECLARATION_SCHEMA, "result_view_declaration_schema", str(RESULT_VIEW_DECLARATION_SCHEMA))
    if not isinstance(schema, dict):
        return False
    try:
        import jsonschema
    except ImportError as exc:
        add_error(report, "invalid_contract", str(RESULT_VIEW_DECLARATION_SCHEMA), f"Result-view schema validation is unavailable: {exc}", "Install requirements-validator.txt.")
        return False
    try:
        jsonschema.Draft202012Validator.check_schema(schema)
        errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(declaration), key=lambda item: list(item.absolute_path))
    except jsonschema.SchemaError as exc:
        add_error(report, "invalid_contract", str(RESULT_VIEW_DECLARATION_SCHEMA), f"Result-view schema validation is unavailable: {exc}", "Install requirements-validator.txt and fix the shared schema.")
        return False
    for error in errors:
        pointer = ".".join(str(part) for part in error.absolute_path)
        error_path = path + (f".{pointer}" if pointer else "")
        add_error(report, "invalid_contract", error_path, error.message, "Conform to the shared result-view declaration schema.")
    return not errors


def package_local_path(report: Report, root: Path, value: Any, path: str) -> Path | None:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        add_error(report, "invalid_contract", path, "Result-view resource_path must be package-relative.", "Use a relative path within the capability package.")
        return None
    resolved = (root / value).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        add_error(report, "invalid_contract", path, "Result-view resource resolves outside the capability package.", "Keep result-view resources inside the package root.")
        return None
    return resolved


def validate_result_view_resource(report: Report, resource_path: Path, path: str) -> str | None:
    try:
        resource_body = resource_path.read_bytes()
    except OSError as exc:
        add_error(report, "invalid_contract", path, f"Result-view resource cannot be read: {exc}", "Make the package-local resource readable.")
        return None
    digest = hashlib.sha256(resource_body).hexdigest()
    try:
        resource = json.loads(resource_body)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        add_error(report, "invalid_contract", path, f"Result-view resource is not valid JSON: {exc}", "Provide a static JSON object for declaration version 0.1.0.")
        return digest
    if not isinstance(resource, dict):
        add_error(report, "invalid_contract", path, "Result-view resource must be a JSON object.", "Provide a static JSON object for declaration version 0.1.0.")
        return digest
    scan_forbidden_keys(report, resource, path)
    return digest


def validate_result_view_lock(
    report: Report,
    declaration: dict[str, Any],
    resource_asset: dict[str, Any],
    package_lock: Any,
    package_lock_ref: Any,
    actual_digest: str | None,
    path: str,
) -> None:
    if not isinstance(package_lock, dict) or declaration.get("lock_ref") != package_lock_ref or package_lock.get("lock_ref") != package_lock_ref:
        add_error(report, "invalid_contract", f"{path}.lock_ref", "Result-view declaration is not bound to the current package lock.", "Bind the declaration to the manifest package_lock ref.")
        return
    locked_assets = package_lock.get("locked_assets") if isinstance(package_lock.get("locked_assets"), list) else []
    locked = next((item for item in locked_assets if isinstance(item, dict) and item.get("role") == "result_view_resource"), None)
    expected_ref, expected_version = asset_ref_identity(resource_asset)
    if not isinstance(locked, dict) or locked.get("path") != resource_asset.get("path") or locked.get("ref") != expected_ref or locked.get("version") != expected_version:
        add_error(report, "invalid_contract", f"{path}.lock_ref", "Result-view resource is missing from or drifts from package locked_assets.", "Relock the exact result-view resource path, ref, and version.")
        return
    locked_digest = locked.get("sha256")
    declaration_digest = nested_get(declaration, ["integrity", "digest"])
    if not isinstance(locked_digest, str):
        add_error(report, "invalid_contract", f"{path}.lock_ref", "Locked result-view resource must include sha256.", "Lock the exact SHA-256 declared for the result-view resource.")
        return
    if locked_digest != declaration_digest:
        add_error(report, "invalid_contract", f"{path}.lock_ref", "Locked result-view resource SHA-256 does not match the declaration.", "Keep the package lock and declaration digest identical.")
    if actual_digest is not None and locked_digest != actual_digest:
        add_error(report, "invalid_contract", f"{path}.lock_ref", "Locked result-view resource SHA-256 does not match the resource file.", "Relock the digest computed from the package-local resource.")


def validate_result_view_compatibility(
    report: Report,
    declaration: dict[str, Any],
    output_asset: Any,
    output_schema: Any,
    path: str,
) -> None:
    compatible = declaration.get("compatible_outputs") if isinstance(declaration.get("compatible_outputs"), dict) else {}
    if not isinstance(output_asset, dict) or not isinstance(output_schema, dict):
        add_error(report, "invalid_contract", path, "Result-view compatibility requires the package normalized output schema.", "Bind the declaration to a valid package output schema or result kind.")
        return
    schemas = compatible.get("schemas")
    if isinstance(schemas, list) and not any(item.get("schema_ref") == output_asset.get("schema_id") and item.get("schema_version") == output_asset.get("schema_version") for item in schemas if isinstance(item, dict)):
        add_error(report, "unsupported_version", f"{path}.compatible_outputs.schemas", "Result-view declaration does not include the current output schema ref and version.", "Declare the exact current normalized output schema compatibility.")
    result_kinds = compatible.get("result_kinds")
    result_kind = nested_get(output_schema, ["properties", "result_kind", "const"])
    if isinstance(result_kinds, list) and result_kind not in result_kinds:
        add_error(report, "unsupported_version", f"{path}.compatible_outputs.result_kinds", "Result-view declaration does not include the current output result kind.", "Declare the current normalized result_kind compatibility.")


def validate_result_view_declaration(
    report: Report,
    root: Path,
    catalog: dict[str, Any],
    manifest: dict[str, Any],
    refs: dict[str, dict[str, Any]],
    assets: dict[str, Any],
) -> None:
    path = f"{refs.get('catalog_metadata', {}).get('path', 'catalog-metadata.json')}#result_view"
    declaration = catalog.get("result_view")
    resource_asset = refs.get("result_view_resource")
    if declaration is None:
        report.ref("result_view_declaration", path, "absent")
        if resource_asset is not None:
            add_error(report, "invalid_contract", path, "A result_view_resource asset requires a result-view declaration.", "Declare a locked compatible view or remove the resource asset.")
        return
    if not validate_result_view_schema(report, root, declaration, path):
        return
    if declaration["status"] == "absent":
        if resource_asset is not None:
            add_error(report, "invalid_contract", path, "Absent result-view declaration cannot retain a result_view_resource asset.", "Remove the resource asset or declare a locked compatible view.")
        return
    if not isinstance(resource_asset, dict) or resource_asset.get("status") != "present":
        add_error(report, "asset_missing", path, "Present result-view declaration requires a present result_view_resource asset.", "Add and lock the package-local result-view resource.")
        return
    expected_ref = f"lode://result-view/{nested_get(manifest, ['site', 'slug'])}/{nested_get(manifest, ['capability', 'capability_id'])}/{declaration['view_id']}@{declaration['view_version']}"
    if declaration.get("resource_ref") != expected_ref or declaration.get("resource_ref") != resource_asset.get("resource_ref") or declaration.get("view_version") != resource_asset.get("resource_version"):
        add_error(report, "invalid_contract", f"{path}.resource_ref", "Result-view resource identity does not match package, view id, version, and manifest asset ref.", "Use the immutable package-scoped result-view resource ref.")
    if declaration.get("resource_path") != resource_asset.get("path"):
        add_error(report, "invalid_contract", f"{path}.resource_path", "Result-view resource_path does not match the manifest asset ref.", "Keep catalog and manifest resource paths identical.")
    resource_path = package_local_path(report, root, declaration.get("resource_path"), f"{path}.resource_path")
    actual_digest = None
    if resource_path is not None:
        if not resource_path.is_file():
            add_error(report, "asset_missing", f"{path}.resource_path", "Result-view resource file is missing.", "Add the declared package-local resource.")
        else:
            actual_digest = validate_result_view_resource(report, resource_path, f"{path}.resource_path")
            if actual_digest is not None and actual_digest != nested_get(declaration, ["integrity", "digest"]):
                add_error(report, "invalid_contract", f"{path}.integrity.digest", "Result-view resource SHA-256 does not match the declaration.", "Refresh the digest and relock the package resource.")
    validate_result_view_lock(report, declaration, resource_asset, assets.get("package_lock"), refs.get("package_lock", {}).get("lock_ref"), actual_digest, path)
    validate_result_view_compatibility(report, declaration, refs.get("normalized_output_schema"), assets.get("normalized_output_schema"), path)


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


def validate_registry_query_fixture(report: Report, repo_root: Path, index: dict[str, Any], display_path: str) -> None:
    query_path = index.get("query_fixture_path")
    if not isinstance(query_path, str):
        add_error(report, "asset_missing", f"{display_path}#query_fixture_path", "Local registry index must point at a query fixture.", "Add a repo-relative query fixture for App/Core consumers.")
        return
    fixture = load_json(report, repo_root, repo_root / query_path, "local_registry_query_fixture", query_path)
    if not isinstance(fixture, dict):
        return
    require_keys(report, fixture, ["schema_version", "query_fixture_id", "queries"], query_path)
    queries = fixture.get("queries")
    if not isinstance(queries, list) or not queries:
        add_error(report, "invalid_contract", f"{query_path}#queries", "Registry query fixture must include at least one query.", "Expose one App/Core-readable local query example.")
    else:
        validate_write_pre_registry_query(report, queries, query_path)
    scan_forbidden_keys(report, fixture, query_path)


def validate_write_pre_registry_query(report: Report, queries: list[Any], path: str) -> None:
    write_pre_results: list[dict[str, Any]] = []
    for query in queries:
        if not isinstance(query, dict):
            continue
        for result in query.get("results", []):
            if isinstance(result, dict) and result.get("operation_mode") in {"validate_only", "draft", "preview"}:
                write_pre_results.append(result)
    if not write_pre_results:
        add_error(report, "invalid_contract", f"{path}#queries", "Registry query fixture must expose at least one write-precheck package result.", "Add a validate_only/draft/preview query result for Stage 6 consumers.")
        return
    for result in write_pre_results:
        result_path = f"{path}#queries.write_pre_result"
        if result.get("no_submit_guard") != "active":
            add_error(report, "invalid_contract", f"{result_path}.no_submit_guard", "Write-precheck registry result must declare an active no-submit guard.", "Expose no_submit_guard: active for Core admission.")
        if result.get("true_write_execution") != "blocked":
            add_error(report, "invalid_contract", f"{result_path}.true_write_execution", "Write-precheck registry result must block true write execution.", "Expose true_write_execution: blocked.")
        candidate = result.get("write_pre_candidate") if isinstance(result.get("write_pre_candidate"), dict) else {}
        require_keys(
            report,
            candidate,
            ["candidate_id", "candidate_status", "selection_reason", "supported_stage6_modes", "draft_preview_fixture_path", "core_consumption_fixture_path"],
            f"{result_path}.write_pre_candidate",
        )
        modes = candidate.get("supported_stage6_modes")
        if not isinstance(modes, list) or not {"validate_only", "draft", "preview"}.issubset(set(modes)):
            add_error(report, "invalid_contract", f"{result_path}.write_pre_candidate.supported_stage6_modes", "Write-pre candidate must declare validate_only, draft, and preview fixture coverage.", "Expose the Stage 6 fixture modes without claiming executable write.")
        for key in ["draft_preview_fixture_path", "core_consumption_fixture_path"]:
            candidate_path = candidate.get(key)
            if not isinstance(candidate_path, str) or not candidate_path:
                continue
            if Path(candidate_path).is_absolute() or not candidate_path.endswith(".json"):
                add_error(report, "invalid_contract", f"{result_path}.write_pre_candidate.{key}", "Candidate fixture path must be a repo-relative JSON path.", "Use a repo-relative fixture path.")


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
            "updated_at",
            "version_status",
            "rollback",
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
    if "lifecycle_state_vocabulary" in entry and set(entry.get("lifecycle_state_vocabulary", [])) != SUPPORTED_LIFECYCLE_STATES:
        add_error(report, "invalid_contract", f"{entry_path}.lifecycle_state_vocabulary", "Registry lifecycle_state_vocabulary must match Lode lifecycle vocabulary.", "Expose the same Stage 5 lifecycle states to consumers.")
    validate_registry_version_status(report, entry.get("version_status"), entry_path, manifest)
    validate_registry_rollback(report, entry.get("rollback"), entry_path, manifest, entry.get("lock_ref"))

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


def validate_registry_version_status(report: Report, version_status: Any, entry_path: str, manifest: dict[str, Any]) -> None:
    if not isinstance(version_status, dict):
        add_error(report, "invalid_contract", f"{entry_path}.version_status", "Registry version_status must be an object.", "Expose current/latest/default/compatibility facts for consumers.")
        return
    require_keys(report, version_status, ["current", "latest", "default_locked", "compatibility_range"], f"{entry_path}.version_status")
    manifest_version = nested_get(manifest, ["capability", "version"])
    if version_status.get("current") != manifest_version:
        add_error(report, "invalid_contract", f"{entry_path}.version_status.current", "Registry current version does not match manifest.", "Keep registry version facts aligned.")


def validate_registry_rollback(report: Report, rollback: Any, entry_path: str, manifest: dict[str, Any], lock_ref: Any) -> None:
    if not isinstance(rollback, dict):
        add_error(report, "invalid_contract", f"{entry_path}.rollback", "Registry rollback must be an object.", "Expose previous known good refs for App/Core.")
        return
    require_keys(report, rollback, ["previous_known_good_ref", "previous_known_good_lock_ref", "status"], f"{entry_path}.rollback")
    version = nested_get(manifest, ["capability", "version"])
    if rollback.get("previous_known_good_ref") != previous_patch_ref(manifest.get("package_ref"), version):
        add_error(report, "invalid_contract", f"{entry_path}.rollback.previous_known_good_ref", "Registry previous known good package ref does not match the preceding patch version.", "Expose the current ref for an initial version or the preceding patch ref after relock.")
    if rollback.get("previous_known_good_lock_ref") != previous_patch_ref(lock_ref, version):
        add_error(report, "invalid_contract", f"{entry_path}.rollback.previous_known_good_lock_ref", "Registry previous known good lock ref does not match the preceding patch version.", "Keep rollback lock refs aligned with package version history.")


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
    validate_lock_resolution(report, lock.get("resolution"), path, manifest)
    validate_lock_compatibility(report, lock.get("compatibility"), manifest, path)
    validate_lock_rollback(report, lock.get("rollback"), manifest, refs, path)
    validate_locked_assets(report, lock.get("locked_assets"), refs, path)
    validate_lock_invalidation(report, lock.get("invalidation_behavior"), path)
    scan_forbidden_keys(report, lock, path)


def validate_lock_resolution(report: Report, resolution: Any, path: str, manifest: dict[str, Any]) -> None:
    if not isinstance(resolution, dict):
        add_error(report, "invalid_contract", f"{path}#resolution", "Package lock resolution must be an object.", "Declare repo-local lock resolution.")
        return
    require_keys(report, resolution, ["resolution_mode", "registry_index", "package_path", "manifest_path"], f"{path}#resolution")
    if resolution.get("resolution_mode") != "repo-local":
        add_error(report, "invalid_contract", f"{path}#resolution.resolution_mode", "Package lock resolution_mode must be repo-local.", "Keep GH-100 lock resolution local.")
    if resolution.get("registry_index") != str(DEFAULT_LOCAL_REGISTRY):
        add_error(report, "invalid_contract", f"{path}#resolution.registry_index", "Package lock registry_index must point at the repo-local index.", "Use the repo-local registry index.")
    expected_package_path = f"sites/{nested_get(manifest, ['site', 'slug'])}/{nested_get(manifest, ['capability', 'capability_id'])}"
    expected_manifest_path = f"{expected_package_path}/manifest.json"
    if resolution.get("package_path") != expected_package_path or resolution.get("manifest_path") != expected_manifest_path:
        add_error(report, "invalid_contract", f"{path}#resolution", "Package lock resolution paths do not point at the package manifest.", "Keep lock resolution aligned with the package root and manifest.")


def validate_lock_compatibility(report: Report, compatibility: Any, manifest: dict[str, Any], path: str) -> None:
    if not isinstance(compatibility, dict):
        add_error(report, "invalid_contract", f"{path}#compatibility", "Package lock compatibility must be an object.", "Declare locked package version compatibility.")
        return
    require_keys(report, compatibility, ["package_version", "compatible_version_range", "breaking_change_policy_ref"], f"{path}#compatibility")
    if compatibility.get("package_version") != nested_get(manifest, ["capability", "version"]):
        add_error(report, "invalid_contract", f"{path}#compatibility.package_version", "Compatibility package_version does not match manifest.", "Keep lock compatibility aligned with manifest.")


def validate_lock_rollback(report: Report, rollback: Any, manifest: dict[str, Any], refs: dict[str, dict[str, Any]], path: str) -> None:
    if not isinstance(rollback, dict):
        add_error(report, "invalid_contract", f"{path}#rollback", "Package lock rollback must be an object.", "Declare previous known good lock refs.")
        return
    require_keys(report, rollback, ["previous_known_good_ref", "previous_known_good_lock_ref", "status"], f"{path}#rollback")
    package_lock = refs.get("package_lock") if isinstance(refs.get("package_lock"), dict) else {}
    version = nested_get(manifest, ["capability", "version"])
    if rollback.get("previous_known_good_ref") != previous_patch_ref(manifest.get("package_ref"), version):
        add_error(report, "invalid_contract", f"{path}#rollback.previous_known_good_ref", "Rollback package ref does not match the preceding patch version.", "Expose the current ref for an initial version or the preceding patch ref after relock.")
    if rollback.get("previous_known_good_lock_ref") != previous_patch_ref(package_lock.get("lock_ref"), version):
        add_error(report, "invalid_contract", f"{path}#rollback.previous_known_good_lock_ref", "Rollback lock ref does not match the preceding patch version.", "Keep rollback lock refs aligned with package version history.")


def previous_patch_ref(ref: Any, version: Any) -> Any:
    if not isinstance(ref, str) or not isinstance(version, str):
        return ref
    parts = version.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        return ref
    patch = int(parts[2])
    if patch == 0:
        return ref
    previous = f"{parts[0]}.{parts[1]}.{patch - 1}"
    suffix = f"@{version}"
    return f"{ref[:-len(suffix)]}@{previous}" if ref.endswith(suffix) else ref


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
        ("catalog_metadata_id", "catalog_metadata_version"),
        ("resource_ref", "resource_version"),
        ("repair_draft_id", "repair_draft_version"),
        ("overlay_metadata_id", "overlay_metadata_version"),
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
    output_schema: dict[str, Any],
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
    validate_fixture_payload(report, fixture, output_schema_asset, output_schema, path)
    scan_forbidden_keys(report, fixture, path)


def validate_fixture_payload(report: Report, fixture: dict[str, Any], output_schema_asset: dict[str, Any], output_schema: dict[str, Any], path: str) -> None:
    normalized_fixture = fixture.get("normalized_fixture") if isinstance(fixture.get("normalized_fixture"), dict) else {}
    if normalized_fixture.get("output_schema") != output_schema_asset.get("schema_id"):
        add_error(report, "fixture_invalid", path, "Fixture output_schema does not match normalized output schema ref.", "Bind fixture output to the declared output schema.")
    data = normalized_fixture.get("data") if isinstance(normalized_fixture.get("data"), dict) else {}
    validate_normalized_data(report, data, path)
    source_ids = ref_ids(fixture.get("source_refs"))
    evidence_ids = ref_ids(fixture.get("evidence_refs"))
    validate_fixture_refs(report, data, source_ids, evidence_ids, path)
    validate_bindings(report, fixture, data, source_ids, evidence_ids, output_schema, path)


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


def validate_bindings(report: Report, fixture: dict[str, Any], data: dict[str, Any], source_ids: set[str], evidence_ids: set[str], output_schema: dict[str, Any], path: str) -> None:
    requirements = fixture.get("binding_requirements") if isinstance(fixture.get("binding_requirements"), dict) else {}
    bindings = requirements.get("normalized_field_sources")
    if not isinstance(bindings, list) or not bindings:
        add_error(report, "fixture_invalid", path, "Fixture must bind normalized fields to source/evidence refs.", "Declare normalized_field_sources.")
        return
    required_public = nested_get(output_schema, ["$defs", "content_detail", "required"])
    operation_ref = nested_get(output_schema, ["x-lode", "operation_ref"])
    if operation_ref in {"lode://operation/xhs_read_note_detail", "lode://operation/boss_read_job_detail"} and isinstance(required_public, list):
        expected_fields = {f"normalized.{field}" for field in required_public}
        actual_fields = {binding.get("field") for binding in bindings if isinstance(binding, dict)}
        if actual_fields != expected_fields:
            missing = sorted(expected_fields - actual_fields)
            extra = sorted(actual_fields - expected_fields)
            add_error(report, "fixture_invalid", path, f"Fixture binding coverage must exactly match required public fields: missing={missing}, extra={extra}.", "Bind every required normalized public field exactly once.")
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
        declared_binding_fields: set[str] = set()
        for requirement in requirements:
            if isinstance(requirement, dict):
                require_keys(report, requirement, ["requirement_id", "description", "on_failure", "required_source_refs"], f"{path}#requirements")
                validate_ref_list(report, requirement.get("required_source_refs"), source_ids, path, "required_source_refs")
                validate_ref_list(report, requirement.get("required_evidence_refs", []), evidence_ids, path, "required_evidence_refs")
                fields = requirement.get("required_binding_fields")
                if isinstance(fields, list):
                    declared_binding_fields.update(field for field in fields if isinstance(field, str))
        fixture_bindings = nested_get(fixture, ["binding_requirements", "normalized_field_sources"]) if isinstance(fixture, dict) else None
        expected_binding_fields = {binding.get("field") for binding in fixture_bindings if isinstance(binding, dict)} if isinstance(fixture_bindings, list) else set()
        if post_check.get("operation_id") in {"xhs_read_note_detail", "boss_read_job_detail"} and expected_binding_fields and declared_binding_fields != expected_binding_fields:
            add_error(report, "post_check_failed", path, f"Post-check binding coverage must exactly match fixture public bindings: missing={sorted(expected_binding_fields - declared_binding_fields)}, extra={sorted(declared_binding_fields - expected_binding_fields)}.", "Require every normalized public field in the field-source-binding post-check.")

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


def validate_core_consumption_fixture(report: Report, package_root: Path, fixture: dict[str, Any], manifest: dict[str, Any], refs: dict[str, dict[str, Any]]) -> None:
    path = str(refs.get("core_consumption_fixture", {}).get("path", "core-consumption.fixture.json"))
    expected = nested_get(fixture, ["repo_local_resolution", "expected_registry_entry"])
    if not isinstance(expected, dict):
        add_error(report, "fixture_invalid", path, "Core-consumption fixture must declare expected_registry_entry.", "Bind the fixture to the current repo-local registry entry.")
        return
    repo_root = discover_repo_root(package_root) or package_root
    registry = load_json(report, repo_root, repo_root / DEFAULT_LOCAL_REGISTRY, "local_registry_index", str(DEFAULT_LOCAL_REGISTRY))
    entries = registry.get("entries") if isinstance(registry, dict) else None
    matches = [entry for entry in entries if isinstance(entry, dict) and entry.get("package_ref") == manifest.get("package_ref")] if isinstance(entries, list) else []
    if len(matches) != 1:
        add_error(report, "fixture_invalid", path, "Core-consumption fixture package_ref must resolve to exactly one registry entry.", "Relock the fixture and registry together.")
        return
    actual = matches[0]
    required_keys = ["package_ref", "package_type", "site_slug", "capability_id", "operation_id", "operation_mode", "version", "lifecycle"]
    for key in required_keys:
        if expected.get(key) != actual.get(key):
            add_error(report, "fixture_invalid", f"{path}#expected_registry_entry.{key}", f"Expected registry `{key}` does not match current registry truth.", "Refresh the Core-consumption fixture after package relock.")
    lock_ref = refs.get("package_lock", {}).get("lock_ref")
    if fixture.get("package_ref") != manifest.get("package_ref") or fixture.get("lock_ref") != lock_ref:
        add_error(report, "fixture_invalid", path, "Core-consumption fixture package/lock refs do not match manifest truth.", "Bind the fixture to the current package and lock refs.")


def validate_package(root: Path, registry_index: Path | None = None) -> Report:
    report = Report(root)
    manifest_path = root / "manifest.json"
    manifest = load_json(report, root, manifest_path, "manifest")
    if not isinstance(manifest, dict):
        return report
    refs = validate_manifest(report, root, manifest)
    assets = load_present_assets(report, root, refs)

    validate_action_declaration(report, root, manifest, assets.get("resource_requirements"))
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
    if isinstance(assets.get("repair_draft"), dict):
        validate_repair_draft(report, assets["repair_draft"], refs["repair_draft"], manifest)
    if isinstance(assets.get("overlay_fork_metadata"), dict):
        validate_overlay_fork_metadata(report, assets["overlay_fork_metadata"], refs["overlay_fork_metadata"], manifest)
    if isinstance(assets.get("catalog_metadata"), dict):
        validate_catalog_metadata(report, assets["catalog_metadata"], refs["catalog_metadata"], manifest, refs)
        validate_result_view_declaration(report, root, assets["catalog_metadata"], manifest, refs, assets)
    if isinstance(assets.get("package_lock"), dict):
        validate_package_lock(report, assets["package_lock"], refs["package_lock"], manifest, refs)
    if isinstance(assets.get("fixture"), dict) and "normalized_output_schema" in refs:
        validate_fixture(report, assets["fixture"], refs["fixture"], manifest, refs["normalized_output_schema"], assets["normalized_output_schema"])
    if isinstance(assets.get("core_consumption_fixture"), dict):
        validate_core_consumption_fixture(report, root, assets["core_consumption_fixture"], manifest, refs)
    if "post_check" in refs:
        fixture = assets.get("fixture") if isinstance(assets.get("fixture"), dict) else None
        validate_post_check(report, root, refs["post_check"], manifest, fixture)
    registry_path = registry_index or discover_local_registry(root)
    if registry_path is not None:
        validate_local_registry_index(report, root, registry_path, manifest)
    return report


def validate_registry_packages(registry_index: Path) -> dict[str, Any]:
    registry_index = registry_index.resolve()
    repo_root = discover_repo_root(registry_index.parent) or registry_index.parent
    index_report = Report(repo_root)
    index = load_json(index_report, repo_root, registry_index, "local_registry_index", rel(repo_root, registry_index))
    package_reports: list[dict[str, Any]] = []
    runtime_consumption_report: dict[str, Any] = {"status": "not_checked", "errors": []}
    detail_consumption_report: dict[str, Any] = {"status": "not_checked", "errors": []}
    if isinstance(index, dict):
        validate_registry_query_fixture(index_report, repo_root, index, rel(repo_root, registry_index))
        entries = index.get("entries")
        if not isinstance(entries, list) or not entries:
            add_error(index_report, "registry_unavailable", rel(repo_root, registry_index), "Local registry index has no entries.", "Add repo-local package entries before batch validation.")
        else:
            for idx, entry in enumerate(entries):
                if not isinstance(entry, dict):
                    add_error(index_report, "invalid_contract", f"{rel(repo_root, registry_index)}#entries[{idx}]", "Registry entry must be an object.", "Use object entries with package_path.")
                    continue
                package_path = entry.get("package_path")
                if not isinstance(package_path, str) or Path(package_path).is_absolute():
                    add_error(index_report, "invalid_contract", f"{rel(repo_root, registry_index)}#entries[{idx}].package_path", "Registry package_path must be repo-relative.", "Use repo-relative package paths.")
                    continue
                package_root = repo_root / package_path
                report = validate_package(package_root, registry_index)
                package_reports.append(report.to_dict())
        try:
            from validate_validate_only_runtime_consumption import load_json as load_consumption_json
            from validate_validate_only_runtime_consumption import validate as validate_runtime_consumption

            consumption_errors = validate_runtime_consumption(load_consumption_json(repo_root / "registry/validate-only-runtime-consumption.json"))
            runtime_consumption_report = {"status": "failed" if consumption_errors else "passed", "errors": consumption_errors}
        except (ImportError, OSError, json.JSONDecodeError) as exc:
            runtime_consumption_report = {"status": "failed", "errors": [f"validate-only runtime-consumption validation unavailable: {exc}"]}
        try:
            from validate_detail_runtime_consumption import load as load_detail_consumption
            from validate_detail_runtime_consumption import validate as validate_detail_consumption

            detail_errors = validate_detail_consumption(load_detail_consumption(repo_root / "registry/detail-runtime-consumption.json"))
            detail_consumption_report = {"status": "failed" if detail_errors else "passed", "errors": detail_errors}
        except (ImportError, OSError, json.JSONDecodeError) as exc:
            detail_consumption_report = {"status": "failed", "errors": [f"detail runtime-consumption validation unavailable: {exc}"]}
    status = "failed" if index_report.errors or runtime_consumption_report["status"] == "failed" or detail_consumption_report["status"] == "failed" or any(report.get("status") == "failed" for report in package_reports) else "passed"
    return {
        "schema_version": "lode-registry-validation-report.v0",
        "status": status,
        "registry_index": rel(repo_root, registry_index),
        "index_report": index_report.to_dict(),
        "package_reports": package_reports,
        "validate_only_runtime_consumption": runtime_consumption_report,
        "detail_runtime_consumption": detail_consumption_report,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate one Lode site-capability package.")
    parser.add_argument("package_root", nargs="?", type=Path, help="Path to a package root containing manifest.json.")
    parser.add_argument("--registry-index", type=Path, help="Optional repo-local package index to validate with the package.")
    parser.add_argument("--all", action="store_true", help="Validate every package listed by --registry-index.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report. This is the default output format.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print the JSON report.")
    args = parser.parse_args()

    if args.all:
        if args.registry_index is None:
            parser.error("--all requires --registry-index")
        batch_report = validate_registry_packages(args.registry_index)
        json.dump(batch_report, sys.stdout, indent=2 if args.pretty else None)
        sys.stdout.write("\n")
        return 1 if batch_report["status"] == "failed" else 0
    if args.package_root is None:
        parser.error("package_root is required unless --all is used")

    root = args.package_root.resolve()
    registry_index = args.registry_index.resolve() if args.registry_index else None
    report = validate_package(root, registry_index)
    json.dump(report.to_dict(), sys.stdout, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
