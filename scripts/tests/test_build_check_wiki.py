import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_check_wiki
from build_check_wiki import (
    clean_case_request,
    enrich_relationships,
    extract_related_screen_codes,
    format_pdf_page_text,
    frontmatter,
    normalize_screen_title,
    render_pdf_section,
    screen_code,
    slug,
)


def test_slug_normalizes_for_paths() -> None:
    assert slug(" 1300 - 주식현재가 ") == "1300-주식현재가"


def test_screen_code_accepts_only_four_digit_token() -> None:
    assert screen_code("1300 - 주식현재가") == "1300"
    assert screen_code("12345 데이터") is None


def test_related_screen_codes_accept_tr_notation() -> None:
    body = "## 관련 화면\n\n- TR 6350 — 아시아 지수종합\n- 6342 - 대륙별지수"
    assert extract_related_screen_codes(body, "1002") == ["6342", "6350"]


def test_screen_title_and_internal_numbering_have_distinct_hierarchy() -> None:
    assert normalize_screen_title("1002- 세계지수종합") == "1002 - 세계지수종합"
    rendered = format_pdf_page_text(
        "11. 해외\n1002- 세계지수종합\n화면 설명\n1 대륙별 버튼 선택\n설명 본문",
        title="1002 - 세계지수종합",
        category="해외",
        rendered_headings={"화면 설명"},
    )
    assert "11. 해외" not in rendered
    assert "1002- 세계지수종합" not in rendered
    assert "### 화면 항목 1. 대륙별 버튼 선택" in rendered


def test_screen_page_links_source_image_without_repeating_it_inline() -> None:
    rendered = render_pdf_section(
        title="1002 - 세계지수종합",
        category="해외",
        start_page=0,
        end_page=1,
        page_texts=["화면 개요\n세계 주요 지수를 제공합니다."],
        child_headings=[],
    )
    assert "## 원문 근거" in rendered
    assert "[원문 PDF 1쪽 이미지 보기]" in rendered
    assert "![" not in rendered
    assert "<small>" not in rendered
    assert "<details" not in rendered


def test_clean_case_request_removes_source_form_fields() -> None:
    raw = "- 화면번호 : 1949 - 전화번호 : [PHONE] - 버전 : 신버전 - 문의내용 : 엑셀 연동 오류"
    assert clean_case_request(raw) == "엑셀 연동 오류"


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

    assert build_check_wiki.build_manual_enrichment() == 8
    page = output / "문의-대응" / "화면별" / "check-screen-1300.md"
    assert page.exists()
    text = page.read_text(encoding="utf-8")
    assert "검수 전 후보" in text
    assert "sheet!row:1" in text
    cases = list((output / "문의-대응" / "procedure").glob("*.md"))
    assert any(
        'document_type: "support_case"' in item.read_text(encoding="utf-8") for item in cases
    )


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

    assert build_check_wiki.build_unmapped_enrichment() == 3
    pages = list((output / "문의-대응" / "분류-대기").glob("*.md"))
    assert len(pages) == 2
    assert any('mapping_status: "unmapped"' in page.read_text(encoding="utf-8") for page in pages)


def test_typed_relationships_include_manual_sequence_and_semantic_links() -> None:
    records = [
        {
            "id": "check:screen:1000",
            "title": "주식 현재가",
            "aliases": ["현재가"],
            "category": "주식",
            "source": build_check_wiki.PDF_NAME,
            "source_locator": "10-11",
            "related_ids": [],
        },
        {
            "id": "check:screen:1001",
            "title": "주식 현재가 비교",
            "aliases": ["현재가 비교"],
            "category": "주식",
            "source": build_check_wiki.PDF_NAME,
            "source_locator": "12",
            "related_ids": [],
        },
        {
            "id": "check:excel:current-price",
            "title": "주식 현재가 함수",
            "aliases": ["현재가 함수"],
            "category": "Excel Premium",
            "source": "excel-manual.xls",
            "source_locator": "함수설명",
            "related_ids": [],
        },
    ]

    enrich_relationships(records)

    first_types = {item["type"] for item in records[0]["relationships"]}
    assert "next" in first_types
    assert "semantic" in first_types
    assert records[0]["related_ids"]


