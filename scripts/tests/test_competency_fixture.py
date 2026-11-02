import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INTENTS = {
    "find_screen",
    "find_function",
    "explain_field",
    "compare_screens",
    "excel_howto",
    "concept_to_screen",
    "troubleshoot",
}


def _load(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_competency_questions_reference_existing_ids():
    questions = _load(ROOT / "scripts/tests/fixtures/competency_questions.jsonl")
    ids = {r["id"] for r in _load(ROOT / "knowledge/check-expert/knowledge.jsonl")}
    assert len(questions) == 60
    assert len({q["id"] for q in questions}) == len(questions)
    for q in questions:
        assert q["intent"] in INTENTS, q["id"]
        assert q["question"].strip()
        missing = [i for i in q["expected_ids"] + q.get("expected_path", []) if i not in ids]
        assert not missing, (q["id"], missing)
        if q.get("gap"):
            assert q["expected_ids"] == [] and q.get("gap_reason"), q["id"]
        else:
            assert q["expected_ids"], q["id"]
