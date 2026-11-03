from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from query_check_wiki import DEFAULT_INDEX, load_records, search

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUERIES = ROOT / "scripts" / "tests" / "fixtures" / "eval_queries.jsonl"
KINDS = {"screen_code", "alias", "title", "function", "natural_language"}


def crosslink_metrics(records: list[dict[str, Any]]) -> dict[str, Any]:
    screens = {str(item.get("screen_code")): item for item in records
               if item.get("type") == "screen" and item.get("screen_code")}
    linked_mentions = total_mentions = 0
    title_candidates = []
    for code, screen in screens.items():
        title = re.sub(r"^\d{4}\s*[-–—:]?\s*", "", str(screen.get("title", ""))).strip()
        if len(title) >= 5 and title not in {"기타", "종합", "조회", "현황", "정보", "관리", "설정", "검색", "화면"}:
            title_candidates.append((title, str(screen["id"]), code))
    title_targets = [(title, target_id, code) for title, target_id, code in title_candidates
                     if sum(title == other for other, _, _ in title_candidates) == 1
                     and not any(title != other and title in other for other, _, _ in title_candidates)]
    for record in records:
        if record.get("type") != "screen":
            continue
        text = str(record.get("text") or "")
        text = re.sub(r"(?ms)^## (?:관련 화면|원문 근거)\s*\n.*?(?=^## |\Z)", "\n", text)
        # 실제 앱에서 관찰한 탭·항목 이름은 화면 UI 라벨이지 다른 화면에 대한 언급이 아니다.
        text = re.sub(r"(?ms)^### 관찰된 (?:탭|금융 항목)\s*\n.*?(?=^#{1,3} |\Z)", "\n", text)
        own = str(record.get("screen_code") or "")
        counts: dict[str, int] = {}
        tr_spans: list[tuple[int, int]] = []
        for match in re.finditer(r"(?i)\bTR\s*(\d{4})\b", text):
            code = match.group(1)
            tr_spans.append(match.span(1))
            if code in screens and code != own:
                target_id = str(screens[code]["id"])
                counts[target_id] = counts.get(target_id, 0) + 1
        for match in re.finditer(r"(?<!\d)(\d{4})(?!\d)", text):
            code = match.group(1)
            if any(start <= match.start(1) < end for start, end in tr_spans):
                continue
            suffix = text[match.end(1):]
            if re.match(r"\s*년", suffix) or re.match(r"\s*[-/.]\s*\d{1,2}(?:\D|$)", suffix):
                continue
            if code in screens and code != own:
                target_id = str(screens[code]["id"])
                counts[target_id] = counts.get(target_id, 0) + 1
        for title, target_id, code in title_targets:
            if target_id != str(record["id"]):
                count = text.count(title)
                if count:
                    counts[target_id] = counts.get(target_id, 0) + count
        total_mentions += sum(counts.values())
        linked_mentions += sum(count for target_id, count in counts.items()
                               if target_id in set(record.get("related_ids", [])))
    manuals = [item for item in records if item.get("type") == "manual"]
    manuals_without_links = [str(item["id"]) for item in manuals
                             if not any(str(target).startswith("check:screen:") for target in item.get("related_ids", []))]
    records_by_id = {str(item["id"]): item for item in manuals}
    manual_reasons = {}
    for record_id in manuals_without_links:
        item = records_by_id[record_id]
        if item.get("mapping_status") == "unmapped":
            reason = "문의 주제가 공식 화면에 매핑되지 않아 분류 대기 상태로 보존됨"
        elif item.get("source") == "CHECKPlus_Manual.pdf":
            reason = "본문에 실제 존재하는 화면번호·TR번호·구별 가능한 화면명이 없음"
        else:
            reason = "보강·안내 자료에 공식 화면을 특정할 수 있는 근거가 없음"
        manual_reasons[record_id] = reason
    edges = {(str(item["id"]), str(target)) for item in records for target in item.get("related_ids", [])}
    asymmetric = [(source, target) for source, target in edges if (target, source) not in edges]
    cases = [r for r in records if r.get("type") == "support_case"]
    # The extracted strong keys are spans from body sections (TR notation or
    # distinguishing context); case_topic labels are deliberately excluded.
    tr_cases = [r for r in cases if r.get("screen_codes")]
    unresolved_cases = [r for r in cases if r.get("tr_candidates")]
    candidate_linked = sum(any(x in set(r.get("related_ids", [])) for x in (f"check:tr:{c['code']}" for c in r.get("tr_candidates", []))) for r in unresolved_cases)
    screen_counts = [sum(1 for target in r.get("related_ids", []) if str(target).startswith("check:screen:")) for r in cases]
    placeholder_count = sum(str(target).startswith("check:enrichment:unmapped:") for r in cases for target in r.get("related_ids", []))
    pages_linked = sum("[[" in str(r.get("text", "")) for r in cases)
    return {
        "body_mentions": total_mentions,
        "linked_body_mentions": linked_mentions,
        "mention_link_rate": linked_mentions / total_mentions if total_mentions else 1.0,
        "manual_records_without_screen_links": len(manuals_without_links),
        "manual_records_total": len(manuals),
        "manual_records_without_screen_link_ids": manuals_without_links,
        "manual_records_without_screen_link_reasons": manual_reasons,
        "relationship_edges": len(edges),
        "asymmetric_relationship_edges": len(asymmetric),
        "case_tr_screen_key_rate": sum(bool(r.get("screen_codes")) for r in tr_cases) / len(tr_cases) if tr_cases else 1.0,
        "case_tr_screen_key_cases": len(tr_cases),
        "case_wiki_link_rate": pages_linked / len(cases) if cases else 1.0,
        "unregistered_tr_candidate_link_rate": candidate_linked / len(unresolved_cases) if unresolved_cases else 1.0,
        "unregistered_tr_cases": len(unresolved_cases),
        "average_case_screen_related_ids": sum(screen_counts) / len(screen_counts) if screen_counts else 0.0,
        "case_unmapped_placeholder_links": placeholder_count,
    }


