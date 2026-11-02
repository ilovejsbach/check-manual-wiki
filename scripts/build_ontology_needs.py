#!/usr/bin/env python3
"""화면을 못 찾은 '화면 찾기' 사례를 정보요구 노드(gap)로 승격한다: ontology/needs.jsonl.

대상: case_classes 의 intent=screen_finding 이면서 화면/TR 엣지가 없는 사례.
시장 영역별로 묶어 노드 하나(`check:need:unresolved-<영역>`)를 만들고 gap:true 로 표시한다.
노드에는 사례 본문·제목을 넣지 않는다(사례 ID 와 영역뿐). 사람이 화면을 찾으면 resolves 엣지를 추가해 gap 을 닫는다.
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

SCREEN_EDGES = ("about_screen", "mentions_tr")
SLUG = {"채권": "bond", "주식": "stock", "선물": "futures", "옵션": "options", "외환": "fx", "ETP": "etp",
        "ELW": "elw", "펀드": "fund", "해외": "global", "경제지표": "macro", None: "general"}


def compute(classes: list[dict], edges: list[dict], as_of: str) -> list[dict]:
    linked = {e["source_id"] for e in edges if e["type"] in SCREEN_EDGES}
    groups: dict = collections.defaultdict(list)
    for c in classes:
        if c["intent"] == "screen_finding" and c["case_id"] not in linked:
            groups[c["domains"][0] if c["domains"] else None].append(c["case_id"])
    out = []
    for dom, ids in sorted(groups.items(), key=lambda kv: SLUG[kv[0]]):
        out.append({"id": f"check:need:unresolved-{SLUG[dom]}", "type": "information_need", "label": f"화면 찾기(미해결) — {dom or '영역 미상'}",
                    "domain": dom, "gap": True, "raised_by": sorted(ids), "n_cases": len(ids),
                    "grade": "auto_extracted", "review_status": "needs_review", "as_of": as_of})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--classes", type=Path, default=Path("ontology/case_classes.jsonl"))
    ap.add_argument("--edges", type=Path, default=Path("ontology/edges_cases.jsonl"))
    ap.add_argument("--out", type=Path, default=Path("ontology/needs.jsonl"))
    ap.add_argument("--as-of", default="2026-11-02")
    a = ap.parse_args(argv)
    rd = lambda p: [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    nodes = compute(rd(a.classes), rd(a.edges), a.as_of)
    a.out.write_text("".join(json.dumps(n, ensure_ascii=False) + "\n" for n in nodes), encoding="utf-8")
    print(json.dumps({"needs": len(nodes), "cases": sum(n["n_cases"] for n in nodes)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
