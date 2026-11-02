#!/usr/bin/env python3
"""온톨로지 탐색 페이지 데이터를 만든다: content/check-expert/ontology-explorer/data.json (+ index.html 은 정적 파일).

화면·항목·함수·사례·TR 후보가 어떻게 이어지는지 브라우저에서 따라가 보게 하는 읽기 전용 뷰다.
사례는 본문·제목 없이 (해시 8자, 의도, 영역, 위키 페이지 링크)만 싣는다. 새 공개 산출물에 원문을 더 싣지 않기 위해서다.
주의: build_check_wiki.py 가 content/check-expert/ 안의 생성물이 아닌 파일을 지우므로, 위키를 다시 만든 뒤에 이 스크립트를 실행한다.
페이지 템플릿은 scripts/templates/ontology_explorer.html 이고 이 스크립트가 index.html 로 복사한다.
입력: knowledge.jsonl, ontology/{nodes,edges,edges_cases,case_classes,needs}.jsonl
"""
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

OUT_DIR = Path("content/check-expert/ontology-explorer")
TEMPLATE = Path(__file__).resolve().parent / "templates" / "ontology_explorer.html"
ROOT_PREFIX = "check-expert/"


def rd(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def slug_segment(seg: str) -> str:
    """Quartz 가 파일명 조각을 URL 로 바꾸는 규칙(공백→-, &→-and-, %→-percent, ?·# 제거) + 소문자화."""
    seg = re.sub(r"\s", "-", seg).replace("&", "-and-").replace("%", "-percent").replace("?", "").replace("#", "")
    return seg.lower()


def page(md_path: str) -> str:
    """knowledge 의 markdown_path -> 탐색 페이지(check-expert/ontology-explorer/)에서의 상대 링크."""
    rel = md_path[len(ROOT_PREFIX):] if md_path.startswith(ROOT_PREFIX) else md_path
    if rel.endswith(".md"):
        rel = rel[:-3]
    return "../" + "/".join(slug_segment(x) for x in rel.split("/")) + ".html"


def build(knowledge: Path, ont: Path) -> dict:
    recs = rd(knowledge)
    nodes, edges = rd(ont / "nodes.jsonl"), rd(ont / "edges.jsonl")
    cedges, classes, needs = rd(ont / "edges_cases.jsonl"), {c["case_id"]: c for c in rd(ont / "case_classes.jsonl")}, rd(ont / "needs.jsonl")
    screens = {r["id"]: r for r in recs if r["type"] == "screen"}
    cases = {r["id"]: r for r in recs if r["type"] == "support_case"}

    funcs = {n["name"]: {"sig": n.get("signature"), "scope": n.get("scope"), "cases": n.get("case_mentions", 0)} for n in nodes if n["id"].startswith("check:func:")}
    items = {}
    for n in nodes:
        if n["id"].startswith("check:item:"):
            items[n["code"]] = {"n": n["name"], "k": n["value_kind"], "f": sorted({a["function"] for a in n["applies_to"]}),
                                "m": sorted({a["market"] for a in n["applies_to"]})[:3], "s": []}
    scr = {}
    for sid, r in screens.items():
        scr[r["screen_code"] or sid] = {"t": r["title"], "p": page(r["markdown_path"]), "it": [], "ca": []}
    for e in edges:
        if e["type"] in ("provides", "mentions_title") and e["source_id"].startswith("check:screen:"):
            code, tr = e["target_id"].split(":")[-1], e["source_id"].split(":")[-1]
            if tr in scr and code in items:
                scr[tr]["it"].append([code, "P" if e["type"] == "provides" else "M"])
                items[code]["s"].append(tr)
    tr_nodes = {n["screen_code"]: {"mentions": n.get("case_mentions", 0), "fp": bool(n.get("possible_false_positive")), "ca": []} for n in nodes if n["id"].startswith("check:tr:")}
    case_out, idx = [], {}
    links = collections.defaultdict(lambda: {"scr": set(), "tr": set(), "fn": set()})
    for e in cedges:
        s, t = e["source_id"], e["target_id"]
        if e["type"] == "about_screen":
            links[s]["scr"].add(t.split(":")[-1])
        elif e["type"] == "mentions_tr":
            links[s]["tr"].add(t.split(":")[-1])
        elif e["type"] == "uses_function":
            links[s]["fn"].add(t.split(":")[-1])
    for cid in sorted(cases):
        cl, lk = classes.get(cid, {}), links.get(cid, {"scr": set(), "tr": set(), "fn": set()})
        idx[cid] = len(case_out)
        case_out.append({"h": cid.split(":")[-1][:8], "i": cl.get("intent"), "d": cl.get("domains", []), "p": page(cases[cid]["markdown_path"]),
                         "s": sorted(lk["scr"]), "r": sorted(lk["tr"]), "f": sorted(lk["fn"])})
        for t in lk["scr"]:
            if t in scr:
                scr[t]["ca"].append(idx[cid])
        for t in lk["tr"]:
            if t in tr_nodes:
                tr_nodes[t]["ca"].append(idx[cid])
    gaps = [{"label": n["label"], "ca": [idx[c] for c in n["raised_by"] if c in idx]} for n in needs]
    return {"funcs": funcs, "items": items, "screens": scr, "tr": tr_nodes, "cases": case_out, "gaps": gaps,
            "stats": {"items": len(items), "screens": len(scr), "cases": len(case_out), "tr_candidates": len(tr_nodes), "funcs": len(funcs)}}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--knowledge", type=Path, default=Path("knowledge/check-expert/knowledge.jsonl"))
    ap.add_argument("--ontology", type=Path, default=Path("ontology"))
    ap.add_argument("--out", type=Path, default=OUT_DIR / "data.json")
    a = ap.parse_args(argv)
    data = build(a.knowledge, a.ontology)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (a.out.parent / "index.html").write_text(TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")
    print(json.dumps(data["stats"], ensure_ascii=False), f"{a.out.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
