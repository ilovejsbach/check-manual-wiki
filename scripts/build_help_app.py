from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "knowledge" / "check-expert" / "knowledge.jsonl"
APP_SOURCE = ROOT / "help-app"
OUTPUT = ROOT / "help-dist"


def load_records(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def build(source: Path = SOURCE, output: Path = OUTPUT) -> dict[str, object]:
    records = load_records(source)
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(APP_SOURCE, output)
    data_dir = output / "data"
    data_dir.mkdir()

    by_id = {str(record["id"]): record for record in records}
    payload: list[dict[str, object]] = []
    for record in records:
        relationship_by_id = {
            str(item.get("target_id")): item
            for item in record.get("relationships", [])
            if isinstance(item, dict)
        }
        related = [
            {
                "id": related_id,
                "title": by_id.get(str(related_id), {}).get("title", related_id),
                "screen_code": by_id.get(str(related_id), {}).get("screen_code"),
                "review_status": by_id.get(str(related_id), {}).get("review_status"),
                "relation_type": relationship_by_id.get(str(related_id), {}).get("type"),
                "relation_label": relationship_by_id.get(str(related_id), {}).get("label"),
            }
            for related_id in record.get("related_ids", [])
            if str(related_id) in by_id
        ]
        payload.append(
            {
                "id": record["id"],
                "type": record.get("type"),
                "title": record.get("title"),
                "aliases": record.get("aliases", []),
                "category": record.get("category"),
                "screen_code": record.get("screen_code"),
                "source": record.get("source"),
                "source_locator": record.get("source_locator"),
                "review_status": record.get("review_status"),
                "mapping_status": record.get("mapping_status"),
                "signal_count": record.get("signal_count"),
                "markdown_path": record.get("markdown_path"),
                "related": related,
                "text": record.get("text", ""),
            }
        )

    serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    (data_dir / "knowledge.json").write_text(serialized, encoding="utf-8")
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    manifest = {
        "schema_version": "1.0",
        "app": "CHECK Expert 로컬 도움말",
        "record_count": len(payload),
        "screen_count": sum(item.get("screen_code") is not None for item in payload),
        "candidate_count": sum(item.get("review_status") == "candidate" for item in payload),
        "source_sha256": source_hash,
        "data_bytes": len(serialized.encode("utf-8")),
    }
    (data_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    assets = ROOT / "content" / "check-expert" / "assets"
    if assets.exists():
        shutil.copytree(assets, output / "assets")
    (output / ".nojekyll").write_text("", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the GitHub/local CHECK help application")
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = build(args.source, args.output)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else result)


if __name__ == "__main__":
    main()
