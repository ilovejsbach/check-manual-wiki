"""build_tr_registry 단위 테스트. 모든 레코드와 사례 문장은 합성이며 실데이터를 복사하지 않았다."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_tr_registry as btr  # noqa: E402
from test_derive_case_links import base_records, case  # noqa: E402

AS_OF = "2026-11-02"


def records_with(*cases):
    recs = [r for r in base_records() if r["id"] != "check:screen:1002:해외"]
    for r in recs:  # 병합 후 상태: 1002 는 하나의 화면 레코드
        if r["id"] == "check:screen:1002:종합":
            r["id"], r["categories"] = "check:screen:1002", ["종합", "해외"]
    return recs + list(cases)


def by_tr(rows):
    return {r["tr"]: r for r in rows}


def test_manual_screens_become_manual_confirmed_with_unique_tr():
    rows = btr.build_registry(records_with(), [], AS_OF)
    reg = by_tr(rows)
    assert reg["1002"]["status"] == "manual_confirmed" and reg["1002"]["screen_id"] == "check:screen:1002"
    assert reg["1002"]["categories"] == ["종합", "해외"] and reg["1002"]["title"] == "세계지수종합"
    assert len(rows) == len(reg)
    assert btr.validate_registry(rows, records_with()) == []


def test_unregistered_tr_in_case_is_case_mentioned_and_isolated():
    c = case("check:support-case:a1", "TR 9999 화면에서 값이 비어 보입니다")
    rows = btr.build_registry(records_with(c), [], AS_OF)
    r = by_tr(rows)["9999"]
    assert r["status"] == "case_mentioned" and r["screen_id"] is None and r["title"] is None
    assert r["grade"] == "auto_extracted" and r["case_mentions"] == 1
    assert "오탐" in r["notes"]  # 1회 언급 표시


def test_repeated_mentions_sort_first_and_drop_once_note():
    cs = [case(f"check:support-case:b{i}", "TR 8888 화면 문의") for i in range(3)]
    cs.append(case("check:support-case:c1", "TR 7777 화면 문의"))
    rows = btr.build_registry(records_with(*cs), [], AS_OF)
    cm = [r for r in rows if r["status"] == "case_mentioned"]
    assert [r["tr"] for r in cm] == ["8888", "7777"]
    assert cm[0]["case_mentions"] == 3 and "오탐" not in cm[0]["notes"]


def test_known_tr_counts_case_mentions_but_stays_manual_confirmed():
    c = case("check:support-case:d1", "TR 4101 화면에서 문의")
    reg = by_tr(btr.build_registry(records_with(c), [], AS_OF))
    assert reg["4101"]["status"] == "manual_confirmed" and reg["4101"]["case_mentions"] == 1


def test_promoted_states_survive_regeneration():
    c = case("check:support-case:e1", "TR 9999 화면 문의")
    existing = [{"tr": "9999", "status": "screen_observed", "screen_id": None, "title": "관찰됨", "categories": [],
                 "sources": [{"kind": "observation", "ref": "obs-1", "as_of": AS_OF}], "grade": "screen_observed",
                 "case_mentions": 0, "case_ids": [], "notes": "화면 확인"},
                {"tr": "1000", "status": "rejected", "screen_id": None, "title": None, "categories": [],
                 "sources": [], "grade": "auto_extracted", "case_mentions": 0, "case_ids": [], "notes": "금액 오탐"}]
    reg = by_tr(btr.build_registry(records_with(c), existing, AS_OF))
    assert reg["9999"]["status"] == "screen_observed" and reg["9999"]["title"] == "관찰됨"
    assert reg["9999"]["case_mentions"] == 1  # 언급 수만 갱신
    assert reg["1000"]["status"] == "rejected" and reg["1000"]["notes"] == "금액 오탐"


def test_validate_flags_duplicates_missing_and_unpromoted_case_mentioned():
    recs = records_with()
    rows = btr.build_registry(recs, [], AS_OF)
    bad = rows + [dict(rows[0])]  # 중복 TR
    assert any("중복 TR" in e for e in btr.validate_registry(bad, recs))
    missing = [r for r in rows if r["tr"] != "4101"]  # 화면 레코드는 있는데 마스터에 없음
    assert any("마스터에 없는 화면" in e for e in btr.validate_registry(missing, recs))
    stale = [dict(r, status="case_mentioned", screen_id=None) if r["tr"] == "4101" else r for r in rows]
    assert any("승격 필요" in e for e in btr.validate_registry(stale, recs))


def test_registry_has_no_case_text():
    c = case("check:support-case:f1", "TR 9999 화면에서 홍길동 고객이 문의했습니다")
    rows = btr.build_registry(records_with(c), [], AS_OF)
    assert "홍길동" not in str(rows)  # 사례 본문은 어떤 필드에도 들어가지 않는다
