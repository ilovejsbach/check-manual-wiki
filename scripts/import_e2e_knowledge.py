from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def screen_code(value: object) -> str | None:
    text = str(value or "")
    return text if len(text) == 4 and text.isdigit() else None


def artifact_path(e2e_root: Path, path: Path) -> str:
    return f"check-e2e/{path.relative_to(e2e_root).as_posix()}"


def collect(e2e_root: Path) -> list[dict[str, Any]]:
    golden = e2e_root / "golden"
    records: dict[str, dict[str, Any]] = {}
    observed_at: dict[str, list[str]] = defaultdict(list)
    fields: dict[str, set[str]] = defaultdict(set)
    tabs: dict[str, set[str]] = defaultdict(set)
    evidence: dict[str, set[str]] = defaultdict(set)
    warnings: dict[str, set[str]] = defaultdict(set)
    field_definitions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    semantic_sources: dict[str, dict[str, Any]] = defaultdict(dict)

    def ensure(code: str) -> dict[str, Any]:
        return records.setdefault(
            code,
            {
                "schema_version": "1.0",
                "id": f"check:e2e:screen:{code}",
                "screen_id": f"check:screen:{code}",
                "screen_code": code,
                "observation_status": "discovered",
                "golden_status": "not_started",
                "financial_review_status": "not_reviewed",
                "title_observed": None,
                "category": None,
                "callability_status": "unverified",
                "result_data_status": None,
                "interaction_risk": None,
            },
        )

    for path in sorted(golden.rglob("manifest.json")):
        data = read_json(path)
        code = screen_code(data.get("screen_code"))
        if not code:
            continue
        record = ensure(code)
        status = str(data.get("status") or "")
        if status == "completed":
            record["observation_status"] = "baseline_observed"
            record["callability_status"] = "verified"
            record["golden_status"] = "baseline_observed"
        elif status:
            record["observation_status"] = status
        record["title_observed"] = data.get("observed_title") or data.get("expected_title")
        record["category"] = data.get("category") or record.get("category")
        record["capture_review_status"] = data.get("capture_review_status")
        record["query_settle_status"] = data.get("query_settle_status")
        evidence[code].add(artifact_path(e2e_root, path))
        for item in data.get("artifacts", []):
            candidate = path.parent / str(item)
            if candidate.exists():
                evidence[code].add(artifact_path(e2e_root, candidate))

    for path in sorted(golden.rglob("inventory.json")):
        data = read_json(path)
        code = screen_code(data.get("screen_code"))
        if not code:
            continue
        record = ensure(code)
        record["title_observed"] = data.get("title") or record.get("title_observed")
        record["category"] = data.get("category") or record.get("category")
        if data.get("collected_at"):
            observed_at[code].append(str(data["collected_at"]))
        tabs[code].update(str(item).strip() for item in data.get("tabs", []) if str(item).strip())
        evidence[code].add(artifact_path(e2e_root, path))

    for path in sorted(golden.glob("batch-*/analysis.json")):
        data = read_json(path)
        for item in data.get("screens", []):
            if not isinstance(item, dict):
                continue
            code = screen_code(item.get("screen_code"))
            if not code:
                continue
            record = ensure(code)
            record["callability_status"] = (
                item.get("callability_status") or record["callability_status"]
            )
            record["result_data_status"] = item.get("result_data_status")
            record["interaction_risk"] = item.get("interaction_risk")
            record["financial_review_status"] = item.get("financial_semantics_status") or (
                "not_reviewed"
            )
            record["ui_role"] = item.get("role")
            record["ui_role_status"] = item.get("ui_role_status")
            fields[code].update(
                str(value).strip()
                for value in item.get("observed_financial_fields", [])
                if str(value).strip()
            )
            occlusion = item.get("capture_occlusion")
            if isinstance(occlusion, dict) and occlusion.get("status") not in {
                None,
                "none",
                "clean",
            }:
                warnings[code].add(str(occlusion["status"]))
            evidence[code].add(artifact_path(e2e_root, path))
            artifacts = item.get("artifacts", {})
            if isinstance(artifacts, dict):
                for value in artifacts.values():
                    candidate = golden / str(value)
                    if candidate.exists():
                        evidence[code].add(artifact_path(e2e_root, candidate))

    reference = golden / "1300" / "reference.json"
    if reference.exists():
        data = read_json(reference)
        code = screen_code(data.get("screen_code"))
        if code:
            record = ensure(code)
            record["title_observed"] = data.get("title") or record.get("title_observed")
            record["category"] = data.get("category") or record.get("category")
            record["observation_status"] = "deep_observed"
            record["callability_status"] = "verified"
            record["golden_status"] = str(data.get("status") or "in_progress")
            coverage = data.get("coverage", {})
            record["coverage"] = coverage if isinstance(coverage, dict) else {}
            structure = data.get("observed_structure", {})
            if isinstance(structure, dict):
                for key in ("top_tabs", "price_panel_tabs", "analysis_tabs", "member_tabs"):
                    tabs[code].update(
                        str(value).strip() for value in structure.get(key, []) if str(value).strip()
                    )
            for concept in data.get("financial_semantics", []):
                if isinstance(concept, dict) and concept.get("concept"):
                    fields[code].add(str(concept["concept"]))
            if data.get("financial_semantics"):
                record["financial_review_status"] = "partial_unapproved"
            evidence[code].add(artifact_path(e2e_root, reference))

    for path in sorted(golden.rglob("financial-semantics.json")):
        data = read_json(path)
        code = screen_code(data.get("screen_code"))
        if not code:
            continue
        ensure(code)
        for item in data.get("concepts", []):
            if isinstance(item, dict) and (item.get("field") or item.get("concept")):
                field_definitions[code].append(item)
        source_values = data.get("sources", {})
        if isinstance(source_values, dict):
            semantic_sources[code].update(source_values)
        evidence[code].add(artifact_path(e2e_root, path))

    output = []
    for code, record in sorted(records.items()):
        record["observed_at"] = max(observed_at[code], default=None)
        record["observed_fields"] = sorted(fields[code])
        record["observed_tabs"] = sorted(tabs[code])
        record["evidence"] = sorted(evidence[code])
        record["warnings"] = sorted(warnings[code])
        record["field_definitions"] = field_definitions[code]
        record["semantic_sources"] = semantic_sources[code]
        output.append(record)
    return output


def write_jsonl(records: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert CHECK E2E golden evidence to wiki JSONL")
    parser.add_argument("e2e_root", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    records = collect(args.e2e_root.resolve())
    write_jsonl(records, args.output)
    summary = {
        "record_count": len(records),
        "callability_verified_count": sum(
            record["callability_status"] == "verified" for record in records
        ),
        "deep_observed_count": sum(
            record["observation_status"] == "deep_observed" for record in records
        ),
        "financially_approved_count": sum(
            record["financial_review_status"] == "approved" for record in records
        ),
    }
    print(json.dumps(summary, ensure_ascii=False) if args.json else summary)


if __name__ == "__main__":
    main()
