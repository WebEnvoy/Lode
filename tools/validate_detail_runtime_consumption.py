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
REJECTIONS = ["caller_constructed", "raw_url", "cross_site", "cross_identity", "cross_run", "expired", "already_consumed", "asset_digest_drift", "missing_output_schema", "missing_public_field", "empty_summary", "synthetic_summary", "missing_field_binding", "sensitive_material_exposed", "missing_evidence", "post_check_failed"]
EXPECTED_PUBLIC_FIELDS = {
    "xhs_read_note_detail": ["canonical_url", "title", "summary", "source_status", "note_id", "author", "body_summary", "interaction_metrics", "source_citation"],
    "boss_read_job_detail": ["canonical_url", "title", "summary", "source_status", "job", "company", "recruiter", "source_citation"],
}
FORBIDDEN_INLINE = {"raw_dom", "network_response_body", "xsec_token", "cookie", "token", "profile", "raw_profile"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


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
        if not set(expected_fields).issubset(schema_fields):
            errors.append(f"{operation}: pinned output schema omits required public fields")
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
        ("empty_summary", lambda x: x["entries"][0]["output_contract"]["bounded_summary"].__setitem__("min_length", 0)),
        ("synthetic_summary", lambda x: x["entries"][0]["output_contract"]["bounded_summary"].__setitem__("reject_synthetic_placeholder", False)),
        ("missing_field_binding", lambda x: x["entries"][0]["output_contract"]["field_binding"].__setitem__("required_bindings", ["source_ref"])),
        ("sensitive_material_exposed", lambda x: x["result_requirements"].__setitem__("forbidden_inline_material", [])),
        ("missing_evidence", lambda x: x["entries"][0].__setitem__("required_ref_kinds", [])),
        ("post_check_failed", lambda x: x["result_requirements"].__setitem__("success_requires_post_check", "failed")),
    ]
    failures: list[str] = []
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        if not validate(candidate):
            failures.append(f"self-test did not reject {name}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    data = load(TRUTH)
    errors = validate(data)
    if args.self_test and not errors:
        errors.extend(self_test(data))
    print(json.dumps({"status": "failed" if errors else "passed", "operations": sorted(OPERATIONS), "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
