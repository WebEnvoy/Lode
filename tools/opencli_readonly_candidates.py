#!/usr/bin/env python3
"""Inspect pinned OpenCLI adapters as source text and emit review-only candidates."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "tools/opencli_readonly_candidates.json"
REPORT_JSON = ROOT / "docs/verification/opencli-v1.8.8-readonly-candidates.json"
REPORT_MARKDOWN = ROOT / "docs/verification/opencli-v1.8.8-readonly-candidates.md"


class CandidateError(ValueError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_utf8(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise CandidateError(f"cannot read UTF-8 source {path}: {error}") from error


def _find_balanced(source: str, start: int, opener: str, closer: str) -> int:
    if start >= len(source) or source[start] != opener:
        raise CandidateError(f"expected {opener!r} at source offset {start}")
    depth = 0
    quote: str | None = None
    escaped = False
    line_comment = False
    block_comment = False
    index = start
    while index < len(source):
        char = source[index]
        next_char = source[index + 1] if index + 1 < len(source) else ""
        if line_comment:
            if char == "\n":
                line_comment = False
        elif block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
                index += 1
        elif quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char == "/" and next_char == "/":
            line_comment = True
            index += 1
        elif char == "/" and next_char == "*":
            block_comment = True
            index += 1
        elif char in "'\"`":
            quote = char
        elif char == opener:
            depth += 1
        elif char == closer:
            depth -= 1
            if depth == 0:
                return index
        index += 1
    raise CandidateError(f"unterminated {opener}{closer} in source")


def _split_top_level(source: str, delimiter: str = ",") -> list[str]:
    parts: list[str] = []
    start = 0
    stack: list[str] = []
    pairs = {"[": "]", "{": "}", "(": ")"}
    quote: str | None = None
    escaped = False
    line_comment = False
    block_comment = False
    index = 0
    while index < len(source):
        char = source[index]
        next_char = source[index + 1] if index + 1 < len(source) else ""
        if line_comment:
            if char == "\n":
                line_comment = False
        elif block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
                index += 1
        elif quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char == "/" and next_char == "/":
            line_comment = True
            index += 1
        elif char == "/" and next_char == "*":
            block_comment = True
            index += 1
        elif char in "'\"`":
            quote = char
        elif char in pairs:
            stack.append(pairs[char])
        elif stack and char == stack[-1]:
            stack.pop()
        elif not stack and char == delimiter:
            parts.append(source[start:index].strip())
            start = index + 1
        index += 1
    tail = source[start:].strip()
    if tail:
        parts.append(tail)
    return parts


def _split_property(source: str) -> tuple[str, str] | None:
    stack: list[str] = []
    pairs = {"[": "]", "{": "}", "(": ")"}
    quote: str | None = None
    escaped = False
    for index, char in enumerate(source):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char in "'\"`":
            quote = char
        elif char in pairs:
            stack.append(pairs[char])
        elif stack and char == stack[-1]:
            stack.pop()
        elif char == ":" and not stack:
            return source[:index].strip(), source[index + 1 :].strip()
    return None


def _literal(value: str, *, allowed_expressions: frozenset[str] = frozenset()) -> Any:
    value = value.strip().rstrip(",")
    if value in {"true", "false", "null"}:
        return {"true": True, "false": False, "null": None}[value]
    if value in allowed_expressions:
        return value
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value[1:-1]
    raise CandidateError(f"expected a literal value, got dynamic expression {value!r}")


def _parse_object(source: str, *, allow_registration_function: bool = False) -> dict[str, Any]:
    source = source.strip()
    start = source.find("{")
    if start < 0:
        raise CandidateError("expected an object literal")
    end = _find_balanced(source, start, "{", "}")
    result: dict[str, Any] = {}
    for part in _split_top_level(source[start + 1 : end]):
        pair = _split_property(part)
        if not pair:
            raise CandidateError(f"unsupported object property syntax {part!r}")
        key, value = pair
        key = key.strip()
        if len(key) >= 2 and key[0] == key[-1] and key[0] in "'\"`":
            key = str(_literal(key))
        elif not re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", key):
            raise CandidateError(f"dynamic or computed object key is unsupported: {key!r}")
        if key in result:
            raise CandidateError(f"duplicate object property is unsupported: {key}")
        if key == "func" and allow_registration_function:
            if not re.match(r"^async\s*\(\s*args\s*\)\s*=>\s*\{", value.strip()):
                raise CandidateError("CLI func must be the statically reviewed async (args) => { ... } form")
            result[key] = "<adapter-function-source-not-evaluated-by-inspector>"
        elif key in {"args", "columns"} and allow_registration_function:
            if not value.strip().startswith("["):
                raise CandidateError(f"CLI registration {key} must be a static array literal")
            result[key] = value.strip()
        else:
            result[key] = _literal(value, allowed_expressions=frozenset({"Strategy.PUBLIC"}))
    return result


def _array_items(source: str) -> list[str]:
    start = source.find("[")
    if start < 0:
        raise CandidateError("expected an array literal")
    end = _find_balanced(source, start, "[", "]")
    return _split_top_level(source[start + 1 : end])


def extract_cli_declaration(source: str) -> dict[str, Any]:
    matches = list(re.finditer(r"\bcli\s*\(\s*\{", source))
    if len(matches) != 1:
        raise CandidateError(f"expected exactly one static cli({{...}}) registration, found {len(matches)}")
    object_start = source.find("{", matches[0].start())
    object_end = _find_balanced(source, object_start, "{", "}")
    declaration = _parse_object(source[object_start : object_end + 1], allow_registration_function=True)

    allowed_keys = {"site", "name", "access", "description", "domain", "strategy", "browser", "args", "columns", "func"}
    if not set(declaration) <= allowed_keys:
        raise CandidateError(f"CLI registration contains unsupported fields: {sorted(set(declaration) - allowed_keys)}")
    if not {"site", "name", "access", "description", "strategy", "browser", "args", "columns", "func"} <= set(declaration):
        raise CandidateError("CLI registration is missing a required statically inspectable field")
    if declaration.get("browser") is not False:
        raise CandidateError("positive candidate must explicitly declare browser: false")
    if not isinstance(declaration.get("site"), str) or not isinstance(declaration.get("name"), str):
        raise CandidateError("CLI registration site and name must be string literals")
    if not isinstance(declaration.get("access"), str) or not isinstance(declaration.get("description"), str):
        raise CandidateError("CLI registration access and description must be string literals")
    if "domain" in declaration and not isinstance(declaration["domain"], str):
        raise CandidateError("CLI registration domain must be a string literal")

    args_raw = declaration.get("args")
    columns_raw = declaration.get("columns")
    if not isinstance(args_raw, str) or not isinstance(columns_raw, str):
        raise CandidateError("CLI registration must use static args and columns arrays")
    declaration["args"] = [_parse_object(item) for item in _array_items(args_raw)]
    declaration["columns"] = [str(_literal(item)) for item in _array_items(columns_raw)]
    return declaration


def imports(source: str) -> list[str]:
    found: list[str] = []
    for match in re.finditer(r"^\s*import\s+(?:[^;\n]+?\s+from\s+)?['\"]([^'\"]+)['\"]", source, re.MULTILINE):
        found.append(match.group(1))
    return found


def unsafe_markers(source: str) -> list[str]:
    rules = {
        "dynamic_code": r"\b(?:eval|Function)\s*\(",
        "dynamic_import": r"\bimport\s*\(",
        "local_process": r"(?:node:)?child_process|\b(?:spawn|execFile)\s*\(",
        "filesystem": r"(?:node:)?(?:fs|fs/promises)\b|\b(?:readFileSync|writeFileSync|mkdirSync)\s*\(",
        "browser_credentials": r"\.getCookies\s*\(|\bCookie\s*:",
        "raw_protocol": r"\.cdp\s*\(|bridge\.send\s*\(\s*method\s*,",
        "process_environment": r"\bprocess\.env\b",
    }
    return [name for name, pattern in rules.items() if re.search(pattern, source)]


def _line_number(source: str, anchor: str) -> int:
    index = source.find(anchor)
    if index < 0:
        raise CandidateError(f"source evidence anchor not found: {anchor}")
    return source.count("\n", 0, index) + 1


def _source_record(config: dict[str, Any]) -> dict[str, Any]:
    source = config["source"]
    package_path = ROOT / source["package_json"]
    license_path = ROOT / source["license_file"]
    package_bytes = read_utf8(package_path)
    package = json.loads(package_bytes)
    if package.get("name") != source["package_name"] or package.get("version") != source["version"]:
        raise CandidateError("vendored OpenCLI package name or version differs from the pinned candidate")
    if package.get("license") != source["license"]:
        raise CandidateError("vendored OpenCLI license differs from the candidate record")
    if sha256(package_path) != source["package_json_sha256"]:
        raise CandidateError("OpenCLI package.json digest differs from the immutable candidate pin")
    if sha256(license_path) != source["license_sha256"]:
        raise CandidateError("OpenCLI LICENSE digest differs from the immutable candidate pin")

    lifecycle_names = [
        name
        for name in ("preinstall", "install", "postinstall", "prepare", "prepublish", "prepublishOnly", "preuninstall")
        if name in package.get("scripts", {})
    ]
    return {
        "repository": source["repository"],
        "package_name": source["package_name"],
        "version": source["version"],
        "commit": source["commit"],
        "license": source["license"],
        "license_file": source["license_file"],
        "notice_file": source.get("notice_file"),
        "package_json_sha256": source["package_json_sha256"],
        "license_sha256": source["license_sha256"],
        "package_dependencies": package.get("dependencies", {}),
        "package_lifecycle_hooks_present_but_never_run": lifecycle_names,
        "install_hooks_run": False,
        "network_used_during_inspection": False,
        "upstream_code_executed_during_inspection": False,
    }


def _field_schema(sample: dict[str, Any]) -> dict[str, Any]:
    properties: dict[str, Any] = {}
    for field in sample["fields"]:
        properties[field["name"]] = {"type": field["type"]}
    return {
        "type": "array",
        "items": {
            "type": "object",
            "properties": properties,
            "required": [field["name"] for field in sample["fields"]],
            "additionalProperties": False,
        },
    }


def _input_schema(sample: dict[str, Any]) -> dict[str, Any]:
    properties: dict[str, Any] = {}
    required: list[str] = []
    for field in sample["inputs"]:
        prop = {key: value for key, value in field.items() if key not in {"name", "required", "positional", "evidence"}}
        properties[field["name"]] = prop
        if field.get("required"):
            required.append(field["name"])
    return {"type": "object", "properties": properties, "required": required, "additionalProperties": False}


def _sample_report(sample: dict[str, Any]) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    content: dict[str, str] = {}
    for relative, expected_hash in sample["sha256"].items():
        path = ROOT / relative
        actual_hash = sha256(path)
        if actual_hash != expected_hash:
            raise CandidateError(f"source digest mismatch for {relative}: expected {expected_hash}, got {actual_hash}")
        source = read_utf8(path)
        content[relative] = source
        files.append({"path": relative.removeprefix("third_party/opencli-1.8.8/"), "sha256": actual_hash, "bytes": path.stat().st_size})

    entry = content[sample["entrypoint"]]
    declaration = extract_cli_declaration(entry)
    imports_by_file = {relative: imports(source) for relative, source in content.items()}
    if imports_by_file != sample["expected_imports_by_file"]:
        raise CandidateError(f"unexpected import set in {sample['id']}: {imports_by_file}")
    hazards = {relative: unsafe_markers(source) for relative, source in content.items()}
    hazards = {relative: markers for relative, markers in hazards.items() if markers}
    if hazards:
        raise CandidateError(f"unsupported code marker in positive sample {sample['id']}: {hazards}")
    if declaration.get("site") != sample["opencli_site"] or declaration.get("name") != sample["opencli_name"]:
        raise CandidateError(f"OpenCLI registration identity changed for {sample['id']}")
    if declaration.get("access") != "read" or declaration.get("strategy") != "Strategy.PUBLIC":
        raise CandidateError(f"sample {sample['id']} is not declared as a public read adapter")
    if declaration.get("browser") is not False:
        raise CandidateError(f"sample {sample['id']} must explicitly declare browser: false")
    if declaration.get("columns") != [field["name"] for field in sample["fields"]]:
        raise CandidateError(f"field mapping for {sample['id']} must account for all and only source columns")
    args = declaration["args"]
    if [item.get("name") for item in args] != [item["name"] for item in sample["inputs"]]:
        raise CandidateError(f"input mapping for {sample['id']} does not match the source argument order")
    type_map = {"int": "integer"}
    for actual, expected in zip(args, sample["inputs"], strict=True):
        actual_type = type_map.get(actual.get("type"), actual.get("type", "string"))
        if expected["type"] != actual_type:
            raise CandidateError(f"input type mismatch for {sample['id']}.{expected['name']}")
        if bool(actual.get("required", False)) != bool(expected.get("required", False)):
            raise CandidateError(f"input requiredness mismatch for {sample['id']}.{expected['name']}")
        if bool(actual.get("positional", False)) != bool(expected.get("positional", False)):
            raise CandidateError(f"input positional mismatch for {sample['id']}.{expected['name']}")
        if "default" in expected and actual.get("default") != expected["default"]:
            raise CandidateError(f"input default mismatch for {sample['id']}.{expected['name']}")

    source_anchors = []
    for anchor in sample["request"]["evidence"]:
        matching = next(((relative, source) for relative, source in content.items() if anchor in source), None)
        if matching is None:
            raise CandidateError(f"request evidence anchor missing for {sample['id']}: {anchor}")
        relative, source = matching
        source_anchors.append({"path": relative, "line": _line_number(source, anchor), "text": anchor})

    input_anchors = []
    for field in sample["inputs"]:
        anchor = field["evidence"]
        matching = next(((relative, source) for relative, source in content.items() if anchor in source), None)
        if matching is None:
            raise CandidateError(f"input evidence anchor missing for {sample['id']}.{field['name']}: {anchor}")
        input_anchors.append({"field": field["name"], "text": anchor})

    field_anchors = []
    for field in sample["fields"]:
        anchor = field["evidence"]
        matching = next(((relative, source) for relative, source in content.items() if anchor in source), None)
        if matching is None:
            raise CandidateError(f"output field evidence anchor missing for {sample['id']}.{field['name']}: {anchor}")
        relative, source = matching
        field_anchors.append({"field": field["name"], "path": relative, "line": _line_number(source, anchor), "text": anchor})

    return {
        "id": sample["id"],
        "selection_reason": sample["selection_reason"],
        "opencli_registration": {
            "site": declaration.get("site"),
            "name": declaration.get("name"),
            "access": declaration.get("access"),
            "domain": declaration.get("domain"),
            "strategy": declaration.get("strategy"),
            "browser": declaration.get("browser"),
            "arguments": declaration.get("args"),
            "columns_as_field_name_clues_only": declaration.get("columns"),
            "source_imports_by_file": imports_by_file,
        },
        "files": sorted(files, key=lambda item: item["path"]),
        "parser": sample["parser"],
        "response_kind": sample["response_kind"],
        "request_candidate": sample["request"],
        "request_evidence": source_anchors,
        "input_schema_draft": _input_schema(sample),
        "input_argument_semantics": sample["inputs"],
        "input_evidence": input_anchors,
        "output_schema_draft": _field_schema(sample),
        "output_field_semantics": sample["fields"],
        "output_field_evidence": field_anchors,
        "pagination_semantics": sample["pagination"],
        "limitations": sample["limitations"],
        "source_reuse": {
            "original_parser_and_mapping_source_changed": False,
            "business_logic_reimplemented": False,
            "files": files,
        },
        "module_effects_review": {
            "inspector_imported_or_executed_upstream_modules": False,
            "declared_imports": imports_by_file,
            "external_import_top_level_effects": "unknown; the OpenCLI registry/errors modules are not part of the selected source snapshot and were not imported or executed",
            "local_import_top_level_effects": "arXiv utils.js source is bundled and evaluated only in the offline harness; external effects from its original errors import are unknown",
            "reuse_disposition": "manual review is required for every new adapter; this report does not infer safety from the marker scan",
        },
        "webenvoy_candidate_requirements": [
            "Accepted task declaration for anonymous HTTPS reads with exact origin/path/query/header and response limits.",
            "Accepted managed broker operation and redirect revalidation; do not use script-native fetch.",
            "Accepted completeness/error projection for body truncation, malformed response, refusal, timeout and cancellation.",
        ],
        "package_status": "three proposed Lode package candidates are generated and locatable in the existing registry; no code admission, install, enablement, or execution is claimed",
    }


def _negative_report(example: dict[str, Any]) -> dict[str, Any]:
    path = ROOT / example["path"]
    actual_hash = sha256(path)
    if actual_hash != example["sha256"]:
        raise CandidateError(f"negative source digest mismatch for {example['id']}")
    source = read_utf8(path)
    found = []
    for anchor in example["evidence"]:
        line = _line_number(source, anchor)
        found.append({"line": line, "text": anchor})
    markers = unsafe_markers(source)
    expected_marker = {
        "cookie-download": "browser_credentials",
        "raw-cdp": "raw_protocol",
        "local-process-and-credentials": "local_process",
    }[example["id"]]
    if expected_marker not in markers:
        raise CandidateError(f"negative source {example['id']} did not trigger {expected_marker}")
    return {
        "id": example["id"],
        "path": example["path"].removeprefix("third_party/opencli-1.8.8/"),
        "sha256": actual_hash,
        "classification": example["classification"],
        "markers": markers,
        "evidence": found,
        "executed": False,
    }


def build_report() -> dict[str, Any]:
    config = json.loads(read_utf8(CONFIG))
    source = _source_record(config)
    samples = [_sample_report(sample) for sample in config["samples"]]
    if len(samples) != 3 or len({sample["opencli_registration"]["domain"] or sample["request_candidate"]["origin"] for sample in samples}) < 2:
        raise CandidateError("fixed candidate set must contain three positive adapters over at least two sites")
    negatives = [_negative_report(example) for example in config["negative_samples"]]
    return {
        "report_kind": "lode.opencli-static-compatibility-candidates/v1",
        "scope": "fixed-source static review and offline semantics; not a package admission or runtime contract",
        "source": source,
        "positive_candidates": samples,
        "negative_samples": negatives,
        "inspection_constraints": {
            "source_read_mode": "UTF-8 bytes only",
            "upstream_modules_imported": False,
            "upstream_code_executed_by_inspector": False,
            "install_hooks_run": False,
            "network_requests_made": False,
            "registry_write_attempted_by_inspector": False,
            "marker_scan_is_general_security_proof": False,
        },
        "shared_execution_gap": [
            "The adapters use global fetch; the proposed WebEnvoy network.public_read and broker/v1.1 fields remain a cross-repository candidate until accepted and implemented.",
            "The Lode package candidates declare only the pinned anonymous HTTPS request policy and do not grant owner approval, code admission, installation, enablement, or runtime access.",
        ],
        "reuse_assessment": {
            "upstream_parser_and_parameter_logic_rewritten": False,
            "third_sample": "arxiv-recent-atom",
            "third_sample_requires_generator_logic": True,
            "third_sample_specific_work": [
                "Bundle a second, statically imported upstream source file while preserving the helper/parser body.",
                "Add Atom feed envelope, totalResults, entry-count, URL, and confirmed-empty checks to the shared wrapper.",
            ],
            "site_specific_webenvoy_runtime_branch_added": False,
            "declaration_fixture_only_reuse_goal_met": False,
            "time_or_cost_measurement": "not recorded",
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    source = report["source"]
    lines = [
        "# OpenCLI v1.8.8 公共只读兼容候选",
        "",
        "状态：固定源码静态审查、离线 adapter 语义候选和三个 proposed Lode 包文件已形成；**未完成代码准入、正式安装、live 执行或独立业务结果核验**。",
        "",
        "## 来源与检查边界",
        "",
        f"- 上游：[`{source['repository']}` {source['version']}](https://github.com/{source['repository']}/tree/{source['commit']})，固定 commit `{source['commit']}`。",
        f"- 许可：`{source['license']}`；`NOTICE`: `{source['notice_file'] or '未发现'}`；保留副本 `{source['license_file']}`，SHA-256 `{source['license_sha256']}`。",
        f"- package.json SHA-256：`{source['package_json_sha256']}`。",
        f"- 上游 package lifecycle hooks 存在：{', '.join(f'`{hook}`' for hook in source['package_lifecycle_hooks_present_but_never_run']) or '无'}；检查期间未运行。",
        "- 检查器只读固定源文件，不导入/执行上游模块，不运行安装钩子，不访问网站；拒绝样本也只做静态文本检查。",
        "- 三个候选包分别进入现有本地 registry，lifecycle 保持 proposed；候选可发现不等于信任、代码准入、安装或启用。官方 Lode validator 的 warning 继续标示 WebEnvoy #594 合同尚待接受。",
        "- `Strategy.PUBLIC`、`access: read` 和 GET 本身不授予权限，也不证明 URL 安全。每个 task 仍需 WebEnvoy 授权及受管匿名 HTTP broker。",
        "",
        "## 固定正向样本",
        "",
    ]
    for sample in report["positive_candidates"]:
        registration = sample["opencli_registration"]
        request = sample["request_candidate"]
        file_labels = [f"`{item['path']}` (`{item['sha256']}`)" for item in sample["files"]]
        import_labels = [f"`{module}`" for modules in registration["source_imports_by_file"].values() for module in modules]
        lines.extend([
            f"### `{sample['id']}` — `{registration['site']} {registration['name']}`",
            "",
            sample["selection_reason"],
            "",
            f"- 源文件：{', '.join(file_labels)}。",
            f"- 源 imports：{', '.join(import_labels)}。",
            f"- parser：`{sample['parser']}`；响应候选 `{sample['response_kind']}`；分页：{sample['pagination_semantics']}",
            f"- 请求：`{request['method']} {request['origin']}{request['path_template']}`；query `{json.dumps(request['query'], ensure_ascii=False)}`；Accept `{request['accept'] or '上游未设置'}`；User-Agent `{request['user_agent'] or '上游未设置'}`。",
            "- 参数来自静态注册及参数校验源码：",
            "",
            "  | 参数 | 类型 | 必需/默认值/范围 | 证据 |",
            "  | --- | --- | --- | --- |",
        ])
        for field in sample["input_argument_semantics"]:
            flags = []
            if field.get("required"):
                flags.append("必需")
            if field.get("positional"):
                flags.append("位置参数")
            if "default" in field:
                flags.append(f"默认 `{field['default']}`")
            if "minimum" in field or "maximum" in field:
                flags.append(f"范围 {field.get('minimum', '?')}–{field.get('maximum', '?')}")
            if "enum" in field:
                flags.append("枚举 " + ", ".join(f"`{value}`" for value in field["enum"]))
            if "pattern" in field:
                flags.append(f"格式 `{field['pattern']}`")
            lines.append(f"  | `{field['name']}` | `{field['type']}` | {'; '.join(flags) or '可选'} | `{field['evidence']}` |")
        lines.extend([
            "",
            "- 输出字段是人工按映射表达式核对的 schema 草稿；`columns` 只作为字段名线索：",
            "",
            "  | 字段 | 类型 | 缺失/空值语义 | 源码锚点 |",
            "  | --- | --- | --- | --- |",
        ])
        for field, evidence in zip(sample["output_field_semantics"], sample["output_field_evidence"], strict=True):
            missing = field["missing"].replace("|", "\\|")
            lines.append(f"  | `{field['name']}` | `{json.dumps(field['type'], ensure_ascii=False)}` | {missing} | `{evidence['path']}:{evidence['line']}` |")
        lines.extend(["", "- 未决边界："])
        lines.extend(f"  - {item}" for item in sample["limitations"])
        lines.append("")
    lines.extend([
        "## 固定拒绝样本",
        "",
        "| 来源 | 分类 | 静态锚点 | 执行 |",
        "| --- | --- | --- | --- |",
    ])
    for sample in report["negative_samples"]:
        anchors = ", ".join(f"`{sample['path']}:{item['line']}`" for item in sample["evidence"])
        lines.append(f"| `{sample['path']}` (`{sample['sha256']}`) | {sample['classification']} | {anchors} | 未执行 |")
    lines.extend([
        "",
        "## 复用结果与待补合同",
        "",
        "三个正向样本覆盖 GitHub HTML、DEV.to JSON、arXiv Atom/XML。上游参数处理和 parser 函数体保持原样，wrapper 将原 fetch 映射到候选 broker，并补有界完整性检查。第三个样本没有新增 WebEnvoy 站点专属 Runtime 分支，但确实需要改动 Lode 生成器：支持 arXiv 两文件静态 bundle，并加入 Atom envelope、totalResults、entry 数量及明确空集检查。因此“第三样本只需声明/schema/check/fixture”的复用目标未达到；没有记录耗时或成本，不能据此声称接入提效。",
        "",
        "任何正式 Lode task 包都还需固定：任务绑定的 HTTPS origin/path/query/header、匿名请求策略、重定向逐跳复核、响应 MIME 与解压体积、预算/超时/取消、完整性事实和失败结果。脚本不能通过 Node `fetch` 自行访问网络；HTTP 2xx 不代表业务成功。",
        "",
        "## 离线行为验证",
        "",
        "`tools/test_opencli_readonly_semantics.mjs` 在静态摘要验证成功后，用 Node 内置 VM 和合成 fixture 分别运行固定上游源码及实际生成的三份候选脚本。测试禁止额外 module imports，并禁用 VM 字符串代码生成；覆盖正常值、合法空集、无证据空集、缺失字段、异常/截断正文、分页、参数错误和响应丢失。它只证明离线语义与包装行为，不代表 WebEnvoy broker、安装、真实网站、业务结果或 Plugin 验收。",
        "",
        "候选阶段边界：本报告证明固定源码静态可分析；候选包的结构校验由 Lode 官方 validator/CI 单独执行。代码准入、正式安装、真实站点执行、业务结果独立核验均不由本报告证明。",
        "",
        "重复检查：`python3 tools/opencli_readonly_candidates.py --check`；离线行为：`node --experimental-vm-modules tools/test_opencli_readonly_semantics.mjs`。",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true", help="write deterministic reports to docs/verification")
    group.add_argument("--check", action="store_true", help="check committed reports against pinned source bytes")
    args = parser.parse_args()
    try:
        candidate_report = build_report()
        report = json.dumps(candidate_report, ensure_ascii=False, indent=2) + "\n"
        markdown = render_markdown(candidate_report)
        if args.write:
            REPORT_JSON.write_text(report, encoding="utf-8")
            REPORT_MARKDOWN.write_text(markdown, encoding="utf-8")
            print(f"wrote {REPORT_JSON} and {REPORT_MARKDOWN}")
            return 0
        stale = []
        for path, expected in ((REPORT_JSON, report), (REPORT_MARKDOWN, markdown)):
            if read_utf8(path) != expected:
                stale.append(str(path.relative_to(ROOT)))
        if stale:
            print(f"candidate reports are stale: {', '.join(stale)}", file=sys.stderr)
            return 1
        print("candidate reports match fixed OpenCLI source")
        return 0
    except (CandidateError, OSError, json.JSONDecodeError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
