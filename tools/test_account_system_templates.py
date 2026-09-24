#!/usr/bin/env python3
"""Checks the static, public AccountSystem templates owned by Lode."""

from __future__ import annotations

import copy
import hashlib
import json
import unittest
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/account-system-template-v1.schema.json"
TEMPLATE_ROOT = ROOT / "account-systems"
INDEX_PATH = ROOT / "registry/account-system-templates.json"
INDEX_SCHEMA_PATH = ROOT / "schemas/account-system-template-index-v1.schema.json"


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected a JSON object: {path}")
    return value


class AccountSystemTemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_PATH)
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())
        cls.templates = sorted(TEMPLATE_ROOT.glob("*/*.json"))

    def test_fixed_templates_match_schema_and_versioned_identity(self) -> None:
        self.assertTrue(self.templates, "expected at least one fixed AccountSystem template")
        for path in self.templates:
            with self.subTest(path=path.relative_to(ROOT)):
                template = load_json(path)
                self.assertEqual([], list(self.validator.iter_errors(template)))
                self.assertEqual(
                    f"lode://account-system/{template['account_system_id']}@{template['version']}",
                    template["template_ref"],
                )
                self.assertEqual(template["version"], template["source"]["version"])
                allowed_hosts = set(template["related_domains"])
                for entry in [template["login_entry"], *template["admin_entry_points"]]:
                    with self.subTest(entry=entry):
                        parsed = urlparse(entry["url"])
                        self.assertEqual("https", parsed.scheme)
                        self.assertIn(parsed.hostname, allowed_hosts)

    def test_template_index_resolves_unique_refs_and_pins_source_bytes(self) -> None:
        index = load_json(INDEX_PATH)
        index_schema = load_json(INDEX_SCHEMA_PATH)
        Draft202012Validator.check_schema(index_schema)
        index_validator = Draft202012Validator(index_schema, format_checker=FormatChecker())
        self.assertEqual([], list(index_validator.iter_errors(index)))
        self.assertEqual("lode.account-system-template-index.v1", index.get("schema_version"))
        self.assertEqual("lode.account-system-templates", index.get("index_id"))
        entries = index.get("entries")
        self.assertIsInstance(entries, list)
        self.assertEqual(len(entries), len(self.templates))
        seen_refs: set[str] = set()
        seen_paths: set[str] = set()
        for entry in entries:
            self.assertIsInstance(entry, dict)
            template_ref = entry.get("template_ref")
            relative_path = entry.get("path")
            self.assertIsInstance(template_ref, str)
            self.assertIsInstance(relative_path, str)
            self.assertNotIn(template_ref, seen_refs)
            self.assertNotIn(relative_path, seen_paths)
            seen_refs.add(template_ref)
            seen_paths.add(relative_path)
            path = ROOT / relative_path
            self.assertFalse(Path(relative_path).is_absolute())
            path.resolve().relative_to(ROOT)
            template = load_json(path)
            self.assertEqual(template_ref, template.get("template_ref"))
            self.assertEqual(entry.get("version"), template.get("version"))
            self.assertEqual("sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(), entry.get("sha256"))
        self.assertEqual({path.relative_to(ROOT).as_posix() for path in self.templates}, seen_paths)

    def test_template_rejects_private_or_unreviewed_extension_fields(self) -> None:
        template = load_json(TEMPLATE_ROOT / "github/1.0.0.json")
        for key, value in [
            ("cookie", "never-stored"),
            ("profile_id", "private-profile"),
            ("identity_selector", "#account-menu"),
            ("runtime_handle", "opaque-ref"),
        ]:
            with self.subTest(key=key):
                candidate = copy.deepcopy(template)
                candidate[key] = value
                self.assertTrue(list(self.validator.iter_errors(candidate)))

    def test_identity_guidance_is_optional_and_descriptive(self) -> None:
        template = load_json(TEMPLATE_ROOT / "github/1.0.0.json")
        self.assertNotIn("identity_method", template)

        candidate = copy.deepcopy(template)
        candidate["identity_method"] = {
            "method_ref": "owner-confirmed-profile",
            "description": "Owner confirms a public profile identity before use.",
            "evidence_refs": ["https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github"],
        }
        self.assertEqual([], list(self.validator.iter_errors(candidate)))

        candidate["identity_method"]["selector"] = "#user-profile"
        self.assertTrue(list(self.validator.iter_errors(candidate)))


if __name__ == "__main__":
    unittest.main()
