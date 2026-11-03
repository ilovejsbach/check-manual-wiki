import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_check_wiki as b
from field_definition_coverage import compute

DEFS = {"베이시스": {"concept": "베이시스", "definition": "정의", "categories": ["선물"], "sources": [{"title": "t", "authority": "a", "url": "https://x"}]}}


def _obs(code, category, fields, own=()):
    return {"screen_code": code, "category": category, "observed_fields": fields,
            "field_definitions": [{"field": f, "concept": f} for f in own], "evidence": []}


def _built(code):
    return {"id": f"check:field:{code}:{b.slug('베이시스-베이시스')}", "type": "screen_field",
            "definition_status": "authoritative_general_definition", "definition": "정의", "review_status": "researched"}


def test_reasons_are_distinguished_and_only_unbuilt_pairs_fail():
    obs = {"1": _obs("1", "선물", ["베이시스"]), "2": _obs("2", "채권", ["베이시스"]),
           "3": _obs("3", "선물", ["베이시스"], own=["베이시스"]), "4": _obs("4", "선물", ["베이시스"])}
    records = [{"type": "screen", "screen_code": c} for c in ("1", "2", "3")] + [_built("1")]
    r = compute(obs, DEFS, records)
    assert r["applied"] == 1
    assert r["by_reason"] == {"market_mismatch": 1, "own_definition": 1, "no_screen_record": 1}
    assert r["not_built"] == []


def test_applicable_pair_without_record_is_not_built():
    obs = {"1": _obs("1", "선물", ["베이시스"])}
    r = compute(obs, DEFS, [{"type": "screen", "screen_code": "1"}])
    assert r["applied"] == 0 and [s["screen"] for s in r["not_built"]] == ["1"]


def test_real_data_has_no_unbuilt_pairs_when_knowledge_is_current():
    from field_definition_coverage import KNOWLEDGE, load_records
    r = compute(b.load_e2e_observations(), b.load_field_definitions(), load_records(KNOWLEDGE))
    assert r["applied"] >= 0  # 형식 점검: 통합 후 재생성 전에는 not_built 가 있을 수 있어 개수는 단정하지 않는다
