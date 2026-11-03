import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate_case_rewrite as v  # noqa: E402

ORIG = {"id": "a", "request": "TR3471 민평 금리 3.571% 가 TR3435 와 상이하다는 문의입니다 특정 종목 기준", "response": "3471 화면에서 민평(선택)을 민평(3사)로 바꾸면 3435 와 같은 값이 나옵니다 라고 안내"}


def test_good_rewrite_passes():
    new = {"id": "a", "request": "3471 화면과 3435 화면의 민평 금리가 서로 달라 이유를 문의함.", "response": "3471에서 평가사 기준을 민평(3사)로 바꾸면 3435와 같은 값이 나온다고 안내했습니다."}
    assert v.check(ORIG, new) == []


def test_flags_lost_screen_added_number_leak_and_copy():
    bad = {"id": "a", "request": "4000 화면 금리 3.571% 문의 안녕하세요", "response": "3471 화면에서 민평(선택)을 민평(3사)로 바꾸면 3435 와 같은 값이 나옵니다 라고 안내"}
    errs = "; ".join(v.check(ORIG, bad))
    assert "추가 4자리 번호 4000" in errs and "누출 소수값" in errs and "누출 인사말" in errs


def test_missing_and_ok_counts():
    rep = v.validate([ORIG, {**ORIG, "id": "b"}], [{"id": "a", "request": "3471 화면과 3435 화면의 민평 금리가 달라 문의함입니다 정도", "response": "3471에서 민평(3사)로 바꾸면 3435와 같은 값이 나온다고 안내했습니다 입니다."}])
    assert rep["missing"] == ["b"] and rep["ok"] == 1


def test_menu_path_overlap_allowed_but_long_copy_flagged_and_empty_response_ok():
    o = {"id": "c", "request": "화면 설정 문의입니다 정도의 요청입니다", "response": "통합환경설정(F5)>기본설정>화면>화면 정렬 유형에서 바꿉니다 라고 안내하고 추가 설명이 길게 이어지는 응답 문장 전체"}
    ok = {"id": "c", "request": "화면 설정 방법을 문의했습니다 정도입니다.", "response": "통합환경설정(F5)>기본설정>화면>화면 정렬 유형에서 변경할 수 있다고 안내했습니다."}
    assert v.check(o, ok) == []
    copy = {"id": "c", "request": ok["request"], "response": o["response"]}
    assert any("복사 의심" in e for e in v.check(o, copy))
    empty = {"id": "c", "request": ok["request"], "response": "대응 내용이 기록되지 않았습니다."}
    assert v.check(o, empty) == []


def test_form_and_body_screen_numbers_must_be_preserved():
    orig = {"id": "a", "request": "- 화면번호 : 4101 / 3080 - 전화번호 : - 문의내용 : #6000 공시 화면 검색 방법 문의", "response": "1389-항목편집에서 추가하세요"}
    ok = {"id": "a", "request": "#6000 공시 화면의 검색 방법을 문의했습니다. 조건은 기록되지 않았습니다.", "response": "1389 화면의 항목편집에서 추가하도록 안내했습니다.", "form_screens": ["4101", "3080"]}
    assert not [e for e in v.check(orig, ok) if "화면번호" in e]
    bad = {**ok, "response": "항목편집에서 추가하도록 안내했습니다.", "form_screens": ["4101"]}
    errs = v.check(orig, bad)
    assert any("1389" in e for e in errs) and any("3080" in e for e in errs)
