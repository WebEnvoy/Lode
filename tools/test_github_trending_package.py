#!/usr/bin/env python3
"""Offline package and synthetic behavior checks for the fixed OpenCLI conversion."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from tools.lode_validate_package import validate_package
from tools.lode_validate_package import GITHUB_TRENDING_SITE_SKILL_MANIFEST_SHA256
from tools.lode_validate_package import GITHUB_TRENDING_SITE_SKILL_PACKAGE_DIGEST
from tools.lode_validate_package import GITHUB_TRENDING_SITE_SKILL_SCRIPT_SHA256


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "sites/github/trending"
SOURCE_COMMIT = "0dcd6232cdfd9c88982792d2ce88a39d528a6433"
OPENCLI_COMMIT = "8271afc67e8504bda94c147f446ee29775d08274"
CAPABILITY_REF = "lode://site-capability/github/managed-page-snapshot@1.0.0"
SCRIPT_REF = "lode://script/site-skill/github/trending/read-daily-top5@1.0.0"
LICENSE_SHA256 = "0210b8b66cf00358242cb921ba2be3a46dfe0190159b1b952388a3880ce1ff54"


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected JSON object: {path}")
    return value


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def source_comparison_bytes(relative_path: str, data: bytes) -> bytes:
    generated_fields = {
        "capabilities/managed-page-snapshot.json": {"source_ref"},
        "package-lock.json": {"source_ref", "revision_ref"},
    }.get(relative_path)
    if generated_fields is None:
        return data
    value = json.loads(data)
    for field in generated_fields:
        value[field] = "<generated-source-pin>"
    return canonical_bytes(value)


def source_repository_for_commit(commit: str) -> Path | None:
    candidates = [ROOT, ROOT / ".provenance/controlled-local-source"]
    for repository in candidates:
        if not repository.exists():
            continue
        git_prefix = ["git", "-C", str(repository)]
        object_exists = subprocess.run(
            [*git_prefix, "cat-file", "-e", f"{commit}^{{commit}}"], capture_output=True, check=False
        )
        if object_exists.returncode != 0:
            continue
        reachable_refs = subprocess.run(
            [*git_prefix, "for-each-ref", f"--contains={commit}", "--format=%(refname)"], capture_output=True, text=True, check=False
        )
        reachable_from_head = subprocess.run(
            [*git_prefix, "merge-base", "--is-ancestor", commit, "HEAD"], capture_output=True, check=False
        )
        if reachable_refs.returncode == 0 and (reachable_refs.stdout.strip() or reachable_from_head.returncode == 0):
            return repository
    return None


class GitHubTrendingPackageTests(unittest.TestCase):
    def test_registered_package_passes_the_official_validator(self) -> None:
        report = validate_package(PACKAGE, ROOT / "registry/local-packages.json")
        self.assertEqual([], report.errors)

    def test_fixed_package_integrity_source_lock_and_script_refs(self) -> None:
        manifest = load_json(PACKAGE / "manifest.json")
        raw_manifest_sha256 = hashlib.sha256((PACKAGE / "manifest.json").read_bytes()).hexdigest()
        self.assertEqual(GITHUB_TRENDING_SITE_SKILL_MANIFEST_SHA256, raw_manifest_sha256)
        self.assertEqual("lode://site-skill/github/trending", manifest["package_ref"])
        self.assertEqual(SOURCE_COMMIT, manifest["source"]["commit"])
        self.assertEqual("WebEnvoy/Lode", manifest["source"]["repository"])
        self.assertEqual("sites/github/trending", manifest["source"]["package_path"])
        self.assertIn(OPENCLI_COMMIT, (PACKAGE / "references/opencli-source-mapping.md").read_text(encoding="utf-8"))

        records = manifest["integrity"]["files"]
        self.assertEqual(sorted(record["path"] for record in records), [record["path"] for record in records])
        self.assertEqual(len({record["path"] for record in records}), len(records))
        declared = {record["path"] for record in records}
        actual = {
            path.relative_to(PACKAGE).as_posix()
            for path in PACKAGE.rglob("*")
            if path.is_file()
        }
        self.assertEqual(actual - {"manifest.json"}, declared)
        self.assertFalse(any(path.is_symlink() for path in PACKAGE.rglob("*")))

        tuples: list[str] = []
        for record in records:
            data = (PACKAGE / record["path"]).read_bytes()
            sha = "sha256:" + hashlib.sha256(data).hexdigest()
            self.assertEqual(record["bytes"], len(data), record["path"])
            self.assertEqual(record["sha256"], sha, record["path"])
            tuples.append(f"{record['path']}\t{len(data)}\t{sha}\n")
        canonical_manifest = json.loads(json.dumps(manifest))
        canonical_manifest["integrity"].pop("package_digest")
        digest_input = (
            b"lode.site-skill-package/v1\n"
            + canonical_bytes(canonical_manifest)
            + b"\n"
            + "".join(tuples).encode("utf-8")
        )
        package_digest = "sha256:" + hashlib.sha256(digest_input).hexdigest()
        self.assertEqual(manifest["integrity"]["package_digest"], package_digest)
        self.assertEqual(GITHUB_TRENDING_SITE_SKILL_PACKAGE_DIGEST, package_digest)

        source_ref = manifest["source"]["source_ref"]
        task = load_json(PACKAGE / "tasks/read-daily-trending-top5.json")
        capability = load_json(PACKAGE / "capabilities/managed-page-snapshot.json")
        lock = load_json(PACKAGE / "package-lock.json")
        script = manifest["scripts"][0]
        self.assertEqual(source_ref, capability["source_ref"])
        self.assertEqual(source_ref, lock["source_ref"])
        self.assertEqual(CAPABILITY_REF, capability["capability_ref"])
        self.assertEqual(CAPABILITY_REF, lock["capability_ref"])
        self.assertEqual([CAPABILITY_REF], task["entrypoint"]["capability_refs"])
        self.assertEqual(SCRIPT_REF, script["script_ref"])
        script_bytes = (PACKAGE / script["path"]).read_bytes()
        script_sha256 = "sha256:" + hashlib.sha256(script_bytes).hexdigest()
        self.assertEqual(script_sha256, script["sha256"])
        self.assertEqual(GITHUB_TRENDING_SITE_SKILL_SCRIPT_SHA256, script_sha256)
        self.assertEqual(script["version"], task["entrypoint"]["script_version"])
        self.assertEqual(script["sha256"], task["entrypoint"]["script_sha256"])
        self.assertEqual(script["runtime_kind"], task["entrypoint"]["runtime_kind"])
        self.assertEqual(script["broker"], task["entrypoint"]["broker"])
        self.assertEqual(SOURCE_COMMIT, script["source_commit"])
        self.assertEqual(LICENSE_SHA256, hashlib.sha256((PACKAGE / "references/OpenCLI-Apache-2.0-LICENSE.txt").read_bytes()).hexdigest())
        source_text = script_bytes.decode("utf-8")
        self.assertIn("export async function run(input, broker, context)", source_text)
        for forbidden in ["\nimport ", "\nexport default", "fetch(", "eval(", "require(", "child_process", "document."]:
            self.assertNotIn(forbidden, source_text)

    def test_fixed_task_and_output_schema_are_consistent(self) -> None:
        manifest = load_json(PACKAGE / "manifest.json")
        task = load_json(PACKAGE / "tasks/read-daily-trending-top5.json")
        input_schema = load_json(PACKAGE / "schemas/input.schema.json")
        output_schema = load_json(PACKAGE / "schemas/output.schema.json")
        task_locators = {item["task_ref"]: item["path"] for item in manifest["tasks"]}
        self.assertEqual(task_locators[task["task_ref"]], "tasks/read-daily-trending-top5.json")
        self.assertEqual(task["inputs"]["schema_ref"], input_schema["$id"])
        self.assertEqual(task["outputs"]["schema_ref"], output_schema["$id"])
        self.assertEqual("instance.snapshot", task["operation_id"])
        self.assertEqual("read", task["action"])
        self.assertEqual("none", task["inputs"]["carrier"])
        self.assertEqual("query_original_run_only", task["failure_recovery"]["unknown_policy"])

        Draft202012Validator.check_schema(input_schema)
        Draft202012Validator.check_schema(output_schema)
        input_validator = Draft202012Validator(input_schema, format_checker=FormatChecker())
        output_validator = Draft202012Validator(output_schema, format_checker=FormatChecker())
        self.assertEqual([], list(input_validator.iter_errors({})))
        self.assertTrue(list(input_validator.iter_errors({"url": "https://github.com/trending"})))

        available = {
            "result_kind": "github_trending_daily_top5",
            "status": "available",
            "normalized": {
                "period": "daily",
                "requested_count": 5,
                "rows": [
                    {"name": f"owner{i}/repo{i}", "url": f"https://github.com/owner{i}/repo{i}", "language": "TypeScript", "language_state": "observed", "today_stars": i, "today_stars_state": "observed"}
                    for i in range(1, 6)
                ],
                "completeness": "complete",
                "snapshot_coverage": "complete",
            },
            "source_refs": [{"ref_id": "page:1", "source_kind": "harbor_page"}],
            "evidence_refs": [{"ref_id": "observation:1", "evidence_kind": "snapshot_ref", "producer": "harbor", "redaction": "summary_only"}],
        }
        self.assertEqual([], list(output_validator.iter_errors(available)))
        partial = json.loads(json.dumps(available))
        partial["status"] = "partial"
        partial["normalized"]["rows"][0]["language"] = None
        partial["normalized"]["rows"][0]["language_state"] = "unknown"
        partial["normalized"]["completeness"] = "partial"
        self.assertEqual([], list(output_validator.iter_errors(partial)))
        incomplete_available = json.loads(json.dumps(partial))
        incomplete_available["status"] = "available"
        self.assertTrue(list(output_validator.iter_errors(incomplete_available)))

    def test_synthetic_script_cases(self) -> None:
        result = subprocess.run(
            ["node", "--test", str(ROOT / "tools/tests/test_github_trending_top5.mjs")],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_registry_cannot_repoint_fixed_revision_or_digest(self) -> None:
        index_path = ROOT / "registry/local-packages.json"
        index = load_json(index_path)
        entries = index.get("entries")
        self.assertIsInstance(entries, list)
        candidate = next(item for item in entries if isinstance(item, dict) and item.get("package_ref") == "lode://site-skill/github/trending")
        candidate["package_digest"] = "sha256:" + "0" * 64
        with tempfile.TemporaryDirectory(prefix="lode-github-trending-index-") as directory:
            temporary_index = Path(directory) / "local-packages.json"
            temporary_index.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
            report = validate_package(PACKAGE, temporary_index)
        self.assertTrue(report.errors)

    def test_all_registered_site_skill_sources_exist_and_match_their_assets(self) -> None:
        index = load_json(ROOT / "registry/local-packages.json")
        entries = index.get("entries")
        self.assertIsInstance(entries, list)
        site_skill_entries = [entry for entry in entries if isinstance(entry, dict) and entry.get("package_type") == "site-skill"]
        self.assertTrue(site_skill_entries)

        for entry in site_skill_entries:
            package_root = ROOT / entry["package_path"]
            manifest = load_json(package_root / "manifest.json")
            source = manifest.get("source")
            self.assertIsInstance(source, dict)
            commit = source.get("commit")
            package_path = source.get("package_path")
            self.assertIsInstance(commit, str)
            self.assertEqual(40, len(commit))
            self.assertEqual(str(package_root.relative_to(ROOT)), package_path)

            source_repository = source_repository_for_commit(commit)
            self.assertIsNotNone(source_repository, f"source commit is missing or unreachable: {commit}")
            assert source_repository is not None
            git_prefix = ["git", "-C", str(source_repository)]
            source_tree = subprocess.run(
                [*git_prefix, "cat-file", "-e", f"{commit}:{package_path}"], capture_output=True, text=True, check=False
            )
            self.assertEqual(0, source_tree.returncode, f"source package path is absent at {commit}: {package_path}")

            for record in manifest["integrity"]["files"]:
                relative_path = record["path"]
                source_object = f"{commit}:{package_path}/{relative_path}"
                source_file = subprocess.run(
                    [*git_prefix, "show", source_object], capture_output=True, check=False
                )
                self.assertEqual(0, source_file.returncode, f"source asset is absent: {source_object}")
                current_bytes = (package_root / relative_path).read_bytes()
                self.assertEqual(
                    source_comparison_bytes(relative_path, source_file.stdout),
                    source_comparison_bytes(relative_path, current_bytes),
                    f"source asset differs from its pinned commit: {source_object}",
                )


if __name__ == "__main__":
    unittest.main()
