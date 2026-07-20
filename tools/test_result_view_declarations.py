#!/usr/bin/env python3
"""Focused contract tests for optional result-view declarations."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable

from tools.lode_validate_package import Report, asset_index, validate_result_view_declaration


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOTS = tuple(sorted(path.parent for path in (ROOT / "sites").glob("*/*/manifest.json")))
PRESENT_ROOT = ROOT / "sites" / "xiaohongshu" / "search-notes"


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


class ResultViewDeclarationTests(unittest.TestCase):
    def current_errors(self, package_root: Path) -> list[dict[str, Any]]:
        manifest = load(package_root / "manifest.json")
        refs = asset_index(manifest)
        assets = {
            "normalized_output_schema": load(package_root / refs["normalized_output_schema"]["path"]),
            "package_lock": load(package_root / refs["package_lock"]["path"]),
        }
        report = Report(package_root)
        validate_result_view_declaration(report, package_root, load(package_root / "catalog-metadata.json"), manifest, refs, assets)
        return report.errors

    def present_errors(
        self,
        mutate: Callable[[dict[str, Any], dict[str, Any], dict[str, Any]], None] | None = None,
        compatibility: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        manifest = load(PRESENT_ROOT / "manifest.json")
        catalog = load(PRESENT_ROOT / "catalog-metadata.json")
        package_lock = load(PRESENT_ROOT / "package-lock.json")
        output_schema = load(PRESENT_ROOT / "schemas/output.schema.json")
        refs = asset_index(manifest)
        resource_ref = "lode://result-view/xiaohongshu/search-notes/search-summary@0.1.0"
        resource_body = b'{"fixture":"inert result-view resource"}\n'
        with tempfile.TemporaryDirectory(prefix=".result-view-test-", dir=ROOT) as directory:
            package_root = Path(directory)
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
                    "digest": hashlib.sha256(resource_body).hexdigest(),
                },
                "lock_ref": refs["package_lock"]["lock_ref"],
                "fallback": "standard_renderer",
            }
            if mutate:
                mutate(catalog, refs, package_lock)
            report = Report(package_root)
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
        refs = asset_index(manifest)
        catalog = load(package_root / "catalog-metadata.json")
        catalog.pop("result_view")
        assets = {
            "normalized_output_schema": load(package_root / refs["normalized_output_schema"]["path"]),
            "package_lock": load(package_root / refs["package_lock"]["path"]),
        }
        report = Report(package_root)
        validate_result_view_declaration(report, package_root, catalog, manifest, refs, assets)
        self.assertEqual([], report.errors)

    def test_present_result_kind_compatibility_is_valid(self) -> None:
        self.assertEqual([], self.present_errors(compatibility={"result_kinds": ["xhs_note_search"]}))

    def test_malformed_declaration_fails_closed(self) -> None:
        errors = self.present_errors(lambda catalog, _refs, _lock: catalog["result_view"].pop("view_version"))
        self.assertTrue(any(error["code"] == "invalid_contract" for error in errors))

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