def load_queries(path: Path = DEFAULT_QUERIES) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _metrics(rows: list[dict[str, Any]]) -> dict[str, float | int]:
    count = len(rows)
    if not count:
        return {"count": 0, "recall@1": 0.0, "recall@3": 0.0, "recall@5": 0.0, "mrr": 0.0}
    return {
        "count": count,
        **{
            f"recall@{k}": sum(bool(set(row["expected_ids"]) & set(row["ranked_ids"][:k])) for row in rows) / count
            for k in (1, 3, 5)
        },
        "mrr": sum(row["reciprocal_rank"] for row in rows) / count,
    }


def evaluate(
    records: list[dict[str, Any]], queries: list[dict[str, Any]]
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for query in queries:
        results = search(records, query["query"], limit=5)
        ranked_ids = [str(record["id"]) for record in results]
        rank = next((i for i, record_id in enumerate(ranked_ids, 1) if record_id in query["expected_ids"]), 0)
        row = {
            "id": query["id"],
            "query": query["query"],
            "kind": query["kind"],
            "expected_ids": query["expected_ids"],
            "ranked_ids": ranked_ids,
            "rank": rank or None,
            "reciprocal_rank": 1 / rank if rank else 0.0,
        }
        rows.append(row)
        grouped[query["kind"]].append(row)
    return {
        "metrics": _metrics(rows),
        "crosslinks": crosslink_metrics(records),
        "by_kind": {kind: _metrics(grouped[kind]) for kind in sorted(grouped)},
        "queries": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate CHECK wiki search against labeled queries")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--queries", type=Path, default=DEFAULT_QUERIES)
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args()
    report = evaluate(load_records(args.index), load_queries(args.queries))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"metrics": report["metrics"], "by_kind": report["by_kind"]}, ensure_ascii=False, indent=2))
        for row in report["queries"]:
            if row["rank"] is None or row["rank"] > 1:
                print(f"LOW {row['id']} [{row['kind']}] {row['query']}: rank={row['rank']}")


if __name__ == "__main__":
    main()
