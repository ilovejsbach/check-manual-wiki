"""derive_item_links 단위 테스트 (합성 데이터)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import derive_item_links as D  # noqa: E402

TABLE = """# 항목코드표 - CH (1)

| 함수 | 시장(대분류 개념) | 카테고리 | 항목코드 | 항목명 |
| --- | --- | --- | --- | --- |
| CH | 상품 | 상품 | 15001 | 현재가 |
| CT | 주식 | 시세 | 15001 | 현재가 |
| CH | 상품 | 상품 | 14501 | 매도호가1 |
| CH | 상품 | 상품 | 14502 | 매도호가2 |
| CH | 상품 | 상품 | 15004 | 등락율 |
| CH | 상품 | 상품 | 14763 | 중간호가((매수호가+매도호가)/2) |
| CT | 주식 | 시세 | 90001 | 구분 |
| CT | 주식 | 시세 | 90002 | 수익률 |
| CT | 주식 | 시세 | 90003 | 수익률(KIS) |
| CT | 주식 | 시세 | 90004 | 체결량 |
| CT | 주식 | 시세 | 90005 | 가나|다 |
"""


def make_dict() -> D.ItemDict:
    recs = [
        {"type": "excel", "source": D.DICT_SOURCE, "text": TABLE},
        {"type": "excel", "source": "other.xlsx", "text": "| CH | a | b | 1 | 무시 |"},
        {"type": "screen", "id": "s", "text": "현재가"},
    ]
    return D.ItemDict(D.parse_dictionary(recs))


def test_parse_dictionary_skips_header_other_sources_and_handles_pipe_in_name():
    rows = D.parse_dictionary([
        {"type": "excel", "source": D.DICT_SOURCE, "text": TABLE},
        {"type": "excel", "source": "other.xlsx", "text": TABLE},
    ])
    assert len(rows) == 11
    assert rows[0] == {"function": "CH", "market": "상품", "category": "상품",
                       "code": "15001", "name": "현재가"}
    assert rows[-1]["name"] == "가나|다"


def test_dictionary_merges_same_code_across_functions():
    d = make_dict()
    e = d.by_full["현재가"]
    assert len(e) == 1
    assert e[0]["function"] == {"CH", "CT"}
    assert d.n_codes == 10


def test_normalization_whitespace_paren_digit_and_ryul():
    assert D.norm_full(" 등락 률 ") == "등락율"
    assert D.norm_full("고가수익률*") == "고가수익율"
    assert D.norm_base("매도호가1") == "매도호가"
    assert D.norm_base("중간호가((매수호가+매도호가)/2)") == "중간호가"
    assert D.norm_base("수익률(KIS)") == "수익율"


def test_exact_and_variant_spelling_match():
    d = make_dict()
    m = D.match_candidate("등락률", "body", d)
    assert m["match_type"] == "exact"
    assert [c["code"] for c in m["matched_codes"]] == ["15004"]
    assert not m["ambiguous"]
    assert m["matched_codes"][0]["function"] == ["CH"]


def test_numeric_suffix_maps_to_all_codes_and_marked_ambiguous():
    d = make_dict()
    m = D.match_candidate("매도호가", "heading", d)
    assert m["match_type"] == "normalized"
    assert {c["code"] for c in m["matched_codes"]} == {"14501", "14502"}
    assert m["ambiguous"] and m["n_codes"] == 2
    exact = D.match_candidate("매도호가1", "heading", d)
    assert exact["match_type"] == "exact" and not exact["ambiguous"]
    assert exact["confidence"] > m["confidence"]


def test_generic_and_too_short_candidates_excluded():
    d = make_dict()
    assert not D.candidate_ok("구분")
    assert not D.candidate_ok("가")
    assert not D.candidate_ok("123")
    assert D.match_candidate("구분", "heading", d) is None
    texts = [t for t, _ in D.extract_candidates("### 화면 항목 1. 구분\n구분 선택")]
    assert "구분" not in texts


def test_partial_only_for_headings_and_prefers_specific_entry():
    d = make_dict()
    m = D.match_candidate("수익률별", "heading", d)
    assert m["match_type"] == "partial"
    # 정확히 같은 이름('수익률')을 우선하고 '수익률(KIS)' 변형은 섞지 않는다
    assert [c["code"] for c in m["matched_codes"]] == ["90002"]
    assert D.match_candidate("수익률별", "body", d) is None
    p = D.match_candidate("수익률로", "body", d)  # 조사 제거는 normalized 로 표기
    assert p["match_type"] == "normalized"
    # 사전명이 후보에서 차지하는 비율이 낮으면(문장 조각) 부분 일치하지 않는다
    assert D.match_candidate("현재가 변동을 한눈에 비교하는 영역", "heading", d) is None


def test_extract_candidates_from_heading_and_body():
    text = (
        "# 제목\n## 화면 설명\n"
        "### 화면 항목 1. 현재가• 종가 기준으로 표시됩니다.\n"
        "등락률, 체결량 및 거래량을 보여줍니다.\n"
        "## 관련 화면\n- TR 1440 — ETF 현재가\n"
    )
    got = dict(D.extract_candidates(text))
    assert got["현재가"] == "heading"
    assert got["등락률"] == "body"
    assert "체결량" in got


def test_derive_links_end_to_end_and_report():
    d = make_dict()
    screens = [
        {"id": "check:screen:1", "type": "screen",
         "text": "### 화면 항목 1. 현재가\n등락률을 표시합니다."},
        {"id": "check:screen:2", "type": "screen", "text": "### 화면 항목 1. 설정 버튼"},
    ]
    links = D.derive_links(screens, d)
    assert {l["screen_id"] for l in links} == {"check:screen:1"}
    assert {l["matched_codes"][0]["code"] for l in links} >= {"15001", "15004"}
    rep = D.build_report(links, screens, d)
    assert rep["screens_total"] == 2 and rep["screens_linked"] == 1
    assert rep["dictionary_rows"] == 11
