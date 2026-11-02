import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_ontology_needs as bn  # noqa: E402


def test_groups_unlinked_screen_finding_only():
    cl = [{"case_id": "a", "intent": "screen_finding", "domains": ["채권"]},
          {"case_id": "b", "intent": "screen_finding", "domains": ["채권", "주식"]},
          {"case_id": "c", "intent": "screen_finding", "domains": []},
          {"case_id": "d", "intent": "screen_finding", "domains": ["주식"]},
          {"case_id": "e", "intent": "howto", "domains": ["주식"]}]
    ed = [{"source_id": "d", "type": "about_screen"}]
    out = {n["id"]: n for n in bn.compute(cl, ed, "2026-11-02")}
    assert set(out) == {"check:need:unresolved-bond", "check:need:unresolved-general"}
    assert out["check:need:unresolved-bond"]["raised_by"] == ["a", "b"] and out["check:need:unresolved-bond"]["gap"] is True
