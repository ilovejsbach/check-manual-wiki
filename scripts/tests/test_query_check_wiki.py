import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from query_check_wiki import score_record, search

RECORDS = [
    {
        "id": "check:screen:1300",
        "type": "screen",
        "title": "1300 - 주식현재가",
        "aliases": ["1300", "TR1300", "화면 1300"],
        "screen_code": "1300",
        "category": "주식",
        "text": "주식 종목의 시세와 투자자 정보를 제공합니다.",
    },
    {
        "id": "check:screen:4000",
        "type": "screen",
        "title": "4000 - 선물옵션종합",
        "aliases": ["4000", "TR4000"],
        "screen_code": "4000",
        "category": "선물",
        "text": "선물과 옵션의 시세를 제공합니다.",
    },
]


def test_exact_screen_code_has_strong_score() -> None:
    assert score_record(RECORDS[0], "1300") >= 100


def test_alias_query_returns_matching_screen_first() -> None:
    assert search(RECORDS, "TR1300")[0]["id"] == "check:screen:1300"


def test_type_and_category_filters() -> None:
    results = search(RECORDS, "시세", record_type="screen", category="선물")
    assert [record["id"] for record in results] == ["check:screen:4000"]
