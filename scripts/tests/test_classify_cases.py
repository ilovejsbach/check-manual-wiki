import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import classify_cases as cc  # noqa: E402


def rec(title, situation="", cid="check:support-case:t1"):
    return {"id": cid, "type": "support_case", "title": title,
            "text": f"# {title}\n\n## 사용자가 겪은 상황\n\n{situation}\n\n## 당시 대응\n\n응답"}


def test_screen_finding_beats_env_words():
    c = cc.classify(rec("사용 절차 — 선물옵션 협의대량 거래를 볼 수 있는 화면 문의"))
    assert c["intent"] == "screen_finding" and "선물" in c["domains"] and "옵션" in c["domains"]


def test_empty_case():
    assert cc.classify(rec("활용 팁 — 문의 내용 미기재", "문의 내용 미기재"))["intent"] == "empty"


def test_env_setup_and_no_domain():
    c = cc.classify(rec("주의사항 — 단말 교체 후 윈도우 초기화"))
    assert c["intent"] == "env_setup" and c["domains"] == []


def test_response_section_not_used():
    r = rec("질문과 답변 — 확인 부탁드립니다", "내용")
    r["text"] += "\n채권 선물 옵션 설치"
    assert cc.classify(r)["domains"] == []


def test_compute_has_no_body_or_locator():
    r = rec("사용 절차 — 방법 문의")
    r["source_locator"] = "row:1"
    out = cc.compute([r], "2026-11-02")[0]
    assert "text" not in out and "source_locator" not in out and out["grade"] == "auto_extracted"
