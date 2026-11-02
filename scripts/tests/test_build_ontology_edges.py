"""build_ontology_edges 단위 테스트. 레코드와 화면 본문은 합성이며 실데이터를 복사하지 않았다."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_ontology_edges as boe  # noqa: E402
import build_ontology_nodes as bon  # noqa: E402
from test_derive_case_links import rec  # noqa: E402

AS_OF = "2026-11-02"
DICT = "\n".join([
    "| 함수 | 시장 | 카테고리 | 항목코드 | 항목명 |", "| --- | --- | --- | --- | --- |",
    "| CT | 주식 | 시세 | 15001 | 현재가 |", "| CH | 주식 | 시세 | 15001 | 현재가 |",
    "| CT | 주식 | 시세 | 15015 | 거래량 |", "| CT | 주식 | 시세 | 14501 | 매도호가1 |",
    "| CT | 주식 | 시세 | 4018 | 괴리율 |", "| CT | 선물 | 시세 | 4019 | 괴리율 |",
])
SCREEN_A = ("# 4101 - 현재가 종합표\n\n### 화면 항목 1. 현재가\n주식의 가격을 보여 줍니다.\n\n"
            "### 화면 항목 2. 조회 기간을 설정합니다\n거래량 추이를 함께 볼 수 있습니다.\n")
SCREEN_B = "# 4102 - 괴리 화면\n\n### 화면 항목 1. 괴리율\n괴리율을 표시합니다.\n"


def records():
    return [
        rec("check:screen:4101", "screen", "4101 - 현재가 종합표", SCREEN_A, code="4101", loc="100-101"),
        rec("check:screen:4102", "screen", "4102 - 괴리 화면", SCREEN_B, code="4102", loc="102-102"),
        rec("check:excel:항목코드표:CT:001", "excel", "항목코드표", DICT, source=bon.DICT_SOURCE),
        rec(bon.FUNC_DOC_ID, "manual", "주요 함수 설명", "".join(f"## {n}\n=" + n + '("a")\n' for n in bon.FUNC_FACTS)),
    ]


def build():
    recs = records()
    items, _ = bon.build_item_nodes(recs, AS_OF)
    edges = boe.available_via_edges(items, AS_OF)
    scr, queue = boe.screen_item_edges(recs, AS_OF)
    return recs, items, edges + scr, queue


def test_available_via_one_edge_per_item_function_with_code_table_evidence():
    _, items, edges, _ = build()
    av = [e for e in edges if e["type"] == "available_via"]
    pairs = {(e["source_id"], e["target_id"]) for e in av}
    assert ("check:item:15001", "check:func:CT") in pairs and ("check:item:15001", "check:func:CH") in pairs
    assert len(av) == len(pairs) == 6  # 15001(CT,CH) + 15015 + 14501 + 4018 + 4019
    e = next(e for e in av if e["target_id"] == "check:func:CH")
    assert e["grade"] == "manual_confirmed" and e["evidence"]["record_id"] == "check:excel:항목코드표:CT:001"


def test_heading_match_is_provides_candidate_not_canonical():
    _, _, edges, _ = build()
    e = next(e for e in edges if e["type"] == "provides" and e["target_id"] == "check:item:15001")
    assert e["source_id"] == "check:screen:4101" and e["grade"] == "auto_extracted"
    assert e["canonical"] is False and e["review_status"] == "candidate"
    assert e["evidence"]["source_locator"] == "100-101" and e["evidence"]["matched_text"] == "현재가"


def test_body_only_match_is_mentions_title_not_provides():
    _, _, edges, _ = build()
    types = {(e["target_id"], e["type"]) for e in edges if e["source_id"] == "check:screen:4101"}
    assert ("check:item:15015", "mentions_title") in types and ("check:item:15015", "provides") not in types
    assert not any(e.get("canonical") for e in edges if e["type"] == "mentions_title")


def test_ambiguous_name_goes_to_review_queue_without_edge():
    _, _, edges, queue = build()
    assert not any(e["source_id"] == "check:screen:4102" and e["target_id"].startswith("check:item:") for e in edges)
    q = [x for x in queue if x["source_id"] == "check:screen:4102"]
    assert q and q[0]["candidate_codes"] == ["4018", "4019"] and q[0]["review_status"] == "needs_review"


def test_edges_are_deterministic_and_valid():
    recs, items, edges, _ = build()
    _, _, edges2, _ = build()
    assert [e["id"] for e in edges] == [e["id"] for e in edges2]
    funcs = bon.build_function_nodes(recs, AS_OF)
    node_ids = {n["id"] for n in items + funcs}
    assert boe.validate_edges(edges, node_ids, {"check:screen:4101", "check:screen:4102"}) == []


def test_validate_catches_missing_node_wrong_types_and_canonical_auto():
    recs, items, edges, _ = build()
    node_ids = {n["id"] for n in items + bon.build_function_nodes(recs, AS_OF)}
    screens = {"check:screen:4101", "check:screen:4102"}
    bad_node = dict(edges[0], id="x1", target_id="check:func:ZZZ")
    assert any("없는 노드" in e for e in boe.validate_edges([bad_node], node_ids, screens))
    bad_type = dict(edges[0], id="x2", source_id="check:func:CT", target_id="check:item:15001")
    assert any("타입 제약" in e for e in boe.validate_edges([bad_type], node_ids, screens))
    prov = next(e for e in edges if e["type"] == "provides")
    assert any("정본" in e for e in boe.validate_edges([dict(prov, canonical=True)], node_ids, screens))
    assert any("누락" in e for e in boe.validate_edges([dict(prov, as_of=None)], node_ids, screens))
