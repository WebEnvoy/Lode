#!/usr/bin/env python3
"""Validate static dual-site detail-read runtime-consumption truth."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
TRUTH = ROOT / "registry/detail-runtime-consumption.json"
SCHEMA = ROOT / "registry/detail-runtime-consumption.schema.json"
FIXTURE = ROOT / "registry/detail-runtime-consumption.fixture.json"
OPERATIONS = {"xhs_read_note_detail", "boss_read_job_detail"}
EXPECTED_ADMISSION = {
    "xhs_read_note_detail": {"enabled": True, "status": "current", "recheck_condition": "not_applicable"},
    "boss_read_job_detail": {"enabled": False, "status": "deferred_experimental", "recheck_condition": "deferred_milestone_scope_restored_with_current_head_review_and_runtime_live_evidence"},
}
REJECTIONS = ["caller_constructed", "raw_url", "cross_site", "cross_identity", "cross_run", "expired", "already_consumed", "asset_digest_drift", "missing_output_schema", "missing_public_field", "public_security_identifier", "empty_summary", "synthetic_summary", "missing_field_binding", "sensitive_material_exposed", "missing_evidence", "post_check_failed"]
EXPECTED_PUBLIC_FIELDS = {
    "xhs_read_note_detail": ["canonical_url", "title", "summary", "source_status", "note_id", "author", "body_summary", "interaction_metrics", "source_citation"],
    "boss_read_job_detail": ["canonical_url", "title", "summary", "source_status", "detail_ref", "job", "company", "recruiter", "source_citation"],
}
FORBIDDEN_INLINE = {"raw_dom", "network_response_body", "xsec_token", "securityId", "encryptJobId", "cookie", "token", "profile", "raw_profile"}
OUTPUT_FIXTURES = {
    "xhs_read_note_detail": ROOT / "sites/xiaohongshu/read-note-detail/fixtures/read-note-detail.fixture.json",
    "boss_read_job_detail": ROOT / "sites/boss/read-job-detail/fixtures/read-job-detail.fixture.json",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def output_validator(schema: dict[str, Any]):
    import jsonschema

    return jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())


def output_instance(operation: str) -> dict[str, Any]:
    return load(OUTPUT_FIXTURES[operation])["normalized_fixture"]["data"]


def truth_schema_errors(data: dict[str, Any]) -> list[Any]:
    import jsonschema

    validator = jsonschema.Draft202012Validator(load(SCHEMA), format_checker=jsonschema.FormatChecker())
    return list(validator.iter_errors(data))


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        import jsonschema
        jsonschema.Draft202012Validator(load(SCHEMA), format_checker=jsonschema.FormatChecker()).validate(data)
    except Exception as exc:
        return [f"schema: {exc}"]
    public = data["public_input"]
    if public.get("required") != ["detail_ref"] or public.get("caller_may_construct") is not False:
        errors.append("public input must exclusively require a non-constructible detail_ref")
    rejects = {"unknown_ref", "wrong_kind", "cross_site", "cross_identity", "cross_run", "expired", "already_consumed", "caller_constructed"}
    if set(data["ref_binding"].get("reject", [])) != rejects:
        errors.append("ref rejection set drifted")
    if data["result_requirements"].get("success_requires_post_check") != "passed":
        errors.append("success must require a passed post-check")
    if set(data["result_requirements"].get("forbidden_inline_material", [])) != FORBIDDEN_INLINE:
        errors.append("forbidden inline material policy drifted")
    entries = data["entries"]
    if {entry["operation_id"] for entry in entries} != OPERATIONS:
        errors.append("both detail operations must appear exactly once")
    registry = {entry["operation_id"]: entry for entry in load(ROOT / "registry/local-packages.json")["entries"]}
    for entry in entries:
        operation = entry["operation_id"]
        current = registry.get(operation)
        if current is None:
            errors.append(f"{operation}: missing registry entry")
            continue
        for key in ("package_ref", "lock_ref", "version", "site_slug", "capability_id", "operation_id", "operation_mode", "lifecycle"):
            if entry[key] != current.get(key):
                errors.append(f"{operation}.{key}: registry drift")
        if entry.get("runtime_admission") != EXPECTED_ADMISSION[operation]:
            errors.append(f"{operation}.runtime_admission: site production admission policy drift")
        if current.get("runtime_admission") != EXPECTED_ADMISSION[operation]:
            errors.append(f"{operation}.registry.runtime_admission: site production admission policy drift")
        for role, (path, expected) in entry["assets"].items():
            actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            if actual != expected:
                errors.append(f"{operation}.assets.{role}: digest drift")
        output_asset = entry["assets"].get("output_schema")
        if not output_asset:
            errors.append(f"{operation}: output schema is not pinned")
            continue
        output_schema = load(ROOT / output_asset[0])
        schema_fields = output_schema.get("$defs", {}).get("content_detail", {}).get("required", [])
        contract = entry.get("output_contract", {})
        expected_fields = EXPECTED_PUBLIC_FIELDS[operation]
        if contract.get("required_public_fields") != expected_fields:
            errors.append(f"{operation}: required public fields drifted")
        if schema_fields != expected_fields:
            errors.append(f"{operation}: pinned output schema required fields contradict public output truth")
        instance_errors = list(output_validator(output_schema).iter_errors(output_instance(operation)))
        if instance_errors:
            errors.append(f"{operation}: valid normalized fixture fails pinned output schema: {instance_errors[0].message}")
        summary = contract.get("bounded_summary", {})
        if summary.get("min_length") != 1 or not isinstance(summary.get("max_length"), int) or summary["max_length"] > 2000:
            errors.append(f"{operation}: public summary is not bounded")
        if summary.get("reject_whitespace_only") is not True or summary.get("reject_synthetic_placeholder") is not True:
            errors.append(f"{operation}: empty or synthetic summaries are not rejected")
        binding = contract.get("field_binding", {})
        if binding.get("required_for_every_public_field") is not True or binding.get("required_bindings") != ["source_ref", "evidence_ref"]:
            errors.append(f"{operation}: every public field must bind source and evidence refs")
        policy = contract.get("identifier_policy", {})
        if operation == "xhs_read_note_detail" and policy.get("xsec_token") != "forbidden":
            errors.append("xhs_read_note_detail: xsec_token must be forbidden")
        if operation == "boss_read_job_detail" and (policy.get("securityId") != "core_internal_binding_only" or policy.get("public_security_binding") != "opaque_detail_ref"):
            errors.append("boss_read_job_detail: securityId must remain Core-internal behind an opaque ref")
        if entry["required_ref_kinds"] != current.get("evidence_requirements", {}).get("required_ref_kinds"):
            errors.append(f"{operation}: evidence requirements drift")
    fixture = load(FIXTURE)
    examples = fixture.get("valid_output_examples", {})
    for operation, expected_fields in EXPECTED_PUBLIC_FIELDS.items():
        example = examples.get(operation, {})
        if example.get("public_fields") != expected_fields:
            errors.append(f"fixture {operation}: public fields drifted")
        summary = example.get("summary")
        if not isinstance(summary, str) or not summary.strip() or len(summary) > 2000 or "placeholder" in summary.lower() or "synthetic" in summary.lower():
            errors.append(f"fixture {operation}: summary must be bounded and non-synthetic")
        if example.get("all_fields_source_and_evidence_bound") is not True:
            errors.append(f"fixture {operation}: field bindings are incomplete")
    if examples.get("boss_read_job_detail", {}).get("security_binding") != "opaque_detail_ref":
        errors.append("fixture boss_read_job_detail: security binding must be opaque")
    if fixture.get("rejection_cases") != REJECTIONS:
        errors.append("fixture rejection cases do not match self-tests")
    return errors


def self_test(data: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("caller_constructed", lambda x: x["public_input"].__setitem__("caller_may_construct", True)),
        ("raw_url", lambda x: x["public_input"].__setitem__("required", ["url"])),
        ("cross_site", lambda x: x["ref_binding"]["reject"].remove("cross_site")),
        ("cross_identity", lambda x: x["ref_binding"]["reject"].remove("cross_identity")),
        ("cross_run", lambda x: x["ref_binding"]["reject"].remove("cross_run")),
        ("expired", lambda x: x["ref_binding"]["reject"].remove("expired")),
        ("already_consumed", lambda x: x["ref_binding"]["reject"].remove("already_consumed")),
        ("asset_digest_drift", lambda x: x["entries"][0]["assets"]["manifest"].__setitem__(1, "0" * 64)),
        ("missing_output_schema", lambda x: x["entries"][0]["assets"].pop("output_schema")),
        ("missing_public_field", lambda x: x["entries"][0]["output_contract"]["required_public_fields"].remove("title")),
        ("public_security_identifier", lambda x: x["entries"][1]["output_contract"]["required_public_fields"].append("securityId")),
        ("empty_summary", lambda x: x["entries"][0]["output_contract"]["bounded_summary"].__setitem__("min_length", 0)),
        ("synthetic_summary", lambda x: x["entries"][0]["output_contract"]["bounded_summary"].__setitem__("reject_synthetic_placeholder", False)),
        ("missing_field_binding", lambda x: x["entries"][0]["output_contract"]["field_binding"].__setitem__("required_bindings", ["source_ref"])),
        ("sensitive_material_exposed", lambda x: x["result_requirements"].__setitem__("forbidden_inline_material", [])),
        ("missing_evidence", lambda x: x["entries"][0].__setitem__("required_ref_kinds", [])),
        ("XHS disabled", lambda x: x["entries"][0]["runtime_admission"].__setitem__("enabled", False)),
        ("XHS inverted to BOSS", lambda x: x["entries"][0].__setitem__("runtime_admission", copy.deepcopy(EXPECTED_ADMISSION["boss_read_job_detail"]))),
        ("BOSS enabled", lambda x: x["entries"][1]["runtime_admission"].__setitem__("enabled", True)),
        ("BOSS inverted to XHS", lambda x: x["entries"][1].__setitem__("runtime_admission", copy.deepcopy(EXPECTED_ADMISSION["xhs_read_note_detail"]))),
        ("BOSS current", lambda x: x["entries"][1]["runtime_admission"].__setitem__("status", "current")),
        ("post_check_failed", lambda x: x["result_requirements"].__setitem__("success_requires_post_check", "failed")),
    ]
    failures: list[str] = []
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        if name in {"XHS disabled", "XHS inverted to BOSS", "BOSS enabled", "BOSS inverted to XHS", "BOSS current"} and not truth_schema_errors(candidate):
            failures.append(f"published schema did not reject {name}")
        if not validate(candidate):
            failures.append(f"self-test did not reject {name}")
    failures.extend(output_instance_self_test(data))
    return failures


def output_probes() -> list[tuple[str, str, Callable[[dict[str, Any]], None]]]:
    probes: list[tuple[str, str, Callable[[dict[str, Any]], None]]] = [
        ("boss_read_job_detail", "nested_security_id", lambda x: x["normalized"]["job"].__setitem__("securityId", "raw-security")),
        ("boss_read_job_detail", "nested_encrypt_job_id", lambda x: x["normalized"]["company"].__setitem__("encryptJobId", "raw-job")),
        ("boss_read_job_detail", "nested_raw_material", lambda x: x["normalized"]["recruiter"].__setitem__("cookie", "raw-cookie")),
        ("boss_read_job_detail", "canonical_url_query_leak", lambda x: x["normalized"].__setitem__("canonical_url", "https://www.zhipin.com/job_detail/fixture-job-1.html?securityId=raw")),
        ("boss_read_job_detail", "citation_url_query_leak", lambda x: x["normalized"]["source_citation"].__setitem__("url", "https://www.zhipin.com/job_detail/fixture-job-1.html?encryptJobId=raw")),
        ("xhs_read_note_detail", "xsec_url_query_leak", lambda x: x["normalized"].__setitem__("canonical_url", "https://www.xiaohongshu.com/explore/66aa00000000000001000111?xsec_token=raw")),
        ("xhs_read_note_detail", "citation_xsec_url_query_leak", lambda x: x["normalized"]["source_citation"].__setitem__("url", "https://www.xiaohongshu.com/explore/66aa00000000001000111?xsec_token=raw")),
        ("xhs_read_note_detail", "nested_raw_material", lambda x: x["normalized"]["author"].__setitem__("token", "raw-token")),
    ]
    for operation in sorted(OPERATIONS):
        probes.extend([
            (operation, "whitespace_summary", lambda x: x["normalized"].__setitem__("summary", "   \t")),
            (operation, "oversize_summary", lambda x: x["normalized"].__setitem__("summary", "x" * 2001)),
            (operation, "empty_source_refs", lambda x: x.__setitem__("source_refs", [])),
            (operation, "empty_evidence_refs", lambda x: x.__setitem__("evidence_refs", [])),
        ])
    return probes


def output_instance_self_test(data: dict[str, Any]) -> list[str]:
    entries = {entry["operation_id"]: entry for entry in data["entries"]}
    failures: list[str] = []
    for operation, name, mutate in output_probes():
        schema = load(ROOT / entries[operation]["assets"]["output_schema"][0])
        candidate = copy.deepcopy(output_instance(operation))
        mutate(candidate)
        if output_validator(schema).is_valid(candidate):
            failures.append(f"output probe did not reject {operation}:{name}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    data = load(TRUTH)
    errors = validate(data)
    if args.self_test and not errors:
        errors.extend(self_test(data))
    print(json.dumps({"status": "failed" if errors else "passed", "operations": sorted(OPERATIONS), "valid_output_instances": len(OPERATIONS), "malicious_output_probes": len(output_probes()), "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
