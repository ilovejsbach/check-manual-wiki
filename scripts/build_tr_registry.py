#!/usr/bin/env python3
"""TR(화면번호) 마스터 목록 ontology/tr_registry.jsonl 을 만든다.

명세: docs/check-ontology-spec.md 15절. 한 줄 = TR 하나.
- 매뉴얼에 화면 레코드가 있는 TR      -> status manual_confirmed
- 사례 본문에서만 언급되는 TR        -> status case_mentioned (미확인 후보)
- 이미 승격/기각된 TR(screen_observed, conflict, retired, rejected)은 다시 만들지 않고 보존한다.
  윈도우 PC 화면 관찰 결과로 사람이 승격한 상태가 재생성으로 사라지면 안 되기 때문이다.

사용:
  uv run --offline --no-sync python scripts/build_tr_registry.py            # 파일 쓰기
  uv run --offline --no-sync python scripts/build_tr_registry.py --check    # 쓰지 않고 검증만(위반 시 종료코드 1)
표준 라이브러리만 사용한다(사례 키 추출은 derive_case_links 재사용).
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import derive_case_links as dcl  # noqa: E402

DEFAULT_KNOWLEDGE = Path("knowledge/check-expert/knowledge.jsonl")
DEFAULT_OUT = Path("ontology/tr_registry.jsonl")
DEFAULT_AS_OF = "2026-11-02"
PROMOTED = {"screen_observed", "conflict", "retired", "rejected"}  # 사람이 정한 상태: 재생성이 덮어쓰지 않는다
MAX_CASE_IDS = 5  # 추적용 사례 ID 상한(사례 본문은 담지 않는다)
ONCE_NOTE = "1회 언급: 연도·금액 등 4자리 숫자 오탐 가능. 화면 관찰 전에 오탐 여부부터 판정"


def screen_rows(records: list[dict], as_of: str) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for r in records:
        if r.get("type") != "screen" or not r.get("screen_code"):
            continue
        tr = str(r["screen_code"])
        title = re.sub(r"^\s*\d{4}\s*-\s*", "", r.get("title") or "")
        rows[tr] = {
            "tr": tr, "status": "manual_confirmed", "screen_id": r["id"], "title": title,
            "categories": r.get("categories") or ([r["category"]] if r.get("category") else []),
            "sources": [{"kind": "manual", "ref": r.get("source_locator"), "as_of": as_of}],
            "grade": "manual_confirmed", "case_mentions": 0, "case_ids": [], "notes": "",
        }
    return rows


def count_mentions(records: list[dict]) -> tuple[dict[str, set[str]], dict[str, set[str]], dict[str, collections.Counter]]:
    """사례별 키를 추출해 (등록 TR 언급, 미등록 TR 언급, 미등록 TR의 언급 방식) 을 모은다. 약한 번호(bare)는 제외."""
    idx = dcl.Index(records)
    known: dict[str, set[str]] = collections.defaultdict(set)
    unknown: dict[str, set[str]] = collections.defaultdict(set)
    kinds: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for case in idx.cases:
        keys = dcl.extract_case_keys(case, idx)
        for f in keys["screen_codes"]:
            if f["kind"] != "bare":
                known[f["code"]].add(case["id"])
        for u in keys["unresolved_screen_codes"]:
            unknown[u["code"]].add(case["id"])
            kinds[u["code"]][u["kind"]] += 1
    return known, unknown, kinds


def build_registry(records: list[dict], existing: list[dict], as_of: str) -> list[dict]:
    rows = screen_rows(records, as_of)
    known, unknown, kinds = count_mentions(records)
    for tr, ids in known.items():
        if tr in rows:
            rows[tr]["case_mentions"] = len(ids)
            rows[tr]["case_ids"] = sorted(ids)[:MAX_CASE_IDS]
    for tr, ids in unknown.items():
        if tr in rows:
            continue
        kind_txt = ", ".join(f"{k} {n}" for k, n in sorted(kinds[tr].items()))
        note = f"언급 방식: {kind_txt}"
        if len(ids) == 1:
            note += "; " + ONCE_NOTE
        rows[tr] = {"tr": tr, "status": "case_mentioned", "screen_id": None, "title": None, "categories": [],
                    "sources": [{"kind": "case", "ref": f"{len(ids)}개 사례", "as_of": as_of}],
                    "grade": "auto_extracted", "case_mentions": len(ids), "case_ids": sorted(ids)[:MAX_CASE_IDS], "notes": note}
    # 사람이 승격·기각한 상태는 보존(언급 수만 갱신)
    for old in existing:
        if old.get("status") in PROMOTED:
            cur = rows.get(old["tr"], {})
            merged = {**old}
            if "case_mentions" in cur:
                merged["case_mentions"], merged["case_ids"] = cur["case_mentions"], cur["case_ids"]
            if old["status"] == "screen_observed" and cur.get("screen_id"):
                merged["screen_id"] = cur["screen_id"]  # 이후 매뉴얼 화면 레코드가 생기면 연결만 갱신
            rows[old["tr"]] = merged
    manual = sorted((r for r in rows.values() if r["status"] == "manual_confirmed"), key=lambda r: r["tr"])
    rest = sorted((r for r in rows.values() if r["status"] != "manual_confirmed"),
                  key=lambda r: (-r.get("case_mentions", 0), r["tr"]))
    return manual + rest


def validate_registry(rows: list[dict], records: list[dict]) -> list[str]:
    """명세 I11(TR 마스터 유일성), I12(미확인 TR 격리) 검사. 위반 메시지 목록(비어 있으면 통과)."""
    errs: list[str] = []
    seen = collections.Counter(r["tr"] for r in rows)
    errs += [f"I11 중복 TR {tr}" for tr, n in seen.items() if n > 1]
    for r in rows:
        if not re.fullmatch(r"\d{4}", str(r["tr"])):
            errs.append(f"I11 TR 형식 오류 {r['tr']}")
    screens = collections.defaultdict(list)
    for rec in records:
        if rec.get("type") == "screen" and rec.get("screen_code"):
            screens[str(rec["screen_code"])].append(rec["id"])
    reg = {r["tr"]: r for r in rows}
    for tr, ids in screens.items():
        if len(ids) != 1:
            errs.append(f"I11 같은 TR의 화면 레코드가 {len(ids)}개: {tr}")
        if tr not in reg:
            errs.append(f"I11 마스터에 없는 화면 레코드: {tr}")
    screen_ids = {i for v in screens.values() for i in v}
    for r in rows:
        if r["status"] == "manual_confirmed" and r.get("screen_id") not in screen_ids:
            errs.append(f"I11 manual_confirmed 인데 화면 레코드 없음: {r['tr']}")
        if r["status"] == "case_mentioned" and (r.get("screen_id") or r["tr"] in screens):
            errs.append(f"I12 case_mentioned 인데 화면 레코드가 있음(승격 필요): {r['tr']}")
    return errs


def load_existing(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="TR 마스터 목록 생성/검증")
    ap.add_argument("--knowledge", type=Path, default=DEFAULT_KNOWLEDGE)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--as-of", default=DEFAULT_AS_OF)
    ap.add_argument("--check", action="store_true", help="파일을 쓰지 않고 검증만 한다")
    args = ap.parse_args(argv)

    records = dcl.load_records(args.knowledge)
    rows = build_registry(records, load_existing(args.out), args.as_of)
    errs = validate_registry(rows, records)
    stat = collections.Counter(r["status"] for r in rows)
    print(json.dumps({"rows": len(rows), "by_status": dict(stat),
                      "case_mentioned_once": sum(1 for r in rows if r["status"] == "case_mentioned" and r["case_mentions"] == 1),
                      "violations": len(errs)}, ensure_ascii=False))
    for e in errs[:20]:
        print("위반:", e, file=sys.stderr)
    if errs:
        return 1
    if not args.check:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
