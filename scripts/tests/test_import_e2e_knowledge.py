import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from import_e2e_knowledge import collect, write_jsonl


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def test_collect_merges_manifest_inventory_and_analysis(tmp_path: Path) -> None:
    screen = tmp_path / "golden" / "batch-001" / "3065"
    write(
        screen / "manifest.json",
        {
            "screen_code": "3065",
            "status": "completed",
            "expected_title": "3065 - CP 발행정보",
            "category": "채권",
            "artifacts": ["screen.png", "inventory.json"],
        },
    )
    (screen / "screen.png").write_bytes(b"png")
    write(
        screen / "inventory.json",
        {
            "screen_code": "3065",
            "collected_at": "2026-11-03T09:51:17",
            "tabs": ["CP발행종목", "CP통계"],
        },
    )
    write(
        tmp_path / "golden" / "batch-001" / "analysis.json",
        {
            "screens": [
                {
                    "screen_code": "3065",
                    "callability_status": "verified",
                    "observed_financial_fields": ["만기일", "신용등급"],
                    "financial_semantics_status": "field_presence_only",
                    "capture_occlusion": {"status": "clock_overlay_detected"},
                }
            ]
        },
    )

    records = collect(tmp_path)

    assert len(records) == 1
    assert records[0]["observation_status"] == "baseline_observed"
    assert records[0]["observed_fields"] == ["만기일", "신용등급"]
    assert records[0]["observed_tabs"] == ["CP발행종목", "CP통계"]
    assert records[0]["warnings"] == ["clock_overlay_detected"]


def test_write_jsonl_is_utf8_and_stable(tmp_path: Path) -> None:
    output = tmp_path / "observations.jsonl"
    write_jsonl([{"screen_code": "1300", "title_observed": "주식현재가"}], output)
    assert "주식현재가" in output.read_text(encoding="utf-8")
