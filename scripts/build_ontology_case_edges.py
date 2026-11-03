#!/usr/bin/env python3
"""문의 사례(support_case)의 연결을 온톨로지 엣지로 내보낸다: ontology/edges_cases.jsonl.

사례에서 본문 키(화면번호·제목·엑셀 함수·항목코드)를 추출하고(derive_case_links 재사용) 타입 있는 관계로 만든다.
  about_screen        사례 -> 화면            본문에 TR/제목 근거(auto_extracted) 또는 기존 연결 이월(inferred)
  mentions_tr         사례 -> TR 후보(check:tr:<TR>)  위키에 화면 문서가 없는 TR 을 사례가 언급 (사례 219개 / TR 172개)
  uses_function       사례 -> 함수
  involves_item       사례 -> 항목                모호하면 후보 코드 전부 ambiguous 로 표시
  explained_in_manual 사례 -> 매뉴얼 문서         함수·기능 키워드·화면 원문 쪽 규칙
  resolves            사례 -> 화면/함수            증상-조치 구조의 응답에 키가 있을 때
  similar_to          사례 <-> 사례               TF-IDF + 공유 키, 사례당 상위 2개
키 없는 사례의 검색 기반 후보는 정답이 아니라 ontology/edges_cases_review.jsonl 검수 큐로만 낸다.

개인정보: 사례 원본 위치(source_locator: 행 번호·CRM 위치)는 엣지에 넣지 않는다. 근거는 {섹션, 시작, 끝, sha8, 키 종류} 뿐이다.
표준 라이브러리만 사용한다.

사용:
  uv run --offline --no-sync python scripts/build_ontology_case_edges.py          # 쓰기
  uv run --offline --no-sync python scripts/build_ontology_case_edges.py --check  # 검증만(위반 시 종료코드 1)
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_ontology_edges as boe  # noqa: E402
import build_ontology_nodes as bon  # noqa: E402
import derive_case_links as dcl  # noqa: E402

DEFAULT_KNOWLEDGE = Path("knowledge/check-expert/knowledge.jsonl")
DEFAULT_REGISTRY = Path("ontology/tr_registry.jsonl")
DEFAULT_OUT = Path("ontology/edges_cases.jsonl")
DEFAULT_REVIEW = Path("ontology/edges_cases_review.jsonl")
DEFAULT_AS_OF = "2026-11-02"
CASE_PREFIX = "check:support-case:"
EXTRAS = ("rule", "ambiguous", "n_candidates", "legacy_link", "corroborated_by_label", "known_function", "structure", "reason", "mutual")
ALLOWED = {  # 관계 -> 허용 target 접두사 (I7)
    "about_screen": ("check:screen:",), "mentions_tr": ("check:tr:",), "uses_function": ("check:func:",),
    "involves_item": ("check:item:",), "explained_in_manual": ("check:manual:", "check:excel:"),
    "resolves": ("check:screen:", "check:func:"), "similar_to": (CASE_PREFIX,),
}


def to_edge(link: dict, as_of: str) -> dict:
    ev = {k: v for k, v in link["evidence"].items() if k != "source_locator"}  # 원본 위치 단서 제거
    e = {"id": boe.edge_id(link["from"], link["relation"], link["to"]), "source_id": link["from"], "target_id": link["to"],
         "type": link["relation"], "grade": link["grade"], "evidence": ev, "as_of": as_of, "evidence_type": "case_key",
         "review_status": link["review_status"], "confidence": link["confidence"]}
    for k in EXTRAS:
        if k in link:
            e[k] = link[k]
    vias = link.get("vias") or ([link["via"]] if link.get("via") else [])
    if vias:
        e["via"] = sorted(vias)
    if link.get("target_locator"):
        e["target_locator"] = [link["target_locator"]]
    return e


def merge_edges(edges: list[dict]) -> list[dict]:
    """같은 (source, type, target) 은 하나로 합치고 via·target_locator 는 목록으로 모은다."""
    out: dict[str, dict] = {}
    for e in edges:
        cur = out.get(e["id"])
        if cur is None:
            out[e["id"]] = e
            continue
        for k in ("via", "target_locator"):
            if k in e:
                cur[k] = sorted(set(cur.get(k, [])) | set(e[k]))
        cur["confidence"] = max(cur["confidence"], e["confidence"])
    return sorted(out.values(), key=lambda e: (e["source_id"], e["type"], e["target_id"]))


def mentions_tr_edges(keys_list: list[dict], registry: dict[str, dict], as_of: str) -> list[dict]:
    """위키에 화면 레코드가 없는 TR 의 강한 언급(tr/ctx)을 후보 TR 노드에 잇는다. 기각된 TR 은 잇지 않는다."""
    out = []
    for k in keys_list:
        for u in k["unresolved_screen_codes"]:
            row = registry.get(u["code"])
            if row is None or row["status"] == "rejected":
                continue
            target = f"check:screen:{u['code']}" if row["status"] == "screen_observed" else f"check:tr:{u['code']}"
            rel = "about_screen" if target.startswith("check:screen:") else "mentions_tr"
            out.append({"from": k["id"], "to": target, "relation": rel,
                        "evidence": {"record_id": k["id"], "section": u["section"], "start": u["start"], "end": u["end"], "key_type": u["kind"]},
                        "grade": "auto_extracted", "confidence": 0.9 if u["kind"] == "tr" else 0.85, "review_status": "candidate"})
    return out


def review_rows(cands: list[dict], as_of: str) -> list[dict]:
    rows = []
    for c in cands:
        for rank, cd in enumerate(c["candidates"], 1):
            rows.append({"source_id": c["case_id"], "target_id": cd["to"], "type": cd["relation"], "rank": rank, "score": cd["score"],
                         "confident": c["confident"] and rank == 1, "evidence_tokens": cd["evidence_tokens"],
                         "grade": "inferred", "review_status": "needs_review", "as_of": as_of})
    return rows


def form_screen_review_rows(cases: list[dict], covered: set[str], known: set[str], registry: dict[str, dict], existing: list[dict], as_of: str) -> list[dict]:
    """본문 근거가 없는 사례의 양식 화면번호(form_screens)를 검수 큐로만 낸다. 엣지(정답)로는 쓰지 않는다:
    양식 칸 번호는 문의를 접수한 화면일 뿐 질문 대상 화면과 다를 수 있다."""
    rank_of: dict[str, int] = collections.Counter(r["source_id"] for r in existing)
    seen = {(r["source_id"], r["target_id"]) for r in existing}
    rows = []
    for c in cases:
        if c["id"] in covered:
            continue
        for code in c.get("form_screens") or []:
            target = next((t for t in (f"check:screen:{code}", f"check:tr:{code}") if t in known), None)
            if target is None or (c["id"], target) in seen:
                continue
            rank_of[c["id"]] += 1
            seen.add((c["id"], target))
            rows.append({"source_id": c["id"], "target_id": target, "type": "about_screen" if target.startswith("check:screen:") else "mentions_tr",
                         "rank": rank_of[c["id"]], "score": 0.3, "confident": False, "evidence_tokens": ["form_screen"],
                         "grade": "inferred", "review_status": "needs_review", "as_of": as_of})
    return rows


def validate_case_edges(edges: list[dict], known_ids: set[str]) -> list[str]:
    errs: list[str] = []
    ids = collections.Counter(e["id"] for e in edges)
    errs += [f"I2 중복 엣지 {i}" for i, n in ids.items() if n > 1]
    for e in edges:
        if not e["source_id"].startswith(CASE_PREFIX):
            errs.append(f"I7 source 가 사례가 아님 {e['id']}")
        allowed = ALLOWED.get(e["type"])
        if allowed is None:
            errs.append(f"I7 허용되지 않은 관계 {e['type']}")
        elif not e["target_id"].startswith(allowed):
            errs.append(f"I7 타입 제약 위반 {e['type']}: {e['target_id']}")
        for end in ("source_id", "target_id"):
            if e[end] not in known_ids:
                errs.append(f"I1 {e['id']} {end} 없는 노드 {e[end]}")
        if not (e.get("grade") and e.get("as_of") and e.get("evidence", {}).get("record_id")):
            errs.append(f"I5 등급/근거/기준일 누락 {e['id']}")
        if "source_locator" in e.get("evidence", {}):
            errs.append(f"개인정보: 원본 위치(source_locator)가 엣지 근거에 있음 {e['id']}")
    return errs


def compute(records: list[dict], registry_rows: list[dict], as_of: str):
    """(엣지, 검수 큐, 실존 ID 집합, 사례 키 목록, 사례 ID 목록)."""
    registry = {r["tr"]: r for r in registry_rows}
    items, _ = bon.build_item_nodes(records, as_of)
    funcs = bon.build_function_nodes(records, as_of)
    tr_nodes = bon.build_tr_candidate_nodes(registry_rows, as_of)
    known = {r["id"] for r in records} | {n["id"] for n in items + funcs + tr_nodes}
    idx = dcl.Index(records)
    keys_list = [dcl.extract_case_keys(c, idx) for c in idx.cases]
    links = dcl.build_links(keys_list, idx, as_of)
    sim, _ = dcl.build_similar(keys_list, idx, as_of)
    tr_links = mentions_tr_edges(keys_list, registry, as_of)
    edges = merge_edges([to_edge(l, as_of) for l in links + sim + tr_links])
    # 키 없는 사례의 후보(정답 아님) -> 검수 큐
    any_screen = {l["from"] for l in links + tr_links if l["relation"] in ("about_screen", "mentions_tr")}
    no_key = {k["id"] for k in keys_list if k["id"] not in any_screen}
    scr_all: dict[str, set] = collections.defaultdict(set)
    for l in links:
        if l["relation"] == "about_screen":
            scr_all[l["from"]].add(l["to"])
    review = review_rows(dcl.build_candidates(keys_list, idx, as_of, no_key, scr_all), as_of)
    review += form_screen_review_rows(idx.cases, any_screen, known, registry, review, as_of)
    return edges, review, known, keys_list, [c["id"] for c in idx.cases]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="사례 연결 엣지 내보내기")
    ap.add_argument("--knowledge", type=Path, default=DEFAULT_KNOWLEDGE)
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--out-review", type=Path, default=DEFAULT_REVIEW)
    ap.add_argument("--as-of", default=DEFAULT_AS_OF)
    ap.add_argument("--check", action="store_true", help="파일을 쓰지 않고 검증만 한다")
    args = ap.parse_args(argv)

    records = dcl.load_records(args.knowledge)
    registry_rows = [json.loads(l) for l in args.registry.read_text(encoding="utf-8").splitlines() if l.strip()] if args.registry.exists() else []
    edges, review, known, keys_list, cases = compute(records, registry_rows, args.as_of)
    errs = validate_case_edges(edges, known)
    with_screen = {e["source_id"] for e in edges if e["type"] == "about_screen"}
    with_tr = {e["source_id"] for e in edges if e["type"] in ("about_screen", "mentions_tr")}
    strong_tr_cases = {k["id"] for k in keys_list if any(f["kind"] != "bare" for f in k["screen_codes"]) or k["unresolved_screen_codes"]}
    print(json.dumps({
        "edges": len(edges), "by_type": dict(collections.Counter(e["type"] for e in edges)),
        "cases": len(cases), "cases_with_screen_edge": len(with_screen), "cases_with_any_tr_edge": len(with_tr),
        "cases_with_explicit_tr": len(strong_tr_cases), "explicit_tr_cases_linked": len(strong_tr_cases & with_tr),
        "cases_mentioning_unregistered_tr": sum(1 for k in keys_list if k["unresolved_screen_codes"]),
        "tr_candidate_targets": len({e["target_id"] for e in edges if e["type"] == "mentions_tr"}),
        "review_rows": len(review), "violations": len(errs)}, ensure_ascii=False))
    for e in errs[:20]:
        print("위반:", e, file=sys.stderr)
    if errs:
        return 1
    if not args.check:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in edges), encoding="utf-8")
        args.out_review.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in review), encoding="utf-8")
        print(f"wrote {args.out} ({args.out.stat().st_size // 1024} KB), {args.out_review}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
