#!/usr/bin/env python3
"""온톨로지 엣지를 ontology/edges.jsonl 로 내보낸다.

명세: docs/check-ontology-spec.md 3(관계), 4(등급), 6(엣지 형식), 10(불변식 I1·I5·I7).
- available_via (item -> function): 항목코드표 시트가 근거라 manual_confirmed. 결정적이다.
- provides / mentions_title (screen -> item): 화면 본문·소제목과 항목명의 텍스트 일치(derive_item_links)라 auto_extracted.
  * 소제목에서 정확/정규화 일치하고 모호하지 않은 것만 provides 후보(canonical:false, review_status:candidate).
  * 그 밖의 비모호 일치는 '언급'일 뿐이라 mentions_title 로 낸다(화면이 그 항목을 보여 준다고 단정하지 않는다).
  * 같은 항목명이 여러 코드에 해당하는 모호한 일치는 엣지로 만들지 않고 ontology/edges_ambiguous.jsonl 검수 큐로 분리한다.
표준 라이브러리만 사용한다.

사용:
  uv run --offline --no-sync python scripts/build_ontology_edges.py            # edges.jsonl, edges_ambiguous.jsonl 쓰기
  uv run --offline --no-sync python scripts/build_ontology_edges.py --check    # 쓰지 않고 검증만(위반 시 종료코드 1)
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_ontology_nodes as bon  # noqa: E402
import derive_case_links as dcl  # noqa: E402
import derive_item_links as dil  # noqa: E402

DEFAULT_KNOWLEDGE = Path("knowledge/check-expert/knowledge.jsonl")
DEFAULT_OUT = Path("ontology/edges.jsonl")
DEFAULT_AMBIGUOUS = Path("ontology/edges_ambiguous.jsonl")
DEFAULT_AS_OF = "2026-11-02"
PROVIDES_MATCH_TYPES = {"exact", "normalized"}
DICT_RECORD_PREFIX = "check:excel:항목코드표:"
ALLOWED = {  # I7 타입 제약: 관계 -> (source 타입 접두, target 타입 접두)
    "available_via": ("check:item:", "check:func:"),
    "provides": ("check:screen:", "check:item:"),
    "mentions_title": ("check:screen:", "check:item:"),
}


def edge_id(src: str, typ: str, tgt: str) -> str:
    return "check:edge:" + hashlib.sha1(f"{src}|{typ}|{tgt}".encode("utf-8")).hexdigest()[:12]


def available_via_edges(item_nodes: list[dict], as_of: str) -> list[dict]:
    out = []
    for n in item_nodes:
        locs = n["source_locator"].split("; ")
        for fn in sorted({a["function"] for a in n["applies_to"]}):
            sheet = [loc for loc in locs if loc.split(":")[0] == fn] or locs  # 해당 함수 시트의 청크, 없으면 전체
            out.append({
                "id": edge_id(n["id"], "available_via", f"check:func:{fn}"),
                "source_id": n["id"], "target_id": f"check:func:{fn}", "type": "available_via",
                "label": "가져올 수 있는 함수", "grade": "manual_confirmed",
                "evidence": {"record_id": DICT_RECORD_PREFIX + sheet[0], "source_locator": "; ".join(sheet)},
                "as_of": as_of, "evidence_type": "code_table_row", "review_status": "documented",
            })
    return out


def screen_item_edges(records: list[dict], as_of: str) -> tuple[list[dict], list[dict]]:
    """(엣지, 모호 후보 검수 큐) 를 돌려준다."""
    d = dil.ItemDict(dil.parse_dictionary(records))
    screens = [r for r in records if r.get("type") == "screen"]
    loc = {s["id"]: s.get("source_locator") for s in screens}
    pairs: dict[tuple[str, str], dict] = {}
    queue: list[dict] = []
    for l in dil.derive_links(screens, d):
        if l["ambiguous"]:
            queue.append({"source_id": l["screen_id"], "item_text": l["item_text"], "n_codes": l["n_codes"],
                          "candidate_codes": sorted(m["code"] for m in l["matched_codes"]),
                          "match_type": l["match_type"], "section": l["source"], "confidence": l["confidence"],
                          "review_status": "needs_review", "as_of": as_of})
            continue
        code = l["matched_codes"][0]["code"]
        key = (l["screen_id"], code)
        strong = l["source"] == "heading" and l["match_type"] in PROVIDES_MATCH_TYPES
        cur = pairs.get(key)
        if cur is None:
            cur = pairs[key] = {"provides": False, "conf": 0.0, "texts": set(), "sections": set(), "types": set()}
        cur["provides"] = cur["provides"] or strong
        cur["conf"] = max(cur["conf"], l["confidence"])
        cur["texts"].add(l["item_text"])
        cur["sections"].add(l["source"])
        cur["types"].add(l["match_type"])
    edges = []
    for (sid, code), v in sorted(pairs.items()):
        typ = "provides" if v["provides"] else "mentions_title"
        e = {
            "id": edge_id(sid, typ, f"check:item:{code}"),
            "source_id": sid, "target_id": f"check:item:{code}", "type": typ,
            "label": "화면 소제목의 항목" if typ == "provides" else "본문에서 언급한 항목",
            "grade": "auto_extracted",
            "evidence": {"record_id": sid, "source_locator": loc.get(sid), "matched_text": sorted(v["texts"])[0],
                         "sections": sorted(v["sections"]), "match_types": sorted(v["types"]), "confidence": v["conf"]},
            "as_of": as_of, "evidence_type": "text_match", "review_status": "candidate",
        }
        if typ == "provides":
            e["canonical"] = False  # 명세 4절: 자동추출은 검수 전 provides 정본이 될 수 없다
        edges.append(e)
    return edges, sorted(queue, key=lambda q: (q["source_id"], q["item_text"]))


def validate_edges(edges: list[dict], node_ids: set[str], screen_ids: set[str]) -> list[str]:
    errs: list[str] = []
    ids = collections.Counter(e["id"] for e in edges)
    errs += [f"I2 중복 엣지 {i}" for i, n in ids.items() if n > 1]
    known = node_ids | screen_ids
    for e in edges:
        for end in ("source_id", "target_id"):
            if e[end] not in known:
                errs.append(f"I1 {e['id']} {end} 없는 노드 {e[end]}")
        src_p, tgt_p = ALLOWED.get(e["type"], (None, None))
        if src_p is None:
            errs.append(f"I7 허용되지 않은 관계 {e['type']}")
        elif not (e["source_id"].startswith(src_p) and e["target_id"].startswith(tgt_p)):
            errs.append(f"I7 타입 제약 위반 {e['type']}: {e['source_id']} -> {e['target_id']}")
        if not (e.get("grade") and e.get("as_of") and e.get("evidence", {}).get("record_id")):
            errs.append(f"I5 등급/근거/기준일 누락 {e['id']}")
        if e["type"] == "provides" and e["grade"] == "auto_extracted" and e.get("canonical") is not False:
            errs.append(f"I5 자동추출 provides 가 정본으로 표시됨 {e['id']}")
    return errs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="온톨로지 엣지 내보내기")
    ap.add_argument("--knowledge", type=Path, default=DEFAULT_KNOWLEDGE)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--out-ambiguous", type=Path, default=DEFAULT_AMBIGUOUS)
    ap.add_argument("--as-of", default=DEFAULT_AS_OF)
    ap.add_argument("--check", action="store_true", help="파일을 쓰지 않고 검증만 한다")
    args = ap.parse_args(argv)

    records = dcl.load_records(args.knowledge)
    items, _ = bon.build_item_nodes(records, args.as_of)
    funcs = bon.build_function_nodes(records, args.as_of)
    node_ids = {n["id"] for n in items + funcs}
    screen_ids = {r["id"] for r in records if r.get("type") == "screen"}

    edges = available_via_edges(items, args.as_of)
    scr_edges, queue = screen_item_edges(records, args.as_of)
    edges += scr_edges
    errs = validate_edges(edges, node_ids, screen_ids)

    by_type = collections.Counter(e["type"] for e in edges)
    sc = [e for e in edges if e["type"] in ("provides", "mentions_title")]
    print(json.dumps({
        "edges": len(edges), "by_type": dict(by_type),
        "screens_with_item_edge": len({e["source_id"] for e in sc}), "screens_total": len(screen_ids),
        "items_with_screen_edge": len({e["target_id"] for e in sc}), "items_total": len(items),
        "items_without_function": len({n["id"] for n in items} - {e["source_id"] for e in edges if e["type"] == "available_via"}),
        "ambiguous_queue": len(queue), "violations": len(errs)}, ensure_ascii=False))
    for e in errs[:20]:
        print("위반:", e, file=sys.stderr)
    if errs:
        return 1
    if not args.check:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in edges), encoding="utf-8")
        args.out_ambiguous.write_text("".join(json.dumps(q, ensure_ascii=False) + "\n" for q in queue), encoding="utf-8")
        print(f"wrote {args.out} ({args.out.stat().st_size // 1024} KB), {args.out_ambiguous}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
