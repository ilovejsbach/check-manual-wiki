from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "knowledge" / "check-expert" / "knowledge.jsonl"


def normalize(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().casefold()


def tokens(value: object) -> list[str]:
    return re.findall(r"[0-9a-z가-힣]+", normalize(value))


def load_records(path: Path = DEFAULT_INDEX) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def score_record(record: dict[str, Any], query: str) -> float:
    query_normalized = normalize(query)
    query_tokens = tokens(query)
    if not query_tokens:
        return 0

    title = normalize(record.get("title"))
    aliases = [normalize(alias) for alias in record.get("aliases", [])]
    screen_code = normalize(record.get("screen_code"))
    category = normalize(record.get("category"))
    case_context = normalize(
        " ".join(
            [
                str(record.get("case_type") or ""),
                str(record.get("case_topic") or ""),
                *[str(item) for item in record.get("case_topics", [])],
                *[str(item) for item in record.get("case_facets", [])],
            ]
        )
    )
    text = normalize(record.get("text"))

    score = 0.0
    # Prefer official screen/manual guidance over noisy case-topic overlap in general search.
    score += {"screen": 24, "manual": 8, "excel": 4}.get(str(record.get("type")), 0)
    if record.get("type") == "support_case":
        score -= 20
    elif str(record.get("id", "")).startswith("check:enrichment:"):
        score -= 16
    if query_normalized == screen_code:
        score += 100
    if query_normalized == title or query_normalized in aliases:
        score += 80
    if query_normalized and query_normalized in title:
        score += 30
    if any(query_normalized in alias for alias in aliases):
        score += 25

    title_tokens = set(tokens(title))
    alias_tokens = set(tokens(" ".join(aliases)))
    category_tokens = set(tokens(category))
    for token in query_tokens:
        if token in title_tokens:
            score += 12
        if token in alias_tokens:
            score += 10
        if token in category_tokens:
            score += 5
        if token in set(tokens(case_context)):
            score += 1
        score += min(text.count(token), 8) * 0.5
    return score


def search(
    records: list[dict[str, Any]],
    query: str,
    *,
    limit: int = 5,
    record_type: str | None = None,
    category: str | None = None,
    case_type: str | None = None,
) -> list[dict[str, Any]]:
    ranked: list[tuple[float, dict[str, Any]]] = []
    for record in records:
        if record_type and record.get("type") != record_type:
            continue
        if category and normalize(category) not in normalize(record.get("category")):
            continue
        if case_type and record.get("case_type") != case_type:
            continue
        score = score_record(record, query)
        if score > 0:
            ranked.append((score, record))
    ranked.sort(key=lambda item: (-item[0], str(item[1].get("id"))))
    return [{"score": score, **record} for score, record in ranked[:limit]]


def compact_result(record: dict[str, Any]) -> dict[str, Any]:
    text = normalize(record.get("text"))
    return {
        "score": record["score"],
        "id": record.get("id"),
        "title": record.get("title"),
        "type": record.get("type"),
        "screen_code": record.get("screen_code"),
        "category": record.get("category"),
        "case_type": record.get("case_type"),
        "case_topics": record.get("case_topics", []),
        "source": record.get("source"),
        "source_locator": record.get("source_locator"),
        "markdown_path": record.get("markdown_path"),
        "excerpt": text[:500],
    }


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Query the CHECK Expert JSONL knowledge base")
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument(
        "--type", choices=["screen", "manual", "excel", "support_case", "support_case_index"]
    )
    parser.add_argument("--category")
    parser.add_argument(
        "--case-type", choices=["faq", "procedure", "troubleshooting", "caution", "tip"]
    )
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    results = search(
        load_records(args.index),
        args.query,
        limit=max(1, args.limit),
        record_type=args.type,
        category=args.category,
        case_type=args.case_type,
    )
    compact = [compact_result(record) for record in results]
    if args.json:
        print(json.dumps({"query": args.query, "results": compact}, ensure_ascii=False, indent=2))
        return
    for record in compact:
        print(
            f"[{record['score']:.1f}] {record['title']} ({record['id']})\n"
            f"  source: {record['source']} / {record['source_locator']}\n"
            f"  path: {record['markdown_path']}\n"
        )


if __name__ == "__main__":
    main()
