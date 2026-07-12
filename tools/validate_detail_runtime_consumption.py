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
REJECTIONS = ["caller_constructed", "raw_url", "cross_site", "cross_identity", "cross_run", "expired", "already_consumed", "asset_digest_drift", "missing_evidence", "post_check_failed"]


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
        if entry["required_ref_kinds"] != current.get("evidence_requirements", {}).get("required_ref_kinds"):
            errors.append(f"{operation}: evidence requirements drift")
    if load(FIXTURE).get("rejection_cases") != REJECTIONS:
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
