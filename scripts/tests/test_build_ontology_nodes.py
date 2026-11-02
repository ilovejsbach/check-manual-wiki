"""build_ontology_nodes 단위 테스트. 레코드·사례 문장은 합성이며 실데이터를 복사하지 않았다."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_ontology_nodes as bon  # noqa: E402
from test_derive_case_links import base_records, case, rec  # noqa: E402

AS_OF = "2026-11-02"
FUNC_DOC = (
    "# 주요 함수 설명\n## CT\n### 화면 항목 2. 함수 형식\n=CT(\"종목코드\", \"항목\")\n"
    "## CH\n### 화면 항목 2. 함수 형식\n=CH(\"시작일자\" , \"종료일자\" ,\n\"주기\" , 종목(복수) )\n"
    "## CTD\n### 화면 항목 2. 함수 형식\n=CTD(\"함수명\", 가변 파라미터 )### 화면 항목 3. 일자 표현 방법\n"
    + "".join(f"## {n}\n=" + n + '("a")\n' for n in ("CTS", "CIS", "CLIST", "CTR", "CPFG", "CPF")))
DICT = "\n".join([
    "| 함수 | 시장 | 카테고리 | 항목코드 | 항목명 |", "| --- | --- | --- | --- | --- |",
    "| CH | 주식 | 호가 | 14501 | 매도호가1 |", "| CT | 선물 | 호가 | 14501 | 매도호가1 |",
    "| CT | 주식 | 시세 | 15015 | 거래량 |", "| CT | 주식 | 시세 | 4018 | 괴리율 |",
    "| CT | 주식 | 시세 | 3028 | 전일등락구분(0&cl거래무1&cl상한2&cl상승) |",
    "| CT | 주식 | 시세 | 10101 | 시장구분(1&cl유가증권/2&cl코스닥) |",
    "| CT | 경제 | 조사 | 140377 | 제조업 &cl 의약품 제외 |",
    "| CT | 주식 | 시세 | 5555 | 전일시가 |", "| CT | 주식 | 시세 | 5556 | 시간외단일가 |",
])


def records(*cases):
    recs = [r for r in base_records() if not r["id"].startswith("check:excel:항목코드표")]
    recs.append(rec("check:excel:항목코드표:CT:001", "excel", "항목코드표", DICT, source=bon.DICT_SOURCE))
    recs.append(rec(bon.FUNC_DOC_ID, "manual", "주요 함수 설명", FUNC_DOC))
    recs.append(rec(bon.FUNC_EXAMPLES_ID, "excel", "함수 설명", '=CTD("SPT","1","2","3")\n=CTD("SUM","1","2","3")'))
    return recs + list(cases)


def items():
    nodes, conflicts = bon.build_item_nodes(records(), AS_OF)
    return {n["code"]: n for n in nodes}, conflicts


def test_same_code_merges_into_one_node_with_all_applies_to():
    it, _ = items()
    n = it["14501"]
    assert n["id"] == "check:item:14501" and n["name"] == "매도호가1" and n["visibility"] == "public"
    assert {(a["function"], a["market"]) for a in n["applies_to"]} == {("CH", "주식"), ("CT", "선물")}
    assert n["source_locator"] == "CT:001"


def test_name_conflict_goes_to_review_queue():
    recs = records()
    for r in recs:
        if r["id"] == "check:excel:항목코드표:CT:001":
            r["text"] += "\n| CT | 주식 | 시세 | 15015 | 거래수량 |"
    nodes, conflicts = bon.build_item_nodes(recs, AS_OF)
    assert [c["code"] for c in conflicts] == ["15015"]
    n = {x["code"]: x for x in nodes}["15015"]
    assert n["name_conflict"] is True and n["aliases"] == ["거래수량"]


def test_enum_values_parse_only_for_value_notation():
    it, _ = items()
    assert it["10101"]["enum_values"] == [{"value": "1", "label": "유가증권"}, {"value": "2", "label": "코스닥"}]
    assert it["10101"]["enum_parse"] == "slash" and it["10101"]["name"] == "시장구분"
    assert it["3028"]["enum_parse"] == "sequence" and [v["value"] for v in it["3028"]["enum_values"]] == ["0", "1", "2"]
    # '&cl' 이 서술 일부로 쓰인 이름은 enum 이 아니다
    assert "enum_raw" not in it["140377"] and it["140377"]["value_kind"] != "enum"


def test_value_kind_heuristics_are_conservative():
    it, _ = items()
    assert it["15015"]["value_kind"] == "qty" and it["4018"]["value_kind"] == "ratio"
    assert it["14501"]["value_kind"] == "price" and it["3028"]["value_kind"] == "enum"
    assert it["5555"]["value_kind"] != "date"   # 전일시가 는 날짜가 아니다
    assert it["5556"]["value_kind"] != "date"   # 시간외 는 시각이 아니다
    assert all(n["value_kind_grade"] == "auto_extracted" for n in it.values())


def test_function_signature_extracted_and_trimmed_at_closing_paren():
    funcs = {n["name"]: n for n in bon.build_function_nodes(records(), AS_OF)}
    assert funcs["CT"]["signature"] == '=CT("종목코드", "항목")'
    assert funcs["CH"]["signature"].startswith('=CH("시작일자"') and funcs["CH"]["signature"].endswith("종목(복수) )")
    assert funcs["CTD"]["signature"] == "=CTD(\"함수명\", 가변 파라미터 )"  # 같은 줄에 붙은 다음 절 제목은 버린다
    assert funcs["CTD"]["subfunctions"] == ["SPT", "SUM"]
    assert funcs["CT"]["item_table_sheet"] is True and funcs["CT"]["verification"] == "documented"


def test_undocumented_function_is_mentioned_only_and_internal():
    c = case("check:support-case:z1", '=CRS("1","2") 로 입력했는데 값이 비어 있습니다')
    funcs = {n["name"]: n for n in bon.build_function_nodes(records(c), AS_OF)}
    n = funcs["CRS"]
    assert n["verification"] == "mentioned_only" and n["signature"] is None and n["visibility"] == "internal"
    assert n["grade"] == "inferred" and n["case_mentions"] == 1


def test_validate_catches_duplicate_unknown_function_and_missing_link_target(tmp_path):
    nodes, _ = bon.build_item_nodes(records(), AS_OF)
    funcs = bon.build_function_nodes(records(), AS_OF)
    all_nodes = funcs + nodes
    assert bon.validate_nodes(all_nodes) == []
    assert any("중복 ID" in e for e in bon.validate_nodes(all_nodes + [dict(nodes[0])]))
    assert any("없는 함수" in e for e in bon.validate_nodes(nodes))  # 함수 노드를 빼면 applies_to 참조가 깨진다
    links = tmp_path / "links.jsonl"
    links.write_text('{"from":"check:support-case:a","to":"check:item:99999"}\n{"from":"check:support-case:a","to":"check:func:CT"}\n',
                     encoding="utf-8")
    errs = bon.validate_nodes(all_nodes, links)
    assert errs == ["I1 관계 대상 노드 없음 check:item:99999"]
