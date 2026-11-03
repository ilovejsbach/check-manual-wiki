"""build_ontology_case_edges 단위 테스트. 레코드·사례 문장은 합성이며 실데이터를 복사하지 않았다."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_ontology_case_edges as bce  # noqa: E402
import build_ontology_nodes as bon  # noqa: E402
from test_derive_case_links import base_records, case  # noqa: E402

AS_OF = "2026-11-02"


def reg(tr, status, n=1):
    return {"tr": tr, "status": status, "screen_id": None, "title": None, "categories": [], "sources": [], "grade": "auto_extracted",
            "case_mentions": n, "case_ids": [], "notes": ""}


def run(cases, registry):
    recs = base_records() + cases
    return bce.compute(recs, registry, AS_OF)


def by_type(edges, typ):
    return [e for e in edges if e["type"] == typ]


def test_known_tr_becomes_about_screen_edge_without_origin_locator():
    c = case("check:support-case:a1", "TR 4101 화면에서 값이 비어 보입니다")  # case() 의 원본 위치는 20260101!row:1 로 합성
    edges, _, known, _, _ = run([c], [])
    e = next(e for e in by_type(edges, "about_screen") if e["target_id"] == "check:screen:4101")
    assert e["source_id"] == c["id"] and e["grade"] == "auto_extracted" and e["evidence"]["key_type"] == "tr"
    assert "source_locator" not in e["evidence"]
    assert "row:" not in str(edges)  # 원본 행 위치가 어떤 엣지에도 새지 않는다
    assert bce.validate_case_edges(edges, known) == []


def test_unregistered_tr_connects_to_candidate_node_and_rejected_is_skipped():
    cs = [case("check:support-case:b1", "TR 9999 화면 문의입니다"), case("check:support-case:b2", "TR 8888 화면 문의입니다"),
          case("check:support-case:b3", "TR 7777 화면 문의입니다")]
    registry = [reg("9999", "case_mentioned", 1), reg("8888", "rejected"), reg("7777", "screen_observed")]
    edges, _, known, _, _ = run(cs, registry)
    mt = by_type(edges, "mentions_tr")
    assert [(e["source_id"], e["target_id"]) for e in mt] == [("check:support-case:b1", "check:tr:9999")]
    assert not any(e["target_id"] in ("check:tr:8888", "check:screen:8888") for e in edges)  # 기각된 TR 은 잇지 않는다
    obs = next(e for e in edges if e["target_id"] == "check:screen:7777")  # 화면 관찰로 확인된 TR 은 화면으로
    assert obs["type"] == "about_screen"
    assert "check:tr:9999" in known


def test_function_and_manual_edges_are_merged_with_via_list():
    c = case("check:support-case:c1", '=CT("005930","15001") 와 =CH("","",1) 를 입력했습니다')
    edges, _, known, _, _ = run([c], [])
    uses = {e["target_id"] for e in by_type(edges, "uses_function")}
    assert {"check:func:CT", "check:func:CH"} <= uses
    em = [e for e in by_type(edges, "explained_in_manual") if e["target_id"] == "check:manual:엑셀-프리미엄:주요-함수-설명"]
    assert len(em) == 1 and set(em[0]["via"]) == {"check:func:CT", "check:func:CH"}  # 같은 엣지로 합치고 via 는 목록
    assert bce.validate_case_edges(edges, known) == []


def test_similar_to_limited_and_only_case_to_case():
    cs = [case(f"check:support-case:d{i}", "공통된 문의 내용 입니다 현재가 표시가 되지 않는 문제") for i in range(5)]
    edges, _, _, _, _ = run(cs, [])
    sim = by_type(edges, "similar_to")
    assert sim and all(e["source_id"].startswith(bce.CASE_PREFIX) and e["target_id"].startswith(bce.CASE_PREFIX) for e in sim)
    deg = {}
    for e in sim:
        for end in (e["source_id"], e["target_id"]):
            deg[end] = deg.get(end, 0) + 1
    assert max(deg.values()) <= 4  # 사례 하나의 차수 상한


def test_validate_flags_locator_leak_wrong_source_missing_node_and_bad_target():
    c = case("check:support-case:e1", "TR 4101 문의")
    edges, _, known, _, _ = run([c], [])
    good = by_type(edges, "about_screen")[0]
    leak = dict(good, id="x1", evidence=dict(good["evidence"], source_locator="20260101!row:1"))
    assert any("개인정보" in e for e in bce.validate_case_edges([leak], known))
    wrong_src = dict(good, id="x2", source_id="check:screen:4101")
    assert any("source 가 사례가 아님" in e for e in bce.validate_case_edges([wrong_src], known))
    missing = dict(good, id="x3", target_id="check:screen:0000")
    assert any("없는 노드" in e for e in bce.validate_case_edges([missing], known))
    bad_type = dict(good, id="x4", target_id="check:func:CT")
    assert any("타입 제약" in e for e in bce.validate_case_edges([bad_type], known))


def test_tr_candidate_nodes_from_registry():
    nodes = bon.build_tr_candidate_nodes([reg("9999", "case_mentioned", 1), reg("9998", "case_mentioned", 4), reg("4101", "manual_confirmed")], AS_OF)
    by = {n["id"]: n for n in nodes}
    assert set(by) == {"check:tr:9999", "check:tr:9998"}  # 매뉴얼 화면은 후보가 아니다
    assert by["check:tr:9999"]["possible_false_positive"] is True and by["check:tr:9998"]["possible_false_positive"] is False
    assert by["check:tr:9998"]["type"] == "tr_candidate" and by["check:tr:9998"]["visibility"] == "public"


def test_form_screens_only_go_to_review_queue_when_no_body_evidence():
    import build_ontology_case_edges as bce
    cases = [{"id": "check:support-case:a", "form_screens": ["4101", "9999"]}, {"id": "check:support-case:b", "form_screens": ["4101"]}]
    known = {"check:screen:4101", "check:support-case:a", "check:support-case:b"}
    rows = bce.form_screen_review_rows(cases, {"check:support-case:b"}, known, {}, [], "2026-11-03")
    assert [(r["source_id"], r["target_id"], r["review_status"], r["confident"]) for r in rows] == [
        ("check:support-case:a", "check:screen:4101", "needs_review", False)]
