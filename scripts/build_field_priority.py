#!/usr/bin/env python3
"""화면 항목(screen_field)을 '먼저 채울 순서'로 정렬한 개념 단위 우선순위 목록: ontology/field_priority.jsonl.

같은 표시명(예: 현재가)은 여러 화면에 나오므로 표시명 단위(개념)로 묶는다. 한 번 정의를 채우면 모든 화면에 쓰인다.
점수 근거(모두 이미 가진 공개 데이터):
  case_mentions  표시명을 언급한 문의 사례 수 (실제 사용자가 궁금해한 정도)
  screen_cases   그 항목이 나오는 화면을 다룬 문의 사례 수 합 (중복 화면 제외)
  item_nodes     같은 이름의 엑셀 항목 노드 (함수·항목코드로 이어짐)
  screens        그 표시명이 나오는 화면 수 (한 번 채우면 여러 화면에 쓰임)
이미 조사된(researched) 항목은 done 으로 표시하고 순위에서 제외한다.
사례 본문은 출력하지 않는다(건수와 화면번호만).

사용:
  uv run --offline --no-sync python scripts/build_field_priority.py          # 쓰기
  uv run --offline --no-sync python scripts/build_field_priority.py --check  # 요약만
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

DEFAULT_KNOWLEDGE = Path("knowledge/check-expert/knowledge.jsonl")
DEFAULT_NODES = Path("ontology/nodes.jsonl")
DEFAULT_CASE_EDGES = Path("ontology/edges_cases.jsonl")
DEFAULT_OUT = Path("ontology/field_priority.jsonl")
DEFAULT_AS_OF = "2026-11-03"

CHECK_ON_SCREEN = ["단위·표시 형식(소수점·부호·색)", "값이 비었을 때의 표시", "나타나는 탭·조건", "기간·종류를 바꿨을 때 값 변화"]


BODY_SECTIONS = re.compile(r"## (?:사용자가 겪은 상황|당시 대응)\s*\n+(.+?)(?=\n## |\Z)", re.S)


def case_body(rec: dict) -> str:
    """사례의 실제 내용(제목·겪은 상황·당시 대응)만. 모든 사례에 붙는 고정 안내·검증 문구는 제외한다."""
    title = re.sub(r"^[^—]+—\s*", "", rec.get("title") or "")
    return "\n".join([title, *BODY_SECTIONS.findall(rec.get("text") or "")])


def _norm(text: str) -> str:
    return re.sub(r"\s+", "", text or "").lower()


def label_patterns(label: str) -> list[re.Pattern]:
    """'PER/EPS' 처럼 여러 이름이 붙은 표시명은 각각 찾는다. 한 글자 이름은 오탐이 커서 쓰지 않는다."""
    pats = []
    for part in re.split(r"[/,]", label):
        part = part.strip()
        if len(part) < 2 or not re.search(r"[A-Za-z가-힣]", part):  # '-1' 같은 열 머리글은 사례와 대응시킬 수 없다
            continue
        esc = re.escape(part)
        pats.append(re.compile(rf"(?<![A-Za-z0-9]){esc}(?![A-Za-z0-9])", re.I) if part.isascii() else re.compile(esc))
    return pats


def is_common_word(label: str) -> bool:
    """두 글자 이하 한글 표시명(시간·현재·선물·채권…)은 일반 문장에도 흔해 언급 수가 과대하다."""
    parts = [p.strip() for p in re.split(r"[/,]", label) if p.strip()]
    return bool(parts) and all(len(p) <= 2 and not p.isascii() for p in parts)


def compute(records: list[dict], nodes: list[dict], case_edges: list[dict], as_of: str) -> list[dict]:
    fields = [r for r in records if r.get("type") == "screen_field"]
    cases = [r for r in records if r.get("type") == "support_case"]
    bodies = [case_body(r) for r in cases]
    case_id = [r["id"] for r in cases]

    screen_case_ids: dict[str, set[str]] = collections.defaultdict(set)
    for e in case_edges:
        if e.get("type") == "about_screen":
            screen_case_ids[str(e["target_id"]).rsplit(":", 1)[-1]].add(e["source_id"])

    items_by_name: dict[str, list[dict]] = collections.defaultdict(list)
    for n in nodes:
        if n.get("type") == "item":
            items_by_name[_norm(n.get("name") or "")].append(n)

    groups: dict[str, list[dict]] = collections.defaultdict(list)
    for f in fields:
        groups[f.get("field_label") or f.get("title")].append(f)

    rows = []
    for label, fs in groups.items():
        pats = label_patterns(label)
        mentioned = {case_id[i] for i, t in enumerate(bodies) if any(p.search(t) for p in pats)} if pats else set()
        screens = sorted({str(f["screen_code"]) for f in fs if f.get("screen_code")})
        scr_cases = set().union(*(screen_case_ids.get(s, set()) for s in screens)) if screens else set()
        item_nodes = items_by_name.get(_norm(label), [])
        funcs = sorted({a["function"] for n in item_nodes for a in n.get("applies_to", []) if a.get("function")})
        done = all(f.get("review_status") == "researched" for f in fs)
        common = is_common_word(label)
        score = round((1 if common else 3) * len(mentioned) + 0.5 * min(len(scr_cases), 20) + (4 if item_nodes else 0) + 0.5 * min(len(screens), 10), 1)
        reasons = []
        if mentioned:
            reasons.append(f"문의 사례 {len(mentioned)}건이 언급" + (" (일반 단어라 과대할 수 있음, 가중치 낮춤)" if common else ""))
        if item_nodes:
            reasons.append("엑셀 항목과 이름 일치(함수·항목코드 연결 가능)")
        if len(screens) > 1:
            reasons.append(f"{len(screens)}개 화면에 공통 등장")
        if scr_cases:
            reasons.append(f"해당 화면을 다룬 문의 {len(scr_cases)}건")
        rows.append({
            "label": label, "score": score, "done": done,
            "case_mentions": len(mentioned), "screen_cases": len(scr_cases),
            "common_word": common, "screens": screens, "item_codes": sorted({n["code"] for n in item_nodes if n.get("code")})[:10],
            "functions": funcs, "field_ids": sorted(f["id"] for f in fs),
            "reasons": reasons or ["근거 신호 없음(화면에 존재만 확인)"],
            "check_on_screen": CHECK_ON_SCREEN, "as_of": as_of,
        })
    pending = sorted((r for r in rows if not r["done"]), key=lambda r: (-r["score"], r["label"]))
    for rank, r in enumerate(pending, 1):
        r["rank"] = rank
    for r in rows:
        r.setdefault("rank", None)
    return sorted(rows, key=lambda r: (r["rank"] is None, r["rank"] or 0, r["label"]))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="화면 항목 채우기 우선순위")
    ap.add_argument("--knowledge", type=Path, default=DEFAULT_KNOWLEDGE)
    ap.add_argument("--nodes", type=Path, default=DEFAULT_NODES)
    ap.add_argument("--case-edges", type=Path, default=DEFAULT_CASE_EDGES)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--as-of", default=DEFAULT_AS_OF)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    load = lambda p: [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows = compute(load(args.knowledge), load(args.nodes), load(args.case_edges), args.as_of)
    pending = [r for r in rows if not r["done"]]
    print(json.dumps({
        "concepts": len(rows), "pending": len(pending), "done": len(rows) - len(pending),
        "with_case_mentions": sum(1 for r in pending if r["case_mentions"]),
        "with_item_node": sum(1 for r in pending if r["item_codes"]),
        "no_signal": sum(1 for r in pending if r["score"] <= 0.5 * min(len(r["screens"]), 10)),
    }, ensure_ascii=False))
    if not args.check:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
