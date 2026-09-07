#!/usr/bin/env python3
"""Focused contract tests for capability action declarations."""

from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path
from typing import Any, Callable

from tools.lode_validate_package import Report, validate_action_declaration


ROOT = Path(__file__).resolve().parents[1]
XHS_PACKAGES = ("search-notes", "read-note-detail", "publish-note-precheck", "publish-note-image-text-commit")


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


class ActionDeclarationTests(unittest.TestCase):
    def manifest(self, package: str) -> dict[str, Any]:
        return load(ROOT / "sites" / "xiaohongshu" / package / "manifest.json")

    def errors(self, package: str, manifest: dict[str, Any]) -> list[dict[str, Any]]:
        package_root = ROOT / "sites" / "xiaohongshu" / package
        report = Report(package_root)
        validate_action_declaration(report, package_root, manifest, load(package_root / "resource-requirements.json"))
        return report.errors

    def test_current_xiaohongshu_packages(self) -> None:
        for package in XHS_PACKAGES:
            with self.subTest(package=package):
                self.assertEqual([], self.errors(package, self.manifest(package)))

    def test_all_four_categories(self) -> None:
        cases = {
            "read": [],
            "prepare": [],
            "commit": ["submit"],
            "destructive": ["delete"],
        }
        for category, effects in cases.items():
            with self.subTest(category=category):
                manifest = self.manifest("publish-note-precheck")
                action = manifest["action_declaration"]["actions"][0]
                action["category"] = category
                action["external_effects"] = effects
                self.assertEqual([], self.errors("publish-note-precheck", manifest))

    def test_multiple_actions_may_share_a_category(self) -> None:
        manifest = self.manifest("search-notes")
        second = copy.deepcopy(manifest["action_declaration"]["actions"][0])
        second["action_id"] = "xhs_search_notes.read_next_page"
        manifest["action_declaration"]["actions"].append(second)
        self.assertEqual([], self.errors("search-notes", manifest))

    def test_cleanup_is_exact_destructive_delete_with_required_provenance(self) -> None:
        package_root = ROOT / "sites" / "xiaohongshu" / "publish-note-image-text-commit"
        manifest = load(package_root / "manifest.json")
        resources = load(package_root / "resource-requirements.json")
        fixture = load(package_root / "fixtures" / "core-consumption.fixture.json")
        action = next(item for item in manifest["action_declaration"]["actions"] if item["action_id"].endswith(".cleanup"))
        profile = next(item for item in resources["resource_requirement_profiles"] if item["action_id"].endswith(".cleanup"))
        facts = {item["fact_key"] for item in profile["required_harbor_facts"]}
        required = {
            "snapshot.cleanup_control.available",
            "business_state.cleanup_marker.unique_match",
            "business_state.cleanup_target.task_created",
            "business_state.cleanup_content.matched",
        }
        self.assertEqual("destructive", action["category"])
        self.assertEqual(["delete"], action["external_effects"])
        self.assertTrue(required <= facts)
        for missing in required:
            with self.subTest(missing=missing):
                self.assertFalse(required <= (facts - {missing}))
        cleanup_inputs = [item for item in fixture["admission_fixture"]["input_instances"] if item["action_id"].endswith(".cleanup")]
        self.assertEqual(1, len(cleanup_inputs))
        self.assertEqual("delete", fixture["safety_boundary"]["external_effects"][cleanup_inputs[0]["action_id"]])
        self.assertNotIn("cleanup", fixture["safety_boundary"]["forbidden_actions"])

    def test_commit_package_lock_digests_match_assets(self) -> None:
        package_root = ROOT / "sites" / "xiaohongshu" / "publish-note-image-text-commit"
        package_lock = load(package_root / "package-lock.json")
        for asset in package_lock["locked_assets"]:
            with self.subTest(path=asset["path"]):
                actual = hashlib.sha256((package_root / asset["path"]).read_bytes()).hexdigest()
                self.assertEqual(asset["sha256"], actual)

    def test_fail_closed_mutations(self) -> None:
        mutations: dict[str, Callable[[dict[str, Any]], None]] = {
            "missing_declaration": lambda value: value.pop("action_declaration"),
            "missing_action_id": lambda value: value["action_declaration"]["actions"][0].pop("action_id"),
            "action_namespace_drift": lambda value: value["action_declaration"]["actions"][0].__setitem__("action_id", "other_operation"),
            "environment_category": lambda value: value["action_declaration"]["actions"][0].__setitem__("category", "environment"),
            "unknown_field": lambda value: value["action_declaration"].__setitem__("policy", "auto"),
            "prepare_upload": lambda value: value["action_declaration"]["actions"][0].__setitem__("external_effects", ["upload"]),
            "commit_without_effect": lambda value: value["action_declaration"]["actions"][0].__setitem__("category", "commit"),
            "origin_widening": lambda value: value["action_declaration"]["actions"][0]["target_scope"].__setitem__("supported_origins", ["https://example.com"]),
            "target_drift": lambda value: value["action_declaration"]["actions"][0]["target_scope"].__setitem__("target_types", ["other_page"]),
            "resource_drift": lambda value: value["action_declaration"]["actions"][0]["resource_requirements"].__setitem__("id", "other.resources"),
            "unknown_profile": lambda value: value["action_declaration"]["actions"][0]["resource_requirements"].__setitem__("profile_ids", ["unknown-profile"]),
            "duplicate_action_id": lambda value: value["action_declaration"]["actions"].append({**copy.deepcopy(value["action_declaration"]["actions"][0]), "category": "read"}),
        }
        base = self.manifest("publish-note-precheck")
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                candidate = copy.deepcopy(base)
                mutate(candidate)
                self.assertTrue(self.errors("publish-note-precheck", candidate))


if __name__ == "__main__":
    unittest.main()
