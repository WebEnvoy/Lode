#!/usr/bin/env python3
"""Focused contract tests for optional result-view declarations."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable

from tools.lode_validate_package import Report, asset_index, validate_manifest, validate_result_view_declaration


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOTS = tuple(sorted(path.parent for path in (ROOT / "sites").glob("*/*/manifest.json")))
PRESENT_ROOT = ROOT / "sites" / "xiaohongshu" / "search-notes"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


class ResultViewDeclarationTests(unittest.TestCase):
    def current_errors(self, package_root: Path) -> list[dict[str, Any]]:
        manifest = load(package_root / "manifest.json")
        report = Report(package_root)
        refs = asset_index(report, manifest)
        assets = {
            "normalized_output_schema": load(package_root / refs["normalized_output_schema"]["path"]),
            "package_lock": load(package_root / refs["package_lock"]["path"]),
        }
        validate_result_view_declaration(report, package_root, load(package_root / "catalog-metadata.json"), manifest, refs, assets)
        return report.errors

    def present_errors(
        self,
        mutate: Callable[[dict[str, Any], dict[str, Any], dict[str, Any]], None] | None = None,
        compatibility: dict[str, Any] | None = None,
        resource_body: bytes = b'{"fixture":"inert result-view resource"}\n',
    ) -> list[dict[str, Any]]:
        manifest = load(PRESENT_ROOT / "manifest.json")
        catalog = load(PRESENT_ROOT / "catalog-metadata.json")
        package_lock = load(PRESENT_ROOT / "package-lock.json")
        output_schema = load(PRESENT_ROOT / "schemas/output.schema.json")
        resource_ref = "lode://result-view/xiaohongshu/search-notes/search-summary@0.1.0"
        resource_digest = hashlib.sha256(resource_body).hexdigest()
        with tempfile.TemporaryDirectory(prefix=".result-view-test-", dir=ROOT) as directory:
            package_root = Path(directory)
            report = Report(package_root)
            refs = asset_index(report, manifest)
            resource_path = package_root / "views" / "search-summary.json"
            resource_path.parent.mkdir()
            resource_path.write_bytes(resource_body)
            resource_asset = {
                "role": "result_view_resource",
                "path": "views/search-summary.json",
                "status": "present",
                "work_item": "LODE-287",
                "resource_ref": resource_ref,
                "resource_version": "0.1.0",
            }
            refs["result_view_resource"] = resource_asset
            package_lock["locked_assets"].append({
                "role": "result_view_resource",
                "path": resource_asset["path"],
                "ref": resource_ref,
                "version": "0.1.0",
                "sha256": resource_digest,
            })
            catalog["result_view"] = {
                "status": "present",
                "declaration_version": "0.1.0",
                "view_id": "search-summary",
                "view_version": "0.1.0",
                "resource_ref": resource_ref,
                "resource_path": resource_asset["path"],
                "compatible_outputs": compatibility or {
                    "schemas": [{
                        "schema_ref": refs["normalized_output_schema"]["schema_id"],
                        "schema_version": refs["normalized_output_schema"]["schema_version"],
                    }],
                },
                "integrity": {
                    "algorithm": "sha256",
                    "digest": resource_digest,
                },
                "lock_ref": refs["package_lock"]["lock_ref"],
                "fallback": "standard_renderer",
            }
            if mutate:
                mutate(catalog, refs, package_lock)
            assets = {"normalized_output_schema": output_schema, "package_lock": package_lock}
            validate_result_view_declaration(report, package_root, catalog, manifest, refs, assets)
            return report.errors

    def test_current_packages_explicitly_declare_standard_renderer_only(self) -> None:
        for package_root in PACKAGE_ROOTS:
            with self.subTest(package=package_root.relative_to(ROOT)):
                catalog = load(package_root / "catalog-metadata.json")
                self.assertEqual({"status": "absent", "fallback": "standard_renderer"}, catalog["result_view"])
                self.assertEqual([], self.current_errors(package_root))

    def test_present_schema_compatibility_is_valid(self) -> None:
        self.assertEqual([], self.present_errors())

    def test_missing_declaration_is_valid_standard_renderer_only(self) -> None:
        package_root = PRESENT_ROOT
        manifest = load(package_root / "manifest.json")
        report = Report(package_root)
        refs = asset_index(report, manifest)
        catalog = load(package_root / "catalog-metadata.json")
        catalog.pop("result_view")
        assets = {
            "normalized_output_schema": load(package_root / refs["normalized_output_schema"]["path"]),
            "package_lock": load(package_root / refs["package_lock"]["path"]),
        }
        validate_result_view_declaration(report, package_root, catalog, manifest, refs, assets)
        self.assertEqual([], report.errors)

    def test_present_result_kind_compatibility_is_valid(self) -> None:
        self.assertEqual([], self.present_errors(compatibility={"result_kinds": ["xhs_note_search"]}))

    def test_malformed_declaration_fails_closed(self) -> None:
        errors = self.present_errors(lambda catalog, _refs, _lock: catalog["result_view"].pop("view_version"))
        self.assertTrue(any(error["code"] == "invalid_contract" for error in errors))

    def test_unsupported_declaration_version_fails_closed(self) -> None:
        def mutate(catalog: dict[str, Any], _refs: dict[str, Any], _lock: dict[str, Any]) -> None:
            catalog["result_view"]["declaration_version"] = "9.9.9"

        self.assertTrue(any(error["code"] == "invalid_contract" for error in self.present_errors(mutate)))

    def test_output_schema_mismatch_fails_closed(self) -> None:
        def mutate(catalog: dict[str, Any], _refs: dict[str, Any], _lock: dict[str, Any]) -> None:
            catalog["result_view"]["compatible_outputs"]["schemas"][0]["schema_version"] = "9.9.9"

        self.assertTrue(any(error["code"] == "unsupported_version" for error in self.present_errors(mutate)))

    def test_out_of_root_resource_fails_closed(self) -> None:
        def mutate(catalog: dict[str, Any], refs: dict[str, Any], _lock: dict[str, Any]) -> None:
            catalog["result_view"]["resource_path"] = "../outside.json"
            refs["result_view_resource"]["path"] = "../outside.json"

        errors = self.present_errors(mutate)
        self.assertTrue(any("outside the capability package" in error["message"] for error in errors))

    def test_unlocked_resource_fails_closed(self) -> None:
        def mutate(_catalog: dict[str, Any], _refs: dict[str, Any], package_lock: dict[str, Any]) -> None:
            package_lock["locked_assets"] = [item for item in package_lock["locked_assets"] if item["role"] != "result_view_resource"]

        errors = self.present_errors(mutate)
        self.assertTrue(any("locked_assets" in error["message"] for error in errors))

    def test_integrity_drift_fails_closed(self) -> None:
        def mutate(catalog: dict[str, Any], _refs: dict[str, Any], _lock: dict[str, Any]) -> None:
            catalog["result_view"]["integrity"]["digest"] = "0" * 64

        errors = self.present_errors(mutate)
        self.assertTrue(any("SHA-256" in error["message"] for error in errors))

    def test_missing_locked_resource_digest_fails_closed(self) -> None:
        def mutate(_catalog: dict[str, Any], _refs: dict[str, Any], package_lock: dict[str, Any]) -> None:
            package_lock["locked_assets"][-1].pop("sha256")

        errors = self.present_errors(mutate)
        self.assertTrue(any("must include sha256" in error["message"] for error in errors))

    def test_wrong_locked_resource_digest_fails_closed(self) -> None:
        def mutate(_catalog: dict[str, Any], _refs: dict[str, Any], package_lock: dict[str, Any]) -> None:
            package_lock["locked_assets"][-1]["sha256"] = "0" * 64

        errors = self.present_errors(mutate)
        self.assertTrue(any("does not match the declaration" in error["message"] for error in errors))

    def test_coordinated_declaration_and_lock_digest_drift_fails_closed(self) -> None:
        def mutate(catalog: dict[str, Any], _refs: dict[str, Any], package_lock: dict[str, Any]) -> None:
            catalog["result_view"]["integrity"]["digest"] = "0" * 64
            package_lock["locked_assets"][-1]["sha256"] = "0" * 64

        errors = self.present_errors(mutate)
        self.assertTrue(any("does not match the resource file" in error["message"] for error in errors))

    def test_invalid_json_resource_fails_closed(self) -> None:
        errors = self.present_errors(resource_body=b'{"fixture":')
        self.assertTrue(any("not valid JSON" in error["message"] for error in errors))

    def test_non_object_json_resource_fails_closed(self) -> None:
        errors = self.present_errors(resource_body=b'["inert"]\n')
        self.assertTrue(any("must be a JSON object" in error["message"] for error in errors))

    def test_non_finite_json_constants_fail_closed(self) -> None:
        for constant in ["NaN", "Infinity", "-Infinity"]:
            with self.subTest(constant=constant):
                errors = self.present_errors(resource_body=f'{{"value":{constant}}}\n'.encode())
                self.assertTrue(any(error["code"] == "invalid_contract" and f"`{constant}`" in error["message"] for error in errors))

    def test_forbidden_resource_fields_fail_closed(self) -> None:
        for key in ["token", "runtime_session", "raw_evidence_body"]:
            with self.subTest(key=key):
                resource_body = json.dumps({"fixture": {key: "forbidden"}}).encode()
                errors = self.present_errors(resource_body=resource_body)
                self.assertTrue(any(error["code"] == "forbidden_field" and f"`{key}`" in error["message"] for error in errors))

    def test_invalid_resource_path_fails_closed_without_traceback(self) -> None:
        def mutate(catalog: dict[str, Any], refs: dict[str, Any], _lock: dict[str, Any]) -> None:
            invalid_path = "views/invalid\x00resource.json"
            catalog["result_view"]["resource_path"] = invalid_path
            refs["result_view_resource"]["path"] = invalid_path

        errors = self.present_errors(mutate)
        self.assertTrue(any(error["code"] == "invalid_contract" and "resource_path is invalid" in error["message"] for error in errors))

    def test_duplicate_manifest_resource_roles_fail_closed_in_either_order(self) -> None:
        valid = {
            "role": "result_view_resource",
            "path": "catalog-metadata.json",
            "status": "present",
            "resource_ref": "lode://result-view/xiaohongshu/search-notes/search-summary@0.1.0",
            "resource_version": "0.1.0",
        }
        conflict = {**valid, "path": "package-lock.json"}
        for order, duplicates in [("valid_first", [valid, conflict]), ("conflict_first", [conflict, valid])]:
            with self.subTest(order=order):
                manifest = load(PRESENT_ROOT / "manifest.json")
                manifest["asset_refs"].extend(duplicates)
                report = Report(PRESENT_ROOT)
                refs = validate_manifest(report, PRESENT_ROOT, manifest)
                self.assertNotIn("result_view_resource", refs)
                self.assertTrue(any("Duplicate role `result_view_resource`" in error["message"] for error in report.errors))

    def test_duplicate_locked_resource_roles_fail_closed_in_either_order(self) -> None:
        for conflict_first in [False, True]:
            with self.subTest(conflict_first=conflict_first):
                def mutate(_catalog: dict[str, Any], _refs: dict[str, Any], package_lock: dict[str, Any]) -> None:
                    valid = package_lock["locked_assets"][-1]
                    conflict = {**valid, "path": "views/conflicting.json"}
                    if conflict_first:
                        package_lock["locked_assets"].insert(0, conflict)
                    else:
                        package_lock["locked_assets"].append(conflict)

                errors = self.present_errors(mutate)
                self.assertTrue(any("Duplicate role `result_view_resource`" in error["message"] for error in errors))

    def test_resource_ref_is_package_scoped_and_immutable(self) -> None:
        def mutate(catalog: dict[str, Any], refs: dict[str, Any], package_lock: dict[str, Any]) -> None:
            drifted = "lode://result-view/xiaohongshu/search-notes/search-summary@0.2.0"
            catalog["result_view"]["resource_ref"] = drifted
            refs["result_view_resource"]["resource_ref"] = drifted
            package_lock["locked_assets"][-1]["ref"] = drifted

        errors = self.present_errors(mutate)
        self.assertTrue(any("resource identity" in error["message"] for error in errors))


if __name__ == "__main__":
    unittest.main()
