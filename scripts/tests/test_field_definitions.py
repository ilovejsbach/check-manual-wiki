import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_check_wiki as b

ROOT = Path(__file__).resolve().parents[2]


def test_every_definition_has_verifiable_public_source():
    defs = b.load_field_definitions()
    assert defs
    for label, rec in defs.items():
        assert rec["definition"] and rec["sources"], label
        for s in rec["sources"]:
            assert s["url"].startswith("https://") and s["authority"] and s["title"], label


def test_definition_overlay_respects_category_and_leaves_others_label_only(monkeypatch):
    obs = {
        "9001": {"screen_code": "9001", "category": "선물", "observed_fields": ["베이시스", "미지항목"], "field_definitions": [], "evidence": []},
        "9002": {"screen_code": "9002", "category": "채권", "observed_fields": ["베이시스"], "field_definitions": [], "evidence": []},
    }
    monkeypatch.setattr(b, "load_e2e_observations", lambda: obs)
    records = [{"id": "check:screen:9001", "type": "screen", "screen_code": "9001"},
               {"id": "check:screen:9002", "type": "screen", "screen_code": "9002"}]
    b.build_screen_field_records(records)
    fields = {r["id"]: r for r in records if r["type"] == "screen_field"}
    basis = next(r for k, r in fields.items() if ":9001:" in k and "베이시스" in k)
    assert basis["review_status"] == "researched" and basis["formula"] == "선물가격 − 현물가격"
    assert "mofe.go.kr" in basis["text"]
    unknown = next(r for k, r in fields.items() if "미지항목" in k)
    assert unknown["review_status"] == "candidate"
    other = next(r for k, r in fields.items() if ":9002:" in k)
    assert other["review_status"] == "candidate"  # 채권 화면의 베이시스에는 선물 정의를 얹지 않는다
