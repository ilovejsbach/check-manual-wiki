"""leak_gate 합성 테스트 (실데이터 문장 아님)."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import leak_gate  # noqa: E402
from sanitize_cases import main as sanitize_main  # noqa: E402

DIRTY = (
    "문의: 321-5678 로 연락, mail@example.test, [REDACTED_ENTITY] 요청, "
    "CRM데이터(PID복원)!row:12, 2026-03-03 오후 1시, 가나다자산운용\n"
)


def _scan(tmp_path, text, names=None):
    f = tmp_path / "a.md"
    f.write_text(text, encoding="utf-8")
    return leak_gate.run([f], names or {}, [], 0.8)


def test_detects_each_leak_type(tmp_path):
    res = _scan(tmp_path, DIRTY, {"가나다자산운용": "한 자산운용사"})
    kinds = set(res["by_type"])
    assert {"phone", "email", "token", "origin", "date", "name"} <= kinds
    assert not res["ok"]
    assert all(v["line"] == 1 for v in res["violations"])


def test_clean_text_passes_and_wrapped_token_allowed(tmp_path):
    res = _scan(tmp_path, "함수가 '⟦[NUMBER]⟧' 로 표시됨. 1300 화면, 장마감 15:30, =CT(\"⟦[NUMBER]⟧\",1)\n")
    assert res["ok"], res["violations"]
    assert res["info"].get("info-token-wrapped", 0) == 2


def test_hex_hash_not_phone(tmp_path):
    res = _scan(tmp_path, "id 0151920252b5fae7 sref:4a19d2159996 case-e2a5b026\n")
    assert res["ok"], res["violations"]


def test_cli_exit_code_and_json(tmp_path, capsys):
    f = tmp_path / "b.md"
    f.write_text(DIRTY, encoding="utf-8")
    assert leak_gate.main([str(f), "--json", "--names-file", str(tmp_path / "none")]) == 1
    data = json.loads(capsys.readouterr().out)
    assert data["violation_count"] > 0 and data["by_type"]["phone"] >= 1
    # 보고에 값 자체가 없어야 함
    assert "321-5678" not in json.dumps(data, ensure_ascii=False)
    g = tmp_path / "c.md"
    g.write_text("1300 화면 문의\n", encoding="utf-8")
    assert leak_gate.main([str(g), "--names-file", str(tmp_path / "none")]) == 0


def _write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False) + "\n", encoding="utf-8")


def test_pair_fact_mismatch_detected(tmp_path):
    o, p = tmp_path / "o.jsonl", tmp_path / "p.jsonl"
    _write(o, {"text": "3005 화면에서 =CT(\"A\",1) 실행 시 '권한이 없습니다' 표시"})
    _write(p, {"text": "3006 화면에서 =CT(\"A\",2) 실행 시 '권한 문제' 표시"})
    res = leak_gate.run([p], {}, [(o, p)], 0.8)
    assert res["by_type"].get("fact") == 1


def test_pair_ngram_overlap_threshold(tmp_path):
    base = "엑셀 프리미엄에서 종목코드를 바꾸면 실시간 값이 갱신되지 않는 현상이 반복적으로 발생합니다"
    o, same, diff = tmp_path / "o.jsonl", tmp_path / "same.jsonl", tmp_path / "diff.jsonl"
    _write(o, {"text": base})
    _write(same, {"text": base})
    _write(diff, {"text": "갱신 지연이 보고되어 재설치와 권한 부여로 정상화 확인함 추가 점검 예정"})
    assert leak_gate.run([same], {}, [(o, same)], 0.8)["by_type"].get("ngram") == 1
    assert "ngram" not in leak_gate.run([diff], {}, [(o, diff)], 0.8)["by_type"]


def test_pair_line_count_mismatch(tmp_path):
    o, p = tmp_path / "o.jsonl", tmp_path / "p.jsonl"
    o.write_text('{"text": "a"}\n{"text": "b"}\n')
    p.write_text('{"text": "a"}\n')
    assert leak_gate.run([p], {}, [(o, p)], 0.8)["by_type"].get("pair") == 1


def test_sanitize_then_gate_clean(tmp_path):
    src = tmp_path / "in.jsonl"
    rec = {"examples": [{
        "request_text": "화면번호 : 1300 - 전화번호 : 321-5678 - 문의내용 : 가나다자산운용 06.25 "
                        "오후 1시 CRM데이터(PID복원)!row:9 [REDACTED_ENTITY] 문의 =CT(\"[NUMBER]\",1) 오류",
        "evidence_locator": "x!row:9", "candidate_id": "manual-candidate:CRM-00009"}]}
    _write(src, rec)
    names = tmp_path / "names.txt"
    names.write_text("가나다자산운용\t한 자산운용사\n", encoding="utf-8")
    out = tmp_path / "out"
    sanitize_main([str(src), "-o", str(out), "--names-file", str(names), "--salt", "s"])
    res = leak_gate.run([out / "in.jsonl"], {"가나다자산운용": "x"}, [(src, out / "in.jsonl")], 1.0)
    assert res["ok"], res["violations"]
