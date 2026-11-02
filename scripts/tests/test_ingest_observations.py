"""ingest_observations 단위 테스트. 관찰 파일·레코드는 모두 합성이다."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import derive_item_links as dil  # noqa: E402
import ingest_observations as ing  # noqa: E402
from test_derive_case_links import rec  # noqa: E402

AS_OF = "2026-11-03"
DICT = "\n".join([
    "| 함수 | 시장 | 카테고리 | 항목코드 | 항목명 |", "| --- | --- | --- | --- | --- |",
    "| CT | 주식 | 시세 | 15001 | 현재가 |", "| CT | 주식 | 시세 | 15015 | 거래량 |",
    "| CT | 주식 | 시세 | 4018 | 괴리율 |", "| CT | 선물 | 시세 | 4019 | 괴리율 |",
])


def obs(tr="4101", **kw):
    base = {"screen_code": tr, "title": "현재가 종합표", "exists": True, "menu_path": ["주식", "시세"], "tabs": [],
            "output_columns": [{"label": "현재가"}, {"label": "거래량"}], "observed_at": AS_OF,
            "app_version": "1.0.0", "capture_id": f"cap-{tr}"}
    base.update(kw)
    return base


def manual():
    return rec("check:screen:4101", "screen", "4101 - 현재가 종합표", "현재가와 거래량을 보여 줍니다.", code="4101", loc="100-101")


def test_valid_observation_passes_and_required_fields_checked():
    assert ing.validate_observation(obs()) == []
    errs = ing.validate_observation({"screen_code": "41"})
    assert any("observed_at" in e for e in errs) and any("형식 오류" in e for e in errs)


def test_privacy_guards_reject_values_phone_email_and_long_digits_but_allow_stock_code():
    assert any("금지된 키" in e for e in ing.validate_observation(obs(values=[1, 2])))
    assert any("전화번호" in e for e in ing.validate_observation(obs(buttons=["문의 02-123-4567"])))
    assert any("전화번호" in e for e in ing.validate_observation(obs(buttons=["a@b.co.kr"])))
    assert any("전화번호" in e for e in ing.validate_observation(obs(inputs=[{"label": "계좌", "default": "12345678901"}])))
    assert ing.validate_observation(obs(inputs=[{"label": "종목", "type": "text", "default": "005930"}])) == []  # 6자리 종목코드는 허용
    assert any("너무 김" in e for e in ing.validate_observation(obs(buttons=["가" * 61])))


def test_exists_false_cannot_carry_columns():
    assert any("exists=false" in e for e in ing.validate_observation(obs(exists=False)))
    assert ing.validate_observation(obs(exists=False, output_columns=[], title=None)) == []


def test_judge_outcomes():
    m = manual()
    assert ing.judge(obs(), m)["outcome"] == "matched"
    r = ing.judge(obs(title="전혀 다른 제목"), m)
    assert r["outcome"] == "conflict" and r["drift"] == ["제목 불일치"]
    assert ing.judge(obs(exists=False, output_columns=[]), m)["outcome"] == "conflict"
    assert ing.judge(obs("9999"), None)["outcome"] == "new"
    assert ing.judge(obs("9999", exists=False, output_columns=[]), None)["outcome"] == "absent"
    assert ing.judge(obs(output_columns=[{"label": "가상컬럼"}]), m)["columns_not_in_manual"] == ["가상컬럼"]


def row(tr, status, **kw):
    r = {"tr": tr, "status": status, "screen_id": None, "title": None, "categories": [], "sources": [], "grade": "auto_extracted",
         "case_mentions": 1, "case_ids": [], "notes": ""}
    r.update(kw)
    return r


def test_promote_registry_rules():
    rows = [row("9999", "case_mentioned"), row("8888", "case_mentioned"), row("4101", "manual_confirmed", screen_id="check:screen:4101"),
            row("1000", "rejected", notes="사람이 기각"), row("2000", "manual_confirmed", screen_id="check:screen:2000")]
    observations = {"9999": obs("9999", title="신규"), "8888": obs("8888", exists=False, output_columns=[]),
                    "4101": obs("4101"), "1000": obs("1000"), "2000": obs("2000", exists=False, output_columns=[]),
                    "7777": obs("7777", title="처음 발견")}
    results = {"9999": {"outcome": "new", "drift": []}, "8888": {"outcome": "absent", "drift": []},
               "4101": {"outcome": "matched", "drift": []}, "1000": {"outcome": "new", "drift": []},
               "2000": {"outcome": "conflict", "drift": ["매뉴얼에는 있으나 실제 앱에 없음"]}, "7777": {"outcome": "new", "drift": []}}
    out = {r["tr"]: r for r in ing.promote_registry(rows, results, observations, AS_OF)}
    assert out["9999"]["status"] == "screen_observed" and out["9999"]["title"] == "신규" and out["9999"]["screen_id"] == "check:screen:9999"
    assert out["8888"]["status"] == "rejected"
    assert out["4101"]["status"] == "manual_confirmed"          # 일치하면 상태 유지
    assert out["1000"]["status"] == "rejected" and out["1000"]["notes"] == "사람이 기각"  # 사람이 정한 상태는 덮어쓰지 않는다
    assert out["2000"]["status"] == "conflict" and "실제 앱에 없음" in out["2000"]["notes"]
    assert out["7777"]["status"] == "screen_observed" and out["7777"]["case_mentions"] == 0  # 관찰로 처음 발견


def dict_index():
    return dil.ItemDict(dil.parse_dictionary([rec("check:excel:항목코드표:CT:001", "excel", "t", DICT, source="HangMokCodeTable_ExcelPremium_update01.xlsx")]))


def test_observed_edges_are_screen_observed_provides_and_ambiguous_goes_to_review():
    o = obs(output_columns=[{"label": "현재가"}, {"label": "거래량"}, {"label": "괴리율"}, {"label": "현재가"}, {"label": "알수없는라벨"}])
    edges, review = ing.observed_edges(o, "check:screen:4101", dict_index(), AS_OF)
    assert {e["target_id"] for e in edges} == {"check:item:15001", "check:item:15015"}  # 중복 라벨은 한 번만
    e = edges[0]
    assert e["type"] == "provides" and e["grade"] == "screen_observed" and e["canonical"] is True
    assert e["evidence"]["source_locator"] == "observations/screens/4101.json"
    assert [r["label"] for r in review] == ["괴리율"] and review[0]["candidate_codes"] == ["4018", "4019"]


def test_observed_screen_node_is_internal_and_screen_observed():
    n = ing.observed_screen_node(obs("9999", title="신규"), AS_OF)
    assert n["id"] == "check:screen:9999" and n["visibility"] == "internal" and n["grade"] == "screen_observed"
    assert n["output_columns"] == ["현재가", "거래량"] and n["aliases"][0] == "TR9999"


def test_pilot_targets_order_and_category_spread():
    reg = [row("9001", "case_mentioned", case_mentions=5), row("9002", "case_mentioned", case_mentions=9), row("9003", "case_mentioned", case_mentions=1)]
    for i in range(30):
        reg.append(row(f"{1000 + i}", "manual_confirmed", title=f"화면{i}", categories=["선물" if i < 20 else "옵션"], case_mentions=30 - i))
    t = ing.pilot_targets(reg, [])["targets"]
    unconfirmed = [x["tr"] for x in t if x["kind"] == "unconfirmed"]
    assert unconfirmed == ["9002", "9001", "9003"]
    manual_t = [x for x in t if x["kind"] == "manual"]
    assert len(manual_t) == ing.PILOT_MANUAL
    assert {x["category"] for x in manual_t} == {"선물", "옵션"}  # 분류가 한쪽으로 쏠리지 않는다
