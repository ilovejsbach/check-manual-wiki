import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build_field_priority import case_body, compute, is_common_word, label_patterns


def _field(label, screen, status="candidate"):
    return {"id": f"check:field:{screen}:{label}", "type": "screen_field", "field_label": label,
            "title": label, "screen_code": screen, "review_status": status}


def _case(cid, situation, boiler="기관 식별정보"):
    return {"id": cid, "type": "support_case", "title": "문의 — x",
            "text": f"## 사용자가 겪은 상황\n\n{situation}\n\n## 검증할 사항\n\n- {boiler}\n"}


def test_boilerplate_is_not_counted_and_body_is():
    assert "기관" not in case_body(_case("c", "현재가가 안 보여요"))
    rows = compute([_field("기관", "1"), _field("현재가", "1"), _case("c1", "현재가가 안 보여요")], [], [], "d")
    by = {r["label"]: r for r in rows}
    assert by["기관"]["case_mentions"] == 0 and by["현재가"]["case_mentions"] == 1


def test_ascii_label_needs_word_boundary_and_slash_labels_split():
    assert not any(p.search("PERCENT") for p in label_patterns("PER"))
    assert any(p.search("EPS 확인") for p in label_patterns("PER/EPS"))
    assert label_patterns("가") == []


def test_common_word_is_dampened_and_done_is_excluded_from_rank():
    assert is_common_word("시간") and not is_common_word("현재가") and not is_common_word("PER")
    rows = compute([_field("시간", "1"), _field("현재가", "1"), _field("PER", "1", "researched"),
                    _case("c1", "시간 현재가")], [], [], "d")
    by = {r["label"]: r for r in rows}
    assert by["시간"]["score"] < by["현재가"]["score"]
    assert by["PER"]["done"] and by["PER"]["rank"] is None
    assert [r["label"] for r in rows if r["rank"]] == ["현재가", "시간"]


def test_item_node_and_cross_screen_reuse_raise_score():
    nodes = [{"type": "item", "name": "현재가", "code": "15001", "applies_to": [{"function": "CT"}]}]
    rows = compute([_field("현재가", "1"), _field("현재가", "2"), _field("고가", "1")], nodes, [], "d")
    by = {r["label"]: r for r in rows}
    assert by["현재가"]["item_codes"] == ["15001"] and by["현재가"]["functions"] == ["CT"]
    assert by["현재가"]["score"] > by["고가"]["score"] and by["현재가"]["screens"] == ["1", "2"]


def test_symbol_only_labels_are_not_matched():
    assert label_patterns("-1") == [] and label_patterns("0") == []
