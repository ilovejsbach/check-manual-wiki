import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_check_wiki
from build_check_wiki import frontmatter, screen_code, slug


def test_slug_normalizes_for_paths() -> None:
    assert slug(" 1300 - 주식현재가 ") == "1300-주식현재가"


def test_screen_code_accepts_only_four_digit_token() -> None:
    assert screen_code("1300 - 주식현재가") == "1300"
    assert screen_code("12345 데이터") is None


def test_frontmatter_supports_alias_lists() -> None:
    rendered = frontmatter(
        title="화면",
        description="설명",
        tags=["CHECK"],
        source="manual.pdf",
        extra={"aliases": ["1300", "TR1300"]},
    )
    assert '  - "1300"' in rendered
    assert '  - "TR1300"' in rendered


def test_manual_enrichment_builds_candidate_companion(tmp_path, monkeypatch) -> None:
    root = tmp_path
    output = root / "content" / "check-expert"
    sources = root / "sources" / "check-expert"
    output.mkdir(parents=True)
    sources.mkdir(parents=True)
    (output / "screen.md").write_text(
        frontmatter(
            title="주식현재가",
            description="공식 문서",
            tags=["CHECK"],
            source="manual.pdf",
            extra={"knowledge_id": "check:screen:1300"},
        )
        + "# 주식현재가\n",
        encoding="utf-8",
    )
    summary = {
        "target_knowledge_id": "check:screen:1300",
        "signal_count": 2,
        "duplicate_group_count": 1,
        "manual_candidate_counts": {"faq": 2},
        "topic_counts": {"주식": 2},
        "examples": [
            {
                "request_text": "조회 방법 문의",
                "action_text": "조회 절차 안내",
                "manual_candidates": ["faq", "procedure"],
                "evidence_locator": "sheet!row:1",
            }
        ],
    }
    (sources / build_check_wiki.ENRICHMENT_NAME).write_text(
        json.dumps(summary, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    monkeypatch.setattr(build_check_wiki, "ROOT", root)
    monkeypatch.setattr(build_check_wiki, "OUTPUT_DIR", output)
    monkeypatch.setattr(build_check_wiki, "SOURCE_DIR", sources)

    assert build_check_wiki.build_manual_enrichment() == 2
    page = output / "운영-보강" / "check-screen-1300.md"
    assert page.exists()
    text = page.read_text(encoding="utf-8")
    assert "검수 전 후보" in text
    assert "sheet!row:1" in text


def test_unmapped_enrichment_preserves_topic_queue(tmp_path, monkeypatch) -> None:
    output = tmp_path / "content" / "check-expert"
    sources = tmp_path / "sources" / "check-expert"
    output.mkdir(parents=True)
    sources.mkdir(parents=True)
    summary = {
        "topic": "설치·실행환경",
        "signal_count": 3,
        "manual_candidate_counts": {"troubleshooting": 3},
        "examples": [
            {
                "request_text": "실행 오류 문의",
                "action_text": "설치 상태 확인",
                "evidence_locator": "sheet!row:2",
            }
        ],
    }
    (sources / build_check_wiki.UNMAPPED_ENRICHMENT_NAME).write_text(
        json.dumps(summary, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    monkeypatch.setattr(build_check_wiki, "ROOT", tmp_path)
    monkeypatch.setattr(build_check_wiki, "OUTPUT_DIR", output)
    monkeypatch.setattr(build_check_wiki, "SOURCE_DIR", sources)

    assert build_check_wiki.build_unmapped_enrichment() == 2
    pages = list((output / "운영-보강" / "미매핑").glob("*.md"))
    assert len(pages) == 2
    assert any("mapping_status: \"unmapped\"" in page.read_text(encoding="utf-8") for page in pages)
