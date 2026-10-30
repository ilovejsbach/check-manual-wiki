from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content" / "check-expert"
KNOWLEDGE_DIR = ROOT / "knowledge" / "check-expert"


def parse_markdown(path: Path) -> tuple[dict[str, object], str]:
    raw = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", raw, re.DOTALL)
    if not match:
        return {}, raw
    return yaml.safe_load(match.group(1)) or {}, match.group(2)


def validate() -> tuple[dict[str, object], list[str]]:
    errors: list[str] = []
    markdown_files = sorted(CONTENT_DIR.rglob("*.md"))
    if not markdown_files:
        return {}, ["no generated Markdown files"]

    ids: list[str] = []
    missing_source = 0
    empty_bodies = 0
    size_outliers: list[str] = []
    for path in markdown_files:
        metadata, body = parse_markdown(path)
        if path.name not in {"화면번호-색인.md", "업무-기능-색인.md"}:
            knowledge_id = metadata.get("knowledge_id")
            if knowledge_id:
                ids.append(str(knowledge_id))
            if not metadata.get("source"):
                missing_source += 1
        if len(body.strip()) < 20:
            empty_bodies += 1
        if path.stat().st_size > 1_500_000:
            size_outliers.append(path.relative_to(CONTENT_DIR).as_posix())

    duplicates = [key for key, count in Counter(ids).items() if count > 1]
    if duplicates:
        errors.append(f"duplicate knowledge IDs: {duplicates[:10]}")
    if missing_source:
        errors.append(f"documents missing source: {missing_source}")
    if empty_bodies:
        errors.append(f"documents with nearly empty bodies: {empty_bodies}")
    if size_outliers:
        errors.append(f"oversized Markdown documents: {size_outliers[:10]}")

    jsonl_path = KNOWLEDGE_DIR / "knowledge.jsonl"
    if not jsonl_path.exists():
        errors.append("knowledge.jsonl is missing")
        records: list[dict[str, object]] = []
    else:
        records = [json.loads(line) for line in jsonl_path.read_text(encoding="utf-8").splitlines()]
    record_ids = {str(record["id"]) for record in records}
    if len(record_ids) != len(records):
        errors.append("knowledge.jsonl contains duplicate record IDs")
    unresolved = sorted(
        {
            str(related)
            for record in records
            for related in record.get("related_ids", [])
            if related not in record_ids
        }
    )
    for required in [CONTENT_DIR / "화면번호-색인.md", CONTENT_DIR / "업무-기능-색인.md"]:
        if not required.exists():
            errors.append(f"required human index missing: {required.name}")
    for required in [
        "knowledge.jsonl",
        "manifest.json",
        "llms.txt",
        "check-manual-wiki-data.zip",
    ]:
        if not (CONTENT_DIR / "api" / required).exists():
            errors.append(f"required API asset missing: {required}")

    manifest_path = KNOWLEDGE_DIR / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("record_count") != len(records):
            errors.append("manifest record_count does not match knowledge.jsonl")
        if manifest.get("screen_count") != sum(
            record.get("type") == "screen" for record in records
        ):
            errors.append("manifest screen_count does not match knowledge.jsonl")
    else:
        errors.append("manifest.json is missing")

    report: dict[str, object] = {
        "markdown_documents": len(markdown_files),
        "knowledge_ids": len(ids),
        "knowledge_records": len(records),
        "screen_records": sum(record.get("type") == "screen" for record in records),
        "unresolved_related_ids": len(unresolved),
        "unresolved_examples": unresolved[:20],
        "oversized_documents": size_outliers,
    }
    return report, errors


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report, errors = validate()
    payload = {"ok": not errors, "report": report, "errors": errors}
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload)
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
