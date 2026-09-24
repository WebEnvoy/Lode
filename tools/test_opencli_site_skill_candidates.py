"""Checks proposed OpenCLI site-skill package candidates and their fixed-source reports."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools import generate_opencli_site_skill_candidates as generator
from tools.lode_validate_package import validate_package
from tools import opencli_readonly_candidates as inspector


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = json.loads((ROOT / "registry/local-packages.json").read_text(encoding="utf-8"))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


class StaticRegistrationTests(unittest.TestCase):
    def test_fixed_positive_registrations_are_explicit_public_non_browser_reads(self) -> None:
        config = read_json(ROOT / "tools/opencli_readonly_candidates.json")
        for sample in config["samples"]:
            with self.subTest(sample=sample["id"]):
                source = (ROOT / sample["entrypoint"]).read_text(encoding="utf-8")
                declaration = inspector.extract_cli_declaration(source)
                self.assertIs(declaration["browser"], False)
                self.assertEqual(declaration["access"], "read")
                self.assertEqual(declaration["strategy"], "Strategy.PUBLIC")

    def test_unknown_or_dynamic_safety_relevant_registration_values_fail_closed(self) -> None:
        source_path = ROOT / "third_party/opencli-1.8.8/clis/devto/latest.js"
        source = source_path.read_text(encoding="utf-8")
        mutations = [
            ("browser: false", "browser: isBrowserDisabled()"),
            ("access: 'read'", "access: accessMode"),
            ("strategy: Strategy.PUBLIC", "strategy: selectedStrategy()"),
            ("domain: 'dev.to'", "domain: allowedDomain"),
            ("name: 'latest'", "name: adapterName"),
            ("browser: false", "unknown_mode: false"),
        ]
        for before, after in mutations:
            with self.subTest(expression=after):
                self.assertIn(before, source)
                with self.assertRaises(inspector.CandidateError):
                    inspector.extract_cli_declaration(source.replace(before, after, 1))


class ProposedPackageTests(unittest.TestCase):
    def test_candidate_generator_matches_committed_candidate_bytes(self) -> None:
        manifests = [
            read_json(ROOT / "sites" / sample["site"] / sample["name"] / "manifest.json")
            for sample in generator.SAMPLES
        ]
        source_commits = {manifest["source"]["commit"] for manifest in manifests}
        self.assertEqual(len(source_commits), 1)
        self.assertEqual(generator.run(next(iter(source_commits)), check=True), 0)

    def test_lode_source_pins_resolve_to_commits_containing_candidate_packages(self) -> None:
        for sample in generator.SAMPLES:
            package_path = f"sites/{sample['site']}/{sample['name']}"
            manifest = read_json(ROOT / package_path / "manifest.json")
            commit = manifest["source"]["commit"]
            for relative in ("manifest.json", "package-lock.json", "capabilities/public-read.json", "scripts/opencli-adapter.mjs", f"tasks/{sample['task']}.json"):
                result = subprocess.run(
                    ["git", "cat-file", "-e", f"{commit}:{package_path}/{relative}"],
                    cwd=ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, f"source pin {commit} lacks {package_path}/{relative}")

    def test_candidates_are_located_in_existing_registry_and_use_exact_candidate_contract(self) -> None:
        registry_entries = REGISTRY["entries"]
        config = read_json(ROOT / "tools/opencli_readonly_candidates.json")
        report = read_json(ROOT / "docs/verification/opencli-v1.8.8-readonly-candidates.json")
        by_id = {sample["id"]: sample for sample in report["positive_candidates"]}
        self.assertFalse(report["inspection_constraints"]["marker_scan_is_general_security_proof"])
        for sample in generator.SAMPLES:
            package_root = ROOT / "sites" / sample["site"] / sample["name"]
            manifest = read_json(package_root / "manifest.json")
            task_path = package_root / "tasks" / f"{sample['task']}.json"
            task = read_json(task_path)
            capability = read_json(package_root / "capabilities/public-read.json")
            input_schema = read_json(package_root / "schemas/input.schema.json")
            output_schema = read_json(package_root / "schemas/output.schema.json")
            script = (package_root / "scripts/opencli-adapter.mjs").read_text(encoding="utf-8")
            candidate = by_id[sample["candidate_id"]]

            with self.subTest(candidate=sample["candidate_id"]):
                matches = [entry for entry in registry_entries if entry.get("package_ref") == manifest["package_ref"]]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0], {
                    "package_ref": manifest["package_ref"],
                    "package_type": "site-skill",
                    "package_path": f"sites/{sample['site']}/{sample['name']}",
                    "manifest_path": f"sites/{sample['site']}/{sample['name']}/manifest.json",
                    "revision_ref": manifest["revision_ref"],
                    "package_digest": manifest["integrity"]["package_digest"],
                    "task_refs": [sample["task"]],
                })
                self.assertEqual(manifest["lifecycle"], "proposed")
                self.assertEqual(manifest["validation"], {"runtime_execution": "not_claimed", "live_evidence": "not_claimed"})
                self.assertEqual(manifest["version"], "0.1.0")
                self.assertEqual(manifest["revision_ref"], f"{manifest['package_ref']}@0.1.0#{manifest['source']['commit']}")
                self.assertEqual(manifest["source"]["commit"], manifest["scripts"][0]["source_commit"])
                self.assertEqual(manifest["scripts"][0]["broker"], "webenvoy.site-skill-broker/v1.1")
                self.assertEqual(manifest["scripts"][0]["broker_capabilities"], ["network.read", "output.write"])
                self.assertEqual(manifest["scripts"][0]["data_handling"]["external_egress"], "declared")
                self.assertEqual(task["operation_id"], "network.public_read")
                self.assertNotIn("candidate_status", task)
                self.assertEqual(task["applicability"]["target_type"], "public_http_origin")
                self.assertEqual(task["applicability"]["origins"], [sample["origin"]])
                self.assertEqual(task["inputs"]["carrier"], "webenvoy.managed-task-inline/v1")
                self.assertLessEqual(task["inputs"]["max_bytes"], 65536)
                self.assertEqual(task["network_read"]["transport"], "program_anonymous_https")
                self.assertEqual(task["network_read"]["origin"], sample["origin"])
                self.assertEqual(task["network_read"]["pathname"], sample["path"])
                self.assertEqual(task["network_read"]["query_keys"], sample["query_keys"])
                self.assertEqual(task["network_read"]["headers"], generator.policy(sample)["headers"])
                if sample["user_agent_source"] == "node_fetch_default":
                    self.assertIsNone(sample["user_agent"], "the pinned OpenCLI call must remain free of an explicit User-Agent")
                    self.assertEqual(task["network_read"]["headers"]["user-agent"], "node")
                    self.assertEqual(candidate["request_candidate"]["effective_user_agent"], "node")
                    self.assertIn("Node 24 built-in fetch default", candidate["request_candidate"]["effective_user_agent_basis"])
                self.assertEqual(task["network_read"]["max_redirects"], 2)
                self.assertEqual(task["network_read"]["max_response_bytes"], sample["max_response_bytes"])
                self.assertEqual(task["network_read"]["timeout_ms"], sample["timeout_ms"])
                self.assertEqual(task["entrypoint"]["broker"], "webenvoy.site-skill-broker/v1.1")
                self.assertEqual(task["entrypoint"]["capability_refs"], [capability["capability_ref"]])
                self.assertEqual(capability["operation_id"], "network.public_read")
                self.assertEqual(capability["action"], "read")
                self.assertNotIn("target", task)
                self.assertIn("omit `target`", (package_root / "SKILL.md").read_text(encoding="utf-8"))
                self.assertEqual(candidate["source_reuse"]["original_parser_and_mapping_source_changed"], False)
                self.assertEqual(candidate["source_reuse"]["business_logic_reimplemented"], False)
                self.assertIn("external_import_top_level_effects", candidate["module_effects_review"])
                self.assertIn("unknown", candidate["module_effects_review"]["external_import_top_level_effects"])

                Draft202012Validator.check_schema(input_schema)
                Draft202012Validator.check_schema(output_schema)
                self.assertEqual(input_schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertEqual(output_schema["properties"]["source_refs"]["items"]["properties"]["source_kind"]["const"], "public_http_response")
                self.assertEqual(output_schema["properties"]["evidence_refs"]["items"]["properties"]["evidence_kind"]["const"], "public_http_response")
                self.assertEqual(output_schema["properties"]["source_refs"]["minItems"], 1)
                self.assertEqual(output_schema["properties"]["source_refs"]["maxItems"], 1)
                self.assertEqual(output_schema["properties"]["evidence_refs"]["minItems"], 1)
                self.assertEqual(output_schema["properties"]["evidence_refs"]["maxItems"], 1)
                normalized = output_schema["properties"]["normalized"]["properties"]
                self.assertNotIn("minItems", normalized["records"], "the fixed output schema must allow a verified empty record set")
                generated_post_check = json.loads(generator.package_files(sample, manifest["source"]["commit"], generator.source_record())["checks/post-check.json"])
                expected_fields = generated_post_check["requirements"][0]["expected_normalized_fields"]
                self.assertTrue(expected_fields, "post-check must retain a positive completeness condition")
                self.assertTrue(
                    set(expected_fields).issubset(normalized),
                    "post-check expected fields must use direct keys supported by Core lookup; nested consistency belongs in output schema",
                )
                self.assertFalse(any("." in field for field in expected_fields), "post-check field lookup does not resolve dotted paths")
                example_output = {
                    "result_kind": task["outputs"]["result_kind"],
                    "status": "available",
                    "normalized": {
                        "parameters": {}, "records": [], "completeness": "complete",
                        "pagination": {"mode": {"github": "top_n", "devto": "requested_page", "arxiv": "max_results"}[sample["site"]], "has_more": None, "completeness": "complete"},
                    },
                    "source_refs": [{"ref_id": "opaque:response", "source_kind": "public_http_response"}],
                    "evidence_refs": [{"ref_id": "opaque:response", "evidence_kind": "public_http_response", "producer": "core", "redaction": "summary_only"}],
                }
                Draft202012Validator(output_schema).validate(example_output)
                self.assertIn("export async function run(input, broker, context)", script)
                self.assertNotRegex(script, r"(?m)^\s*import\s")
                self.assertNotRegex(script, r"\b(?:require|child_process)\b|\bprocess\.env\b|\b(?:eval|Function)\s*\(|\bimport\s*\(")
                self.assertEqual(len(re.findall(r"__opencliBroker\.network\.read\(", script)), 1)

                integrity = manifest["integrity"]["files"]
                integrity_by_path = {item["path"]: item for item in integrity}
                for relative_path, item in integrity_by_path.items():
                    data = (package_root / relative_path).read_bytes()
                    self.assertEqual(item["bytes"], len(data), relative_path)
                    self.assertEqual(item["sha256"], sha256(data), relative_path)
                source_pin = manifest["integrity"]["package_digest"]
                digest_manifest = json.loads(json.dumps(manifest))
                del digest_manifest["integrity"]["package_digest"]
                digest_input = b"lode.site-skill-package/v1\n" + canonical(digest_manifest) + b"\n" + "".join(
                    f"{item['path']}\t{item['bytes']}\t{item['sha256']}\n" for item in integrity
                ).encode("utf-8")
                self.assertEqual(source_pin, sha256(digest_input))

                validation = validate_package(package_root, ROOT / "registry/local-packages.json")
                self.assertEqual(validation.errors, [], validation.to_dict())
                self.assertEqual([warning["code"] for warning in validation.warnings], ["candidate_contract_pending"])

    def test_report_fixes_three_positive_and_three_offline_negative_samples(self) -> None:
        config = read_json(ROOT / "tools/opencli_readonly_candidates.json")
        report = read_json(ROOT / "docs/verification/opencli-v1.8.8-readonly-candidates.json")
        self.assertEqual([sample["id"] for sample in report["positive_candidates"]], [sample["id"] for sample in config["samples"]])
        self.assertEqual({sample["request_candidate"]["origin"] for sample in report["positive_candidates"]}, {"https://github.com", "https://dev.to", "https://export.arxiv.org"})
        self.assertEqual([sample["id"] for sample in report["negative_samples"]], [sample["id"] for sample in config["negative_samples"]])
        self.assertTrue(all(sample["executed"] is False for sample in report["negative_samples"]))
        self.assertFalse(report["reuse_assessment"]["declaration_fixture_only_reuse_goal_met"])
        self.assertTrue(report["reuse_assessment"]["third_sample_requires_generator_logic"])
        self.assertEqual(report["reuse_assessment"]["time_or_cost_measurement"], "not recorded")

    def test_official_validator_rejects_public_read_scope_and_broker_mutations(self) -> None:
        sample = generator.SAMPLES[0]
        source = ROOT / "sites" / sample["site"] / sample["name"]
        cases = [
            ("task", lambda value: value["network_read"].update(origin="https://attacker.example"), "tasks#network_read"),
            ("task", lambda value: value["network_read"].update(query_keys=["api_key"]), "tasks#network_read"),
            ("task", lambda value: value["data_handling"].update(external_egress="none"), "tasks"),
            ("manifest", lambda value: value["scripts"][0].update(broker_capabilities=["network.read", "output.write", "owner.secret"]), "manifest.json#scripts"),
            ("output", lambda value: value["properties"]["normalized"]["properties"]["records"].update(minItems=1), "normalized.records"),
        ]
        for kind, mutate, error_path in cases:
            with self.subTest(kind=kind, error_path=error_path), tempfile.TemporaryDirectory() as temporary:
                candidate = Path(temporary) / "candidate"
                shutil.copytree(source, candidate)
                if kind == "task":
                    path = candidate / "tasks" / f"{sample['task']}.json"
                elif kind == "manifest":
                    path = candidate / "manifest.json"
                else:
                    path = candidate / "schemas/output.schema.json"
                value = json.loads(path.read_text(encoding="utf-8"))
                mutate(value)
                path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                report = validate_package(candidate, ROOT / "registry/local-packages.json")
                self.assertTrue(any(error_path in error["path"] for error in report.errors), report.to_dict())


if __name__ == "__main__":
    unittest.main()
