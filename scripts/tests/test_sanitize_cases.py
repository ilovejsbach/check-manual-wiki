"""합성 사례 테스트 (실데이터 문장 아님)."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sanitize_cases import (  # noqa: E402
    Ctx,
    collect_names,
    extract_facts,
    main,
    sanitize_obj,
    sanitize_text,
)


def ctx(names=None):
    return Ctx("test-salt", names or {})


def test_phone_ext_email_removed_and_field_dropped():
    c = ctx()
    t = "- 화면번호 : 1234 - 전화번호 : 321-5678 - 문의내용 : 담당 연락은 내선 4567 또는 help@example.test 로 부탁"
    out = sanitize_text(t, c)
    assert "321-5678" not in out and "4567" not in out and "@" not in out
    assert "전화번호" not in out
    assert "화면번호 : 1234" in out
    assert "상담 창구" in out or "공식 문의 채널" in out


def test_company_names_collected_and_generalized():
    texts = ["가나다자산운용 담당자가 문의", "라마바증권에서 오류", "기초자산 가격 조회", "유동화증권 목록"]
    names = collect_names(texts)
    assert "가나다자산운용" in names and "라마바증권" in names
    assert "기초자산" not in names and "유동화증권" not in names
    out = sanitize_text("가나다자산운용과 라마바증권 문의", ctx(names))
    assert "가나다" not in out and "라마바" not in out
    assert "자산운용사" in out and "증권사" in out


def test_dates_and_times_generalized_but_market_time_kept():
    out = sanitize_text("06.25 오후 1시경 접속, 2026-03-03 만기, 10:02 에 확인, 장마감 15:30 기준", ctx())
    for bad in ("06.25", "1시", "2026-03-03", "10:02"):
        assert bad not in out
    assert "15:30" in out and "오후" in out and "해당 일자" in out


def test_origin_locator_replaced_by_hash():
    c = ctx()
    src = "증거 위치: `CRM데이터(PID복원)!row:12` / CRM-00001"
    out = sanitize_text(src, c)
    assert "row:" not in out and "PID복원" not in out and "CRM데이터" not in out and "CRM-00001" not in out
    assert "sref:" in out and "case-" in out
    # 같은 입력 -> 같은 해시 (대응은 해시로만 가능)
    assert out == sanitize_text(src, c)
    assert sanitize_text("`CRM데이터(PID복원)!row:13`", c) != sanitize_text("`CRM데이터(PID복원)!row:12`", c)


def test_placeholder_tokens_become_words_symptom_tokens_wrapped():
    out = sanitize_text("[REDACTED_ENTITY] 담당자 [PERSON]님이 [IDENTIFIER] 조회", ctx())
    assert "[" not in out and "고객사" in out and "특정 종목" in out
    sym = sanitize_text("함수 결과가 '[NUMBER]' 로 표시됩니다", ctx())
    assert "⟦[NUMBER]⟧" in sym
    sym2 = sanitize_text("셀에 [NUMBER]로 나옵니다", ctx())
    assert "⟦[NUMBER]⟧" in sym2


def test_technical_facts_preserved_exactly():
    t = (
        "화면번호 : 3005, 4080 에서 =CT(\"[NUMBER]\",\"A\",1) 입력 시 '사용 권한이 없습니다' 오류, "
        "#NAME? 가 보임. TR 1318 와 [1321] 화면 확인. 연락 321-5678."
    )
    out = sanitize_text(t, ctx())
    assert extract_facts(out) == extract_facts(t)
    assert '=CT("⟦[NUMBER]⟧","A",1)' in out
    assert "'사용 권한이 없습니다'" in out and "#NAME?" in out


def test_greeting_and_person_titles():
    out = sanitize_text("안녕하세요. [IDENTIFIER]+ 입니다. 김철수 과장님께 전달했습니다. 감사합니다.", ctx())
    assert "안녕하세요" not in out and "감사합니다" not in out
    assert "김철수" not in out


def test_record_walk_drops_cells_and_hashes_locators():
    rec = {
        "candidate_id": "manual-candidate:CRM-00123",
        "evidence_locator": "20260101!row:4",
        "source_cell_ids": ["workbook:01:abc:sheet:001:A4"],
        "request_text": "화면번호 : 1300 문의",
        "markdown_path": "x/y/abcd-[REDACTED_ENTITY]-문의.md",
    }
    out = sanitize_obj(rec, ctx())
    assert "source_cell_ids" not in out and "evidence_locator" not in out
    assert out["source_ref"].startswith("sref:")
    assert "CRM-00123" not in json.dumps(out, ensure_ascii=False)
    assert "[" not in out["markdown_path"] and " " not in out["markdown_path"]


def test_cli_end_to_end(tmp_path):
    src = tmp_path / "in.jsonl"
    rec = {"examples": [{"request_text": "화면번호 : 1300 - 전화번호 : 321-5678 - 문의내용 : 가나다자산운용 06.25 문의",
                         "evidence_locator": "a!row:1"}]}
    src.write_text(json.dumps(rec, ensure_ascii=False) + "\n", encoding="utf-8")
    names = tmp_path / "names.txt"
    names.write_text("가나다자산운용\t한 자산운용사\n", encoding="utf-8")
    out = tmp_path / "out"
    assert main([str(src), "-o", str(out), "--names-file", str(names), "--salt", "s"]) == 0
    body = (out / "in.jsonl").read_text(encoding="utf-8")
    for bad in ("321-5678", "가나다", "06.25", "row:1"):
        assert bad not in body
    assert "1300" in body


def test_neutralize_tokens_replaces_placeholders_but_keeps_symptoms_and_facts():
    import sanitize_cases as sc

    assert sc.neutralize_tokens("[REDACTED_ENTITY]에서 [PERSON]님 문의") == "고객사에서 담당자님 문의"
    assert sc.neutralize_tokens("[IDENTIFIER] 종목 시세") == "특정 종목 시세"
    assert sc.neutralize_tokens("함수가 '[NUMBER]' 로 표시됩니다") == "함수가 '⟦[NUMBER]⟧' 로 표시됩니다"
    assert sc.neutralize_tokens('=CT([IDENTIFIER], 4001)') == '=CT(⟦[IDENTIFIER]⟧, 4001)'
    assert sc.neutralize_tokens("화면번호 : 1300 TR 4611 2026년 3월") == "화면번호 : 1300 TR 4611 2026년 3월"  # 토큰 외에는 건드리지 않는다
