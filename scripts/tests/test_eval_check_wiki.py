import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from eval_check_wiki import DEFAULT_QUERIES, crosslink_metrics, evaluate, load_queries
from query_check_wiki import load_records

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "knowledge" / "check-expert" / "knowledge.jsonl"


def test_fixture_expected_ids_exist_in_knowledge_base() -> None:
    records = load_records(INDEX)
    ids = {record["id"] for record in records}
    queries = load_queries(DEFAULT_QUERIES)
    assert 40 <= len(queries) <= 60
    assert all(query["kind"] in {"screen_code", "alias", "title", "function", "natural_language"} for query in queries)
    assert all(expected_id in ids for query in queries for expected_id in query["expected_ids"])
    assert sum(record.get("screen_code") == "1002" for record in records) == 1


def test_search_quality_does_not_regress_below_baseline() -> None:
    report = evaluate(load_records(INDEX), load_queries(DEFAULT_QUERIES))
    metrics = report["metrics"]
    # 59-query post-change measurements are .8644/.8983/.9322/.8898; floors keep a 2pp cushion.
    assert metrics["recall@1"] >= 0.844
    assert metrics["recall@3"] >= 0.878
    assert metrics["recall@5"] >= 0.912
    assert metrics["mrr"] >= 0.869


def test_crosslinks_cover_mentions_and_are_symmetric() -> None:
    report = crosslink_metrics(load_records(INDEX))
    assert report["mention_link_rate"] >= 0.90
    assert report["asymmetric_relationship_edges"] == 0
    # 53 -> 62: 증거 위치 줄의 행 번호(row:4657 등)가 화면번호로 오인돼 만들던 가짜 링크가 사라져,
    # 의도적으로 매핑하지 않은 "공식 문서 연결 대기" 9건이 링크 없음으로 집계된다.
    assert report["manual_records_without_screen_links"] <= 62
    assert len(report["manual_records_without_screen_link_reasons"]) == report["manual_records_without_screen_links"]