def test_apply_e2e_observations_preserves_verification_boundaries(tmp_path, monkeypatch) -> None:
    observation = {
        "screen_code": "1300",
        "observation_status": "deep_observed",
        "callability_status": "verified",
        "golden_status": "in_progress",
        "financial_review_status": "partial_unapproved",
        "observed_at": "2026-11-03T10:00:00",
        "observed_fields": ["현재가", "VWAP"],
        "observed_tabs": ["현재가", "공시"],
        "warnings": ["clock_overlay_detected"],
    }
    (tmp_path / build_check_wiki.E2E_OBSERVATIONS_NAME).write_text(
        json.dumps(observation, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    monkeypatch.setattr(build_check_wiki, "SOURCE_DIR", tmp_path)
    records = [
        {
            "id": "check:screen:1300",
            "type": "screen",
            "screen_code": "1300",
            "title": "1300 - 주식현재가",
            "text": "# 1300 - 주식현재가",
        }
    ]

    assert build_check_wiki.apply_e2e_observations(records) == 1
    assert records[0]["observation_status"] == "deep_observed"
    assert records[0]["financial_review_status"] == "partial_unapproved"
    assert "실제 화면 관찰은 금융 정의나 산식의 승인을 의미하지 않습니다" in records[0]["text"]


def test_apply_e2e_observations_preserves_non_catalog_screen(tmp_path, monkeypatch) -> None:
    observation = {
        "screen_code": "1515",
        "observation_status": "baseline_observed",
        "callability_status": "verified",
        "title_observed": "저가대비 급등",
        "evidence": ["check-e2e/golden/meta-ranking/1515/manifest.json"],
    }
    (tmp_path / build_check_wiki.E2E_OBSERVATIONS_NAME).write_text(
        json.dumps(observation, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    monkeypatch.setattr(build_check_wiki, "SOURCE_DIR", tmp_path)
    records = []

    assert build_check_wiki.apply_e2e_observations(records) == 1
    assert records[0]["type"] == "observed_screen"
    assert records[0]["mapping_status"] == "observed_not_in_official_catalog"


def test_build_screen_field_records_separates_researched_and_observed_labels(
    tmp_path, monkeypatch
) -> None:
    observation = {
        "screen_code": "1300",
        "observed_fields": ["PER", "현재가"],
        "evidence": ["check-e2e/golden/1300/financial-semantics.json"],
        "field_definitions": [
            {
                "field": "PER",
                "concept": "주가수익비율(PER)",
                "definition": "주가를 주당순이익으로 나눈 값입니다.",
                "formula": "주가 / EPS",
                "unit": "배",
                "definition_status": "authoritative_external",
                "check_field_status": "formula_pending",
                "sources": ["krx"],
            }
        ],
        "semantic_sources": {
            "krx": {"title": "KRX 정보데이터시스템", "url": "https://example.test/krx"}
        },
    }
    (tmp_path / build_check_wiki.E2E_OBSERVATIONS_NAME).write_text(
        json.dumps(observation, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    monkeypatch.setattr(build_check_wiki, "SOURCE_DIR", tmp_path)
    records = [
        {
            "id": "check:screen:1300",
            "type": "screen",
            "screen_code": "1300",
            "title": "1300 - 주식현재가",
            "related_ids": [],
        }
    ]

    assert build_check_wiki.build_screen_field_records(records) == 2
    fields = {
        record["field_label"]: record for record in records if record["type"] == "screen_field"
    }
    assert fields["PER"]["formula"] == "주가 / EPS"
    assert fields["PER"]["review_status"] == "researched"
    assert fields["현재가"]["definition_status"] == "observed_label_only"
    assert fields["현재가"]["review_status"] == "candidate"
    assert set(records[0]["related_ids"]) == {fields["PER"]["id"], fields["현재가"]["id"]}


def test_support_case_merges_multiple_official_contexts(tmp_path, monkeypatch) -> None:
    output = tmp_path / "content" / "check-expert"
    output.mkdir(parents=True)
    monkeypatch.setattr(build_check_wiki, "OUTPUT_DIR", output)
    example = {
        "candidate_id": "manual-candidate:CRM-1",
        "request_text": "조회 방법 문의",
        "action_text": "조회 절차 안내",
        "manual_candidates": ["faq", "procedure"],
        "evidence_locator": "sheet!row:1",
    }

    relative, _ = build_check_wiki.build_support_case(
        example=example,
        topic="주식",
        related_ids=["check:screen:1000"],
        mapping_status="mapped",
    )
    build_check_wiki.build_support_case(
        example=example,
        topic="채권",
        related_ids=["check:screen:3000"],
        mapping_status="mapped",
    )

    text = (output / relative).read_text(encoding="utf-8")
    assert '  - "check:screen:1000"' in text
    assert '  - "check:screen:3000"' in text
    assert '  - "주식"' in text
    assert '  - "채권"' in text
