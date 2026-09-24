#!/usr/bin/env python3
"""Focused checks for the controlled-local site-skill package contract."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.lode_validate_package import validate_package


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "sites/controlled-local/page-summary"


def rewrite_package_pins(package_root: Path) -> None:
    manifest_path = package_root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for record in manifest["integrity"]["files"]:
        data = (package_root / record["path"]).read_bytes()
        record["bytes"] = len(data)
        record["sha256"] = "sha256:" + hashlib.sha256(data).hexdigest()
    canonical = dict(manifest)
    integrity = dict(canonical["integrity"])
    integrity.pop("package_digest", None)
    canonical["integrity"] = integrity
    canonical_bytes = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    tuples = "".join(
        f"{record['path']}\t{record['bytes']}\t{record['sha256']}\n"
        for record in sorted(manifest["integrity"]["files"], key=lambda item: item["path"])
    ).encode("utf-8")
    manifest["integrity"]["package_digest"] = "sha256:" + hashlib.sha256(
        b"lode.site-skill-package/v1\n" + canonical_bytes + b"\n" + tuples
    ).hexdigest()
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ControlledSiteSkillPackageTests(unittest.TestCase):
    def test_pinned_package_is_valid(self) -> None:
        self.assertEqual([], validate_package(PACKAGE).errors)

    def test_wrong_action_and_unknown_replay_policy_are_rejected(self) -> None:
        for name, mutate in [
            ("wrong-action", lambda task: task.__setitem__("action", "prepare")),
            ("unknown-policy", lambda task: task["failure_recovery"].__setitem__("unknown_policy", "retry_new_key")),
        ]:
            with self.subTest(case=name), tempfile.TemporaryDirectory(prefix="lode-site-skill-") as directory:
                package_root = Path(directory) / "package"
                shutil.copytree(PACKAGE, package_root)
                task_path = package_root / "tasks/read-page-summary.json"
                task = json.loads(task_path.read_text(encoding="utf-8"))
                mutate(task)
                task_path.write_text(json.dumps(task, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                rewrite_package_pins(package_root)
                report = validate_package(package_root)
                self.assertTrue(report.errors)
                self.assertTrue(any(error["code"] == "invalid_contract" for error in report.errors))

    def test_non_object_required_assets_are_rejected(self) -> None:
        for relative in [
            "tasks/read-page-summary.json",
            "schemas/output.schema.json",
            "checks/post-check.json",
            "package-lock.json",
        ]:
            for invalid in ["[]", "null", "false", "1", '"text"']:
                with self.subTest(asset=relative, value=invalid), tempfile.TemporaryDirectory(prefix="lode-site-skill-") as directory:
                    package_root = Path(directory) / "package"
                    shutil.copytree(PACKAGE, package_root)
                    (package_root / relative).write_text(invalid + "\n", encoding="utf-8")
                    rewrite_package_pins(package_root)
                    report = validate_package(package_root)
                    self.assertTrue(report.errors)
                    self.assertTrue(any(error["code"] == "invalid_contract" for error in report.errors))

    def test_controlled_local_still_rejects_unreviewed_script_assets(self) -> None:
        with tempfile.TemporaryDirectory(prefix="lode-site-skill-script-") as directory:
            package_root = Path(directory) / "package"
            shutil.copytree(PACKAGE, package_root)
            scripts = package_root / "scripts"
            scripts.mkdir()
            (scripts / "unreviewed.mjs").write_text("export async function run() {}\n", encoding="utf-8")
            report = validate_package(package_root)
            self.assertTrue(report.errors)
            self.assertTrue(any(error["code"] == "invalid_contract" for error in report.errors))


if __name__ == "__main__":
    unittest.main()
