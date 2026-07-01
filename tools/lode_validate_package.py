#!/usr/bin/env python3
"""Offline validator for a single Lode site-capability package."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SUPPORTED_MANIFEST_VERSION = "lode.site-capability.manifest.v0"
SUPPORTED_PACKAGE_TYPE = "site-capability"
SUPPORTED_OPERATION_MODES = {"read", "validate_only", "draft", "preview", "write"}
REQUIRED_ASSET_ROLES = {
    "input_schema",
    "normalized_output_schema",
    "resource_requirements",
    "version_lifecycle_metadata",
    "fixture",
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


def load_json(report: Report, root: Path, path: Path, role: str) -> Any | None:
    display_path = rel(root, path)
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


def validate_post_check(report: Report, root: Path, asset: dict[str, Any]) -> None:
    path = asset.get("path") or "manifest.json#asset_refs.post_check"
    if asset.get("status") == "planned":
        report.ref("post_check", str(path), "planned")
        add_warning(report, "asset_missing", str(path), "Post-check asset is planned until GH-97.", "Keep the package proposed until post-check requirements are present.")
        return
    loaded = load_json(report, root, root / str(path), "post_check")
    if not isinstance(loaded, dict):
        return
    if not loaded.get("requirements"):
        add_error(report, "post_check_failed", str(path), "Post-check must declare requirements.", "Add declarative post-check requirements.")
    scan_forbidden_keys(report, loaded, str(path))


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


def validate_package(root: Path) -> Report:
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
    if isinstance(assets.get("fixture"), dict) and "normalized_output_schema" in refs:
        validate_fixture(report, assets["fixture"], refs["fixture"], manifest, refs["normalized_output_schema"])
    if "post_check" in refs:
        validate_post_check(report, root, refs["post_check"])
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate one Lode site-capability package.")
    parser.add_argument("package_root", type=Path, help="Path to a package root containing manifest.json.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report. This is the default output format.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print the JSON report.")
    args = parser.parse_args()

    root = args.package_root.resolve()
    report = validate_package(root)
    json.dump(report.to_dict(), sys.stdout, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
