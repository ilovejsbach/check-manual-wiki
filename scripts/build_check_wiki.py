from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata
import zipfile
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
import pymupdf
import yaml
from pypdf import PdfReader
from pypdf.errors import PdfReadError

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path(os.environ.get("CHECK_SRC", ROOT / "sources" / "check-expert")).resolve()
OUTPUT_DIR = ROOT / "content" / "check-expert"
KNOWLEDGE_DIR = ROOT / "knowledge" / "check-expert"
PDF_NAME = "CHECKPlus_Manual.pdf"
CODE_TABLE_ROWS = 750
ENRICHMENT_NAME = "manual-enrichment.jsonl"
UNMAPPED_ENRICHMENT_NAME = "manual-enrichment-unmapped.jsonl"
MANUAL_ASSET_DIR = OUTPUT_DIR / "assets" / "manual-pages"
MANUAL_ASSET_SCALE = 1.25
SEMANTIC_STOPWORDS = {
    "check", "expert", "공식", "매뉴얼", "기능", "사용", "설명", "화면", "조회",
    "관련", "정보", "데이터", "메뉴", "방법", "기타", "새로운", "모습", "주요",
}
CASE_TYPE_LABELS = {
    "faq": "질문과 답변",
    "procedure": "사용 절차",
    "troubleshooting": "오류 해결",
    "caution": "주의사항",
    "tip": "활용 팁",
}
CASE_TYPE_PRIORITY = ("troubleshooting", "procedure", "caution", "tip", "faq")


@dataclass
class Bookmark:
    title: str
    page: int
    depth: int
    children: list[Bookmark] = field(default_factory=list)


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def slug(value: str, fallback: str = "document") -> str:
    value = unicodedata.normalize("NFKC", value).strip()
    value = re.sub(r"[<>:\"/\\|?*]", "-", value)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-. ")
    return value[:120] or fallback


def frontmatter(
    *, title: str, description: str, tags: Iterable[str], source: str, extra: dict[str, object]
) -> str:
    lines = [
        "---",
        f"title: {yaml_string(title)}",
        f"description: {yaml_string(description)}",
        "tags:",
    ]
    lines.extend(f"  - {yaml_string(tag)}" for tag in tags)
    lines.append(f"source: {yaml_string(source)}")
    for key, value in extra.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            lines.extend(f"  - {yaml_string(str(item))}" for item in value)
            continue
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        elif isinstance(value, (int, float)):
            rendered = str(value)
        else:
            rendered = yaml_string(str(value))
        lines.append(f"{key}: {rendered}")
    lines.extend(["---", ""])
    return "\n".join(lines)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def source_hashes() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in sorted(SOURCE_DIR.iterdir()):
        if path.is_file():
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            hashes[path.name] = digest
    return hashes


@contextlib.contextmanager
def excel_source_dir() -> Iterable[Path]:
    """Yield readable Excel sources, preferring the immutable ZIP on protected PCs."""
    archive = SOURCE_DIR / "excel-sources.zip"
    if archive.exists():
        with tempfile.TemporaryDirectory(prefix="check-excel-") as temp:
            target = Path(temp)
            with zipfile.ZipFile(archive) as bundle:
                for member in bundle.infolist():
                    name = Path(member.filename).name
                    if (
                        name
                        and name == member.filename
                        and name.lower().endswith((".xls", ".xlsx"))
                    ):
                        bundle.extract(member, target)
            yield target
        return
    yield SOURCE_DIR


def parse_bookmarks(reader: PdfReader) -> list[Bookmark]:
    def parse(items: list[object], depth: int) -> list[Bookmark]:
        result: list[Bookmark] = []
        last: Bookmark | None = None
        for item in items:
            if isinstance(item, list):
                if last is not None:
                    last.children.extend(parse(item, depth + 1))
                continue
            try:
                page = reader.get_destination_page_number(item)
            except (KeyError, TypeError, ValueError, PdfReadError):
                continue
            last = Bookmark(title=str(getattr(item, "title", item)).strip(), page=page, depth=depth)
            result.append(last)
        return result

    return parse(reader.outline, 0)


def flatten_bookmarks(items: list[Bookmark]) -> list[Bookmark]:
    flattened: list[Bookmark] = []
    for item in items:
        flattened.append(item)
        flattened.extend(flatten_bookmarks(item.children))
    return flattened


def clean_pdf_text(text: str, page_number: int) -> str:
    cleaned: list[str] = []
    previous = ""
    for raw_line in text.replace("\x00", "").splitlines():
        line = unicodedata.normalize("NFKC", raw_line.replace("\u00a0", " "))
        line = re.sub(r"[ \t]+", " ", line).strip()
        if not line or line == previous:
            continue
        if re.fullmatch(rf"[|\s]*{page_number}[|\s]*", line):
            continue
        line = re.sub(rf"^\|?\s*{page_number}\s*\|?\s*", "", line)
        if line:
            cleaned.append(line)
            previous = line
    return "\n".join(cleaned)


def render_manual_page_assets(pdf_path: Path) -> int:
    """Render every source page once so screenshots, diagrams and tables are never discarded."""
    MANUAL_ASSET_DIR.mkdir(parents=True, exist_ok=True)
    source_digest = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    digest_path = MANUAL_ASSET_DIR / ".source-sha256"
    if digest_path.exists() and digest_path.read_text(encoding="ascii").strip() != source_digest:
        for asset in MANUAL_ASSET_DIR.glob("page-*.webp"):
            asset.unlink()
    rendered = 0
    with pymupdf.open(pdf_path) as document:
        matrix = pymupdf.Matrix(MANUAL_ASSET_SCALE, MANUAL_ASSET_SCALE)
        for index, page in enumerate(document):
            target = MANUAL_ASSET_DIR / f"page-{index + 1:04d}.webp"
            if target.exists():
                rendered += 1
                continue
            pixmap = page.get_pixmap(matrix=matrix, alpha=False, annots=True)
            pixmap.pil_save(target, format="WEBP", quality=68, method=6)
            rendered += 1
    digest_path.write_text(source_digest + "\n", encoding="ascii")
    return rendered


def build_manual_page_index(page_count: int) -> None:
    document = frontmatter(
        title="CHECK Expert+ 원문 페이지 색인",
        description="공식 매뉴얼 전 페이지의 그림·화면·표를 빠짐없이 확인하는 원문 색인.",
        tags=["CHECK Expert", "공식 매뉴얼", "원문", "이미지", "표"],
        source=PDF_NAME,
        extra={
            "knowledge_id": "check:manual:source-page-index",
            "aliases": ["원문 페이지", "그림 색인", "표 색인", "화면 캡처"],
            "source_pages": f"1-{page_count}",
            "category": "원문",
        },
    )
    document += "# CHECK Expert+ 원문 페이지 색인\n\n"
    document += (
        "텍스트 변환 과정에서 사라질 수 있는 화면 캡처, 도형, 표, 각주를 검증하기 위한 "
        "전 페이지 색인입니다. 각 항목을 펼치면 해당 원문을 그대로 확인할 수 있습니다.\n\n"
    )
    for page in range(1, page_count + 1):
        if (page - 1) % 50 == 0:
            end = min(page + 49, page_count)
            document += f"## {page}-{end}쪽\n\n"
        document += (
            f"<details class=\"source-page\"><summary>원문 PDF {page}쪽 보기</summary>\n\n"
            f"![CHECK Expert+ 원문 PDF {page}쪽](assets/manual-pages/page-{page:04d}.webp)\n\n"
            "</details>\n\n"
        )
    write_text(OUTPUT_DIR / "원문-페이지-색인.md", document)


def screen_code(title: str) -> str | None:
    match = re.search(r"(?<!\d)(\d{4})(?!\d)", title)
    return match.group(1) if match else None


def normalize_screen_title(title: str) -> str:
    code = screen_code(title)
    if not code:
        return title.strip()
    remainder = re.sub(rf"^\s*{code}\s*[-–—:]?\s*", "", title).strip()
    return f"{code} - {remainder}" if remainder else code


def format_pdf_page_text(
    text: str, *, title: str, category: str, rendered_headings: set[str]
) -> str:
    """Remove repeated page furniture and distinguish screen-item numbers from section numbers."""
    normalized_title = re.sub(r"\s*[-–—]\s*", "-", title).strip()
    known_headings = {"화면개요", "화면 개요", "화면설명", "화면 설명", "참고사항", "참고 사항", "관련화면", "관련 화면"}
    emitted_headings: set[str] = set()
    lines: list[str] = []
    for line in text.splitlines():
        compact = line.strip()
        comparable = re.sub(r"\s*[-–—]\s*", "-", compact)
        if not compact or comparable == normalized_title:
            continue
        if re.fullmatch(rf"{re.escape(normalized_title)}\s*\|\s*\d+", comparable):
            continue
        if compact == category or re.fullmatch(rf"\d+\.\s*{re.escape(category)}", compact):
            continue
        if compact in known_headings or compact in rendered_headings:
            canonical = compact.replace("화면개요", "화면 개요").replace("화면설명", "화면 설명").replace("참고사항", "참고 사항").replace("관련화면", "관련 화면")
            if canonical not in emitted_headings:
                lines.append(f"## {canonical}")
                emitted_headings.add(canonical)
            continue
        item = re.fullmatch(r"([1-9]|[1-4]\d)\s+(.+)", compact)
        if item:
            lines.append(f"### 화면 항목 {item.group(1)}. {item.group(2)}")
            continue
        related = re.fullmatch(r"(\d{4})\s*[-–—]\s*(.+)", compact)
        if related:
            lines.append(f"- TR {related.group(1)} — {related.group(2)}")
            continue
        lines.append(compact)
    if lines and lines[-1].startswith("## "):
        trailing_heading = lines.pop()
        lines.insert(0, trailing_heading)
    return "\n".join(lines)


def render_pdf_section(
    *,
    title: str,
    category: str,
    start_page: int,
    end_page: int,
    page_texts: list[str],
    child_headings: list[Bookmark],
    knowledge_id: str | None = None,
) -> str:
    code = screen_code(title)
    knowledge_id = knowledge_id or (
        f"check:screen:{code}" if code else f"check:manual:{slug(category)}:{slug(title)}"
    )
    aliases = [title, re.sub(r"^\d+\.\s*", "", title)]
    if code:
        aliases.extend([code, f"TR{code}", f"화면 {code}"])
    tags = ["CHECK Expert", "공식 매뉴얼", category]
    if code:
        tags.extend(["화면", f"화면-{code}"])
    else:
        tags.append("기능")
    description = f"{title} 사용 설명. 공식 전체 매뉴얼 {start_page + 1}-{end_page}쪽에서 추출."
    body = frontmatter(
        title=title,
        description=description,
        tags=tags,
        source=PDF_NAME,
        extra={
            "knowledge_id": knowledge_id,
            "aliases": list(dict.fromkeys(aliases)),
            "source_pages": f"{start_page + 1}-{end_page}",
            "category": category,
            **({"screen_code": code} if code else {}),
        },
    )
    body += f"# {title}\n\n"
    body += (
        f"> 출처: `{PDF_NAME}`, PDF {start_page + 1}-{end_page}쪽. "
        "검색 가능한 본문과 원문 페이지 이미지를 함께 제공합니다.\n\n"
    )

    headings_by_page: dict[int, list[str]] = {}
    for child in child_headings:
        headings_by_page.setdefault(child.page, []).append(child.title)

    seen_headings: set[str] = set()
    for page in range(start_page, end_page):
        page_headings: set[str] = set()
        for heading in headings_by_page.get(page, []):
            normalized = heading.strip()
            if normalized and normalized not in seen_headings and normalized != title:
                page_headings.add(normalized)
                seen_headings.add(normalized)
        text = clean_pdf_text(page_texts[page], page + 1)
        text = format_pdf_page_text(
            text,
            title=title,
            category=category,
            rendered_headings=page_headings,
        )
        if text:
            paragraphs = re.split(
                r"\n(?=###\s|\d+[.)]\s|[가-힣A-Za-z][^\n]{0,45}$)", text
            )
            body += "\n\n".join(part.strip() for part in paragraphs if part.strip())
            body += f"\n\n<small>원본 PDF {page + 1}쪽</small>\n\n"
        body += (
            f"<details class=\"source-page\"><summary>원문 PDF {page + 1}쪽 보기</summary>\n\n"
            f"![{title} 원문 PDF {page + 1}쪽](assets/manual-pages/page-{page + 1:04d}.webp)\n\n"
            "</details>\n\n"
        )
    return body


def build_pdf_wiki() -> dict[str, int]:
    pdf_path = SOURCE_DIR / PDF_NAME
    reader = PdfReader(pdf_path)
    bookmarks = parse_bookmarks(reader)
    flat = flatten_bookmarks(bookmarks)
    page_texts = [(page.extract_text() or "") for page in reader.pages]

    generated = 0
    category = "기타"
    part_dirs = {
        "파트 I": "새로운-모습",
        "파트 II": "주요-기능",
        "파트 III": "화면",
        "파트 IV": "문의",
    }
    current_part_dir = "기타"
    candidates: list[tuple[Bookmark, str, str]] = []
    for bookmark in flat:
        if bookmark.depth == 0 and bookmark.title.startswith("파트"):
            current_part_dir = next(
                (
                    directory
                    for prefix, directory in part_dirs.items()
                    if bookmark.title.startswith(prefix)
                ),
                "기타",
            )
        elif bookmark.depth == 1:
            category = re.sub(r"^\d+\.\s*", "", bookmark.title).strip()
        elif bookmark.depth == 2:
            candidates.append((bookmark, current_part_dir, category))

    code_counts: dict[str, int] = {}
    for bookmark, _, _ in candidates:
        if code := screen_code(bookmark.title):
            code_counts[code] = code_counts.get(code, 0) + 1

    for index, (bookmark, part_dir, bookmark_category) in enumerate(candidates):
        later_pages = [
            candidate.page
            for candidate, _, _ in candidates[index + 1 :]
            if candidate.page > bookmark.page
        ]
        end_page = min(later_pages, default=len(reader.pages))
        end_page = max(bookmark.page + 1, end_page)
        title = normalize_screen_title(bookmark.title)
        code = screen_code(title)
        filename = f"{code}-{slug(title)}.md" if code else f"{slug(title)}.md"
        category_dir = slug(bookmark_category)
        children = [
            child for child in flatten_bookmarks(bookmark.children) if child.page < end_page
        ]
        document = render_pdf_section(
            title=title,
            category=bookmark_category,
            start_page=bookmark.page,
            end_page=end_page,
            page_texts=page_texts,
            child_headings=children,
            knowledge_id=(
                f"check:screen:{code}:{slug(bookmark_category)}"
                if code and code_counts[code] > 1
                else None
            ),
        )
        write_text(OUTPUT_DIR / part_dir / category_dir / filename, document)
        generated += 1

    rendered_pages = render_manual_page_assets(pdf_path)
    build_manual_page_index(rendered_pages)
    return {
        "pdf_pages": len(reader.pages),
        "pdf_page_assets": rendered_pages,
        "pdf_documents": generated + 1,
        "bookmarks": len(flat),
    }


def normalized_rows(frame: pd.DataFrame) -> list[list[str]]:
    rows: list[list[str]] = []
    for values in frame.itertuples(index=False, name=None):
        cells = []
        for value in values:
            if pd.isna(value):
                continue
            text = re.sub(r"\s+", " ", str(value)).strip()
            if text and text.lower() != "nan":
                cells.append(text)
        if cells:
            rows.append(cells)
    return rows


def build_excel_manual(path: Path, title: str) -> int:
    workbook = pd.ExcelFile(path, engine="calamine")
    sections: list[str] = []
    for sheet in workbook.sheet_names:
        frame = pd.read_excel(path, sheet_name=sheet, header=None, engine="calamine")
        sections.append(f"## {sheet}\n")
        sections.append("| 원문 셀 | 내용 |")
        sections.append("| --- | --- |")
        for row_index, values in enumerate(frame.itertuples(index=False, name=None), start=1):
            for column_index, value in enumerate(values, start=1):
                if pd.isna(value):
                    continue
                text = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", str(value))).strip()
                if not text or text.lower() == "nan":
                    continue
                column = ""
                number = column_index
                while number:
                    number, remainder = divmod(number - 1, 26)
                    column = chr(65 + remainder) + column
                safe = text.replace("|", "\\|")
                sections.append(f"| `{column}{row_index}` | {safe} |")
        sections.append("")

    document = frontmatter(
        title=title,
        description=f"CHECK Excel Premium {title}. 공식 Excel 매뉴얼의 셀 텍스트를 검색용으로 변환.",
        tags=["CHECK Expert", "Excel Premium", "공식 매뉴얼"],
        source=path.name,
        extra={
            "knowledge_id": f"check:excel:manual:{slug(title)}",
            "aliases": [title, f"Excel Premium {title}"],
            "generated": True,
        },
    )
    document += f"# {title}\n\n"
    document += (
        f"> 출처: `{path.name}`. 모든 비어 있지 않은 셀을 원문 좌표와 함께 보존했습니다. "
        "도형·그림의 의미는 CHECK Expert+ 공식 PDF의 대응 원문 페이지와 함께 검증합니다.\n\n"
    )
    document += "\n".join(sections)
    write_text(OUTPUT_DIR / "excel-premium" / "매뉴얼" / f"{slug(title)}.md", document)
    return 1


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    safe_headers = [header.replace("|", "\\|") for header in headers]
    lines = [
        "| " + " | ".join(safe_headers) + " |",
        "| " + " | ".join(["---"] * len(safe_headers)) + " |",
    ]
    for row in rows:
        padded = row + [""] * (len(headers) - len(row))
        cells = [cell.replace("|", "\\|").replace("\n", " ") for cell in padded[: len(headers)]]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_code_workbook(path: Path, kind: str) -> tuple[int, int]:
    workbook = pd.ExcelFile(path, engine="calamine")
    documents = 0
    records = 0
    index_links: list[str] = []
    for sheet in workbook.sheet_names:
        frame = pd.read_excel(path, sheet_name=sheet, header=None, engine="calamine")
        rows = normalized_rows(frame)
        header_index = next(
            (index for index, row in enumerate(rows) if len(row) >= 4),
            0,
        )
        headers = rows[header_index]
        data_rows = [row for row in rows[header_index + 1 :] if len(row) >= 2]
        records += len(data_rows)
        for chunk_number, offset in enumerate(range(0, len(data_rows), CODE_TABLE_ROWS), start=1):
            chunk = data_rows[offset : offset + CODE_TABLE_ROWS]
            title = f"{kind} - {sheet} ({chunk_number})"
            relative = Path("excel-premium") / slug(kind) / slug(sheet) / f"{chunk_number:03d}.md"
            document = frontmatter(
                title=title,
                description=f"CHECK Excel Premium {kind} {sheet} 검색용 코드 테이블 {offset + 1}-{offset + len(chunk)}행.",
                tags=["CHECK Expert", "Excel Premium", kind, str(sheet)],
                source=path.name,
                extra={
                    "knowledge_id": f"check:excel:{slug(kind)}:{slug(sheet)}:{chunk_number:03d}",
                    "aliases": [title, str(sheet), kind],
                    "sheet": sheet,
                    "row_start": offset + 1,
                    "row_end": offset + len(chunk),
                },
            )
            document += f"# {title}\n\n"
            document += f"> 출처: `{path.name}` / `{sheet}` 시트.\n\n"
            document += markdown_table(headers, chunk)
            write_text(OUTPUT_DIR / relative, document)
            index_links.append(f"- [[{relative.with_suffix('').as_posix()}|{title}]]")
            documents += 1

    index = frontmatter(
        title=kind,
        description=f"CHECK Excel Premium {kind} 검색 문서 색인.",
        tags=["CHECK Expert", "Excel Premium", kind],
        source=path.name,
        extra={"record_count": records},
    )
    index += f"# {kind}\n\n총 {records:,}개 레코드를 {documents}개 문서로 나누었습니다.\n\n"
    index += "\n".join(index_links)
    write_text(OUTPUT_DIR / "excel-premium" / slug(kind) / "index.md", index)
    return documents + 1, records


def build_home(stats: dict[str, int], hashes: dict[str, str]) -> None:
    hash_lines = "\n".join(f"- `{name}`: `{digest}`" for name, digest in hashes.items())
    document = frontmatter(
        title="CHECK Expert LLM Wiki",
        description="CHECK Expert+와 Excel Premium 공식 매뉴얼을 검색·질의하기 위한 로컬 위키.",
        tags=["CHECK Expert", "LLM Wiki"],
        source="KOSCOM CHECK 공식 매뉴얼",
        extra={"generated": True},
    )
    document += """# CHECK Expert LLM Wiki

이 위키는 CHECK Expert+ 공식 전체 매뉴얼과 Excel Premium 자료를 Markdown으로 변환한 검색·질의용 지식베이스입니다.

## 바로가기

- [[check-expert/화면번호-색인|화면번호로 찾기]]
- [[check-expert/업무-기능-색인|업무·기능으로 찾기]]
- [[check-expert/excel-premium/매뉴얼|Excel Premium 매뉴얼]]
- [[check-expert/excel-premium/종목코드표|종목코드표]]
- [[check-expert/excel-premium/항목코드표|항목코드표]]
- [[check-expert/운영-보강/index|실사용 보강 후보]]

상단 검색에서 화면번호(`1300`), TR 형식(`TR1300`), 화면명 또는 업무 용어를 입력할 수 있습니다.

## AI·프로그램 연동

- [[check-expert/api/llms.txt|LLM 사용 안내]]
- [[check-expert/api/manifest.json|지식베이스 manifest]]
- [[check-expert/api/knowledge.jsonl|전체 JSONL 지식 레코드]]
- [[check-expert/다운로드|저장·다운로드]]

응답에는 `id`, `source`, `source_locator`를 함께 보존해 근거를 추적하세요.

## 생성 현황

"""
    document += f"- PDF: {stats['pdf_pages']:,}쪽, 북마크 {stats['bookmarks']:,}개\n"
    document += f"- 화면·기능 문서: {stats['pdf_documents']:,}개\n"
    document += f"- Excel 문서: {stats['excel_documents']:,}개\n"
    document += f"- 코드 레코드: {stats['code_records']:,}개\n\n"
    document += f"- 실사용 보강 문서: {stats.get('enrichment_documents', 0):,}개\n\n"
    document += """## 사용 시 주의

- 자동 추출 과정에서 이미지, 도형, 복잡한 표의 배치가 생략될 수 있습니다.
- 실제 화면 조작 전에는 문서에 표시된 원본 PDF 페이지나 Excel 시트를 함께 확인하세요.
- 화면과 데이터는 매뉴얼 작성 이후 변경됐을 수 있습니다.

## 원본 무결성(SHA-256)

"""
    document += hash_lines
    write_text(OUTPUT_DIR / "index.md", document)
    write_text(ROOT / "content" / "index.md", document)


def _single_line(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def clean_case_request(value: object) -> str:
    text = _single_line(value)
    inquiry = re.search(r"(?:^|\s)-?\s*문의\s*내용\s*:\s*(.+)$", text, re.IGNORECASE)
    if inquiry:
        return inquiry.group(1).strip()
    return text


def primary_case_type(example: dict[str, object]) -> str:
    facets = [str(item) for item in example.get("manual_candidates", [])]
    request = clean_case_request(example.get("request_text"))
    action = _single_line(example.get("action_text"))
    combined = f"{request} {action}"
    if "troubleshooting" in facets and re.search(
        r"오류|에러|안\s*됨|않|실패|멈춤|비활성|재설치|권한|장애", combined
    ):
        return "troubleshooting"
    if "procedure" in facets and re.search(
        r"방법|어떻게|조회|설정|설치|등록|변경|입력|사용|안내", combined
    ):
        return "procedure"
    for case_type in CASE_TYPE_PRIORITY:
        if case_type in facets:
            return case_type
    return "faq"


def build_support_case(
    *,
    example: dict[str, object],
    topic: str,
    related_ids: list[str],
    mapping_status: str,
) -> tuple[Path, str]:
    case_type = primary_case_type(example)
    label = CASE_TYPE_LABELS[case_type]
    request = clean_case_request(example.get("request_text")) or "문의 내용 미기재"
    action = _single_line(example.get("action_text")) or "대응 내용 미기재"
    candidate_id = _single_line(example.get("candidate_id"))
    evidence_locator = _single_line(example.get("evidence_locator"))
    stable_seed = candidate_id or f"{evidence_locator}|{request}|{action}"
    case_hash = hashlib.sha256(stable_seed.encode("utf-8")).hexdigest()[:16]
    knowledge_id = f"check:support-case:{case_hash}"
    title_text = request if len(request) <= 72 else request[:69].rstrip() + "…"
    title = f"{label} — {title_text}"
    relative = Path("문의-대응") / case_type / f"{case_hash}-{slug(title_text)}.md"
    facets = [str(item) for item in example.get("manual_candidates", [])]
    target_path = OUTPUT_DIR / relative
    topics = [topic]
    if target_path.exists():
        existing_raw = target_path.read_text(encoding="utf-8")
        existing_match = re.match(r"^---\n(.*?)\n---\n?", existing_raw, re.DOTALL)
        if existing_match:
            existing = yaml.safe_load(existing_match.group(1)) or {}
            related_ids = list(
                dict.fromkeys(
                    [str(item) for item in existing.get("related_ids", [])] + related_ids
                )
            )
            topics = list(
                dict.fromkeys(
                    [str(item) for item in existing.get("case_topics", [])]
                    + [str(existing.get("case_topic") or ""), topic]
                )
            )
            topics = [item for item in topics if item]
            if existing.get("mapping_status") == "mapped":
                mapping_status = "mapped"
    topic_label = ", ".join(topics)
    document = frontmatter(
        title=title,
        description=f"{topic_label} 관련 비식별 문의와 당시 대응 기록을 분리한 {label} 검수 후보.",
        tags=["CHECK Expert", "문의 대응", label, "검수 필요", *topics[:5]],
        source=ENRICHMENT_NAME if mapping_status == "mapped" else UNMAPPED_ENRICHMENT_NAME,
        extra={
            "knowledge_id": knowledge_id,
            "document_type": "support_case",
            "case_type": case_type,
            "case_facets": facets,
            "case_topic": topics[0],
            "case_topics": topics,
            "related_ids": related_ids,
            "review_status": "candidate",
            "mapping_status": mapping_status,
            "source_locator": evidence_locator,
            "candidate_id": candidate_id or case_hash,
        },
    )
    document += f"# {title}\n\n"
    document += (
        "> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 "
        "의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.\n\n"
    )
    document += "## 사용자가 겪은 상황\n\n"
    document += f"{request}\n\n"
    document += "## 당시 대응\n\n"
    document += f"{action}\n\n"
    document += "## 의미 분류\n\n"
    document += f"- 대표 유형: **{label}**\n"
    document += f"- 함께 볼 유형: {', '.join(CASE_TYPE_LABELS.get(item, item) for item in facets)}\n"
    document += f"- 업무·주제: {topic_label}\n"
    document += f"- 공식 문서 연결: {'연결됨' if mapping_status == 'mapped' else '분류 대기'}\n"
    document += f"- 증거 위치: `{evidence_locator}`\n\n"
    document += "## 검증할 사항\n\n"
    document += (
        "- [ ] 현재 버전에서도 같은 상황이 재현되는가\n"
        "- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가\n"
        "- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가\n"
        "- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가\n"
    )
    write_text(target_path, document)
    return relative, knowledge_id


def build_manual_enrichment() -> int:
    """Create reviewable companion pages from privacy-screened customer signals."""
    source = SOURCE_DIR / ENRICHMENT_NAME
    if not source.exists():
        return 0
    target_metadata: dict[str, dict[str, object]] = {}
    for path in OUTPUT_DIR.rglob("*.md"):
        raw = path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n?", raw, re.DOTALL)
        if not match:
            continue
        metadata = yaml.safe_load(match.group(1)) or {}
        if metadata.get("knowledge_id"):
            target_metadata[str(metadata["knowledge_id"])] = {
                "title": metadata.get("title", path.stem),
                "path": path.relative_to(ROOT / "content").with_suffix("").as_posix(),
            }

    summaries = [
        json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line
    ]
    links: list[str] = []
    case_links: dict[str, list[str]] = {key: [] for key in CASE_TYPE_LABELS}
    documents = 0
    for summary in summaries:
        target_id = str(summary.get("target_knowledge_id") or "")
        target = target_metadata.get(target_id)
        if not target:
            continue
        target_title = str(target["title"])
        relative = Path("문의-대응") / "화면별" / f"{slug(target_id.replace(':', '-'))}.md"
        knowledge_id = f"check:enrichment:{target_id.removeprefix('check:')}"
        document = frontmatter(
            title=f"문의 대응 사례 묶음 — {target_title}",
            description=f"{target_title} 관련 비식별 문의를 유형별 사례로 연결한 검수 묶음.",
            tags=["CHECK Expert", "문의 대응", "사례 묶음", "검수 필요", target_title],
            source=ENRICHMENT_NAME,
            extra={
                "knowledge_id": knowledge_id,
                "related_ids": [target_id],
                "review_status": "candidate",
                "signal_count": int(summary.get("signal_count", 0)),
                "source_locator": f"target:{target_id}",
            },
        )
        document += f"# 문의 대응 사례 묶음 — {target_title}\n\n"
        document += (
            f"> 공식 문서: [[{target['path']}|{target_title}]]\n\n"
            "> 아래 내용은 비식별 고객 문의·운영 기록에서 추출한 **검수 전 후보**입니다. "
            "공식 금융 정의나 현재 CHECK 동작으로 자동 승인되지 않습니다.\n\n"
        )
        document += "## 수요 요약\n\n"
        document += f"- 관련 신호: {int(summary.get('signal_count', 0)):,}건\n"
        document += (
            f"- 중복 제거 그룹: {int(summary.get('duplicate_group_count', 0)):,}개\n"
        )
        candidate_counts = summary.get("manual_candidate_counts", {})
        if candidate_counts:
            labels = {
                "faq": "FAQ",
                "procedure": "절차",
                "troubleshooting": "문제 해결",
                "caution": "주의사항",
                "tip": "활용 팁",
            }
            rendered = ", ".join(
                f"{labels.get(kind, kind)} {count:,}건"
                for kind, count in sorted(candidate_counts.items(), key=lambda item: -item[1])
            )
            document += f"- 후보 유형: {rendered}\n"
        topics = summary.get("topic_counts", {})
        if topics:
            document += "- 주요 주제: " + ", ".join(
                f"{_single_line(topic)} ({count:,})" for topic, count in list(topics.items())[:8]
            ) + "\n"

        document += "\n## 문의·대응 사례\n\n"
        for index, example in enumerate(summary.get("examples", []), start=1):
            case_relative, _ = build_support_case(
                example=example,
                topic=target_title,
                related_ids=[target_id, knowledge_id],
                mapping_status="mapped",
            )
            case_type = primary_case_type(example)
            case_links[case_type].append(
                f"- [[check-expert/{case_relative.with_suffix('').as_posix()}|"
                f"{_single_line(example.get('request_text'))[:100]}]]"
            )
            documents += 1
            request = _single_line(example.get("request_text")) or "문의 내용 미기재"
            action = _single_line(example.get("action_text")) or "대응 내용 미기재"
            document += f"### 후보 {index}\n\n"
            document += f"- 고객 질문·증상: {request}\n"
            document += f"- 당시 대응 기록: {action}\n"
            document += f"- 후보 유형: {', '.join(example.get('manual_candidates', []))}\n"
            document += f"- 증거 위치: `{_single_line(example.get('evidence_locator'))}`\n"
            document += "- 상태: `candidate` — 공식 문서 및 실제 동작 교차 검증 필요\n\n"
        document += "## 승인 게이트\n\n"
        document += (
            "- [ ] 공식 매뉴얼의 정의·절차와 일치하는가\n"
            "- [ ] 현재 CHECK 또는 Excel Premium에서 재현되는가\n"
            "- [ ] 금융 해석이 필요한 문장은 금융 전문가가 검토했는가\n"
            "- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가\n"
            "- [ ] 충돌하거나 미확인된 내용을 공식 사실과 분리했는가\n"
        )
        write_text(OUTPUT_DIR / relative, document)
        links.append(
            f"- **{int(summary.get('signal_count', 0)):,}건** — "
            f"[[check-expert/{relative.with_suffix('').as_posix()}|{target_title}]]"
        )
        documents += 1

    index = frontmatter(
        title="문의 대응 지식",
        description="비식별 문의를 질문과 답변·사용 절차·오류 해결·주의사항·활용 팁으로 탐색하는 검수 대기 색인.",
        tags=["CHECK Expert", "문의 대응", "검수 필요"],
        source=ENRICHMENT_NAME,
        extra={"knowledge_id": "check:enrichment:index", "review_status": "candidate"},
    )
    index += "# 문의 대응 지식\n\n"
    index += (
        "문의 사례를 화면별 한 묶음으로만 보지 않고 질문과 답변·사용 절차·오류 해결·주의사항·활용 팁으로 "
        "분리했습니다. 모든 항목은 공식 매뉴얼과 실제 동작 검증 전까지 `candidate` 상태입니다.\n\n"
    )
    index += "## 문의 유형으로 찾기\n\n"
    for case_type, label in CASE_TYPE_LABELS.items():
        index += f"- [[check-expert/문의-대응/{case_type}/index|{label}]] ({len(case_links[case_type]):,}건)\n"
        type_index = frontmatter(
            title=f"문의 대응 — {label}",
            description=f"비식별 문의 대응 사례 중 {label} 유형의 검수 후보 색인.",
            tags=["CHECK Expert", "문의 대응", label, "검수 필요"],
            source=ENRICHMENT_NAME,
            extra={
                "knowledge_id": f"check:support-case:index:{case_type}",
                "document_type": "support_case_index",
                "case_type": case_type,
                "review_status": "candidate",
            },
        )
        type_index += f"# 문의 대응 — {label}\n\n"
        type_index += "공식 문서와 제품 동작 검증 전의 대표 사례입니다.\n\n"
        type_index += "\n".join(case_links[case_type])
        write_text(OUTPUT_DIR / "문의-대응" / case_type / "index.md", type_index)
        documents += 1
    index += "\n## 화면별 사례 묶음\n\n"
    if (SOURCE_DIR / UNMAPPED_ENRICHMENT_NAME).exists():
        index += "- [[check-expert/문의-대응/분류-대기/index|공식 문서에 아직 연결되지 않은 사례]]\n\n"
    index += "\n".join(links)
    write_text(OUTPUT_DIR / "문의-대응" / "index.md", index)
    return documents + 1


def build_unmapped_enrichment() -> int:
    """Preserve every unmapped signal as a topic-level human review queue."""
    source = SOURCE_DIR / UNMAPPED_ENRICHMENT_NAME
    if not source.exists():
        return 0
    summaries = [
        json.loads(line) for line in source.read_text(encoding="utf-8").splitlines() if line
    ]
    links: list[str] = []
    documents = 0
    for summary in summaries:
        topic = _single_line(summary.get("topic")) or "미분류"
        topic_hash = hashlib.sha256(topic.encode("utf-8")).hexdigest()[:12]
        collection_id = f"check:enrichment:unmapped:{topic_hash}"
        relative = Path("문의-대응") / "분류-대기" / f"{topic_hash}-{slug(topic)}.md"
        document = frontmatter(
            title=f"공식 문서 연결 대기 — {topic}",
            description=f"기존 화면·기능 문서에 아직 연결되지 않은 {topic} 관련 문의 사례 묶음.",
            tags=["CHECK Expert", "문의 대응", "분류 대기", "검수 필요", topic],
            source=UNMAPPED_ENRICHMENT_NAME,
            extra={
                "knowledge_id": collection_id,
                "review_status": "candidate",
                "mapping_status": "unmapped",
                "signal_count": int(summary.get("signal_count", 0)),
                "source_locator": f"topic:{topic}",
            },
        )
        document += f"# 공식 문서 연결 대기 — {topic}\n\n"
        document += (
            "> 기존 위키 화면·기능에 자동 연결되지 않은 비식별 신호입니다. "
            "삭제하거나 임의 연결하지 않고 사람 검수 대기 상태로 보존합니다.\n\n"
        )
        document += f"- 관련 신호: {int(summary.get('signal_count', 0)):,}건\n"
        document += "- 상태: `candidate` / `unmapped`\n"
        counts = summary.get("manual_candidate_counts", {})
        if counts:
            document += "- 후보 유형: " + ", ".join(
                f"{kind} {count:,}건"
                for kind, count in sorted(counts.items(), key=lambda item: -item[1])
            ) + "\n"
        document += "\n## 대표 사례\n\n"
        for index, example in enumerate(summary.get("examples", []), start=1):
            build_support_case(
                example=example,
                topic=topic,
                related_ids=[collection_id],
                mapping_status="unmapped",
            )
            documents += 1
            document += f"### 후보 {index}\n\n"
            document += (
                f"- 고객 질문·증상: {_single_line(example.get('request_text')) or '미기재'}\n"
            )
            document += (
                f"- 당시 대응 기록: {_single_line(example.get('action_text')) or '미기재'}\n"
            )
            document += f"- 증거 위치: `{_single_line(example.get('evidence_locator'))}`\n"
            document += "- 검토 과제: 연결할 기존 문서 또는 신규 문서 필요 여부 결정\n\n"
        document += "## 분류 게이트\n\n"
        document += (
            "- [ ] 화면번호·기능명·업무 용어를 추가 확인했는가\n"
            "- [ ] 기존 문서 연결과 신규 문서 생성 중 적절한 경로를 결정했는가\n"
            "- [ ] 공식 근거 또는 실제 동작 증거를 확보했는가\n"
            "- [ ] 식별정보와 내부 전용 정보가 남아 있지 않은가\n"
        )
        write_text(OUTPUT_DIR / relative, document)
        links.append(
            f"- **{int(summary.get('signal_count', 0)):,}건** — "
            f"[[check-expert/{relative.with_suffix('').as_posix()}|{topic}]]"
        )
        documents += 1

    index = frontmatter(
        title="공식 문서 연결 대기",
        description="화면·기능 문서에 아직 연결되지 않은 비식별 문의 사례의 주제별 검수 대기열.",
        tags=["CHECK Expert", "문의 대응", "분류 대기", "검수 필요"],
        source=UNMAPPED_ENRICHMENT_NAME,
        extra={
            "knowledge_id": "check:enrichment:unmapped:index",
            "review_status": "candidate",
            "mapping_status": "unmapped",
        },
    )
    index += "# 공식 문서 연결 대기\n\n"
    index += (
        "자동 매핑의 불확실성을 숨기지 않고 주제별 검수 대기열로 보존합니다. "
        "각 문서는 기존 문서 연결 또는 신규 공식 문서 작성 여부를 결정하기 위한 입력입니다.\n\n"
    )
    index += "\n".join(links)
    write_text(OUTPUT_DIR / "문의-대응" / "분류-대기" / "index.md", index)
    return documents + 1


def rebuild_support_case_indexes() -> None:
    links: dict[str, list[str]] = {key: [] for key in CASE_TYPE_LABELS}
    for path in (OUTPUT_DIR / "문의-대응").rglob("*.md"):
        raw = path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n?", raw, re.DOTALL)
        if not match:
            continue
        metadata = yaml.safe_load(match.group(1)) or {}
        if metadata.get("document_type") != "support_case":
            continue
        case_type = str(metadata.get("case_type") or "faq")
        relative = path.relative_to(ROOT / "content").with_suffix("").as_posix()
        links.setdefault(case_type, []).append(
            f"- [[{relative}|{metadata.get('title', path.stem)}]]"
        )
    for case_type, label in CASE_TYPE_LABELS.items():
        document = frontmatter(
            title=f"문의 대응 — {label}",
            description=f"비식별 문의 대응 사례 중 {label} 유형의 검수 후보 색인.",
            tags=["CHECK Expert", "문의 대응", label, "검수 필요"],
            source=f"{ENRICHMENT_NAME}; {UNMAPPED_ENRICHMENT_NAME}",
            extra={
                "knowledge_id": f"check:support-case:index:{case_type}",
                "document_type": "support_case_index",
                "case_type": case_type,
                "review_status": "candidate",
                "signal_count": len(links.get(case_type, [])),
            },
        )
        document += f"# 문의 대응 — {label}\n\n"
        document += "공식 문서와 제품 동작 검증 전의 대표 사례입니다.\n\n"
        document += "\n".join(sorted(links.get(case_type, [])))
        write_text(OUTPUT_DIR / "문의-대응" / case_type / "index.md", document)


def semantic_tokens(record: dict[str, object]) -> set[str]:
    values = [
        str(record.get("title") or ""),
        str(record.get("category") or ""),
        " ".join(str(item) for item in record.get("aliases", [])),
        str(record.get("case_topic") or ""),
        " ".join(str(item) for item in record.get("case_topics", [])),
        " ".join(str(item) for item in record.get("case_facets", [])),
    ]
    tokens = re.findall(r"[0-9A-Za-z가-힣]{2,}", unicodedata.normalize("NFKC", " ".join(values)).lower())
    return {token for token in tokens if token not in SEMANTIC_STOPWORDS}


def add_relationship(
    record: dict[str, object], target_id: str, relation_type: str, label: str
) -> None:
    if target_id == record["id"]:
        return
    relationships = record.setdefault("relationships", [])
    assert isinstance(relationships, list)
    if any(item.get("target_id") == target_id for item in relationships):
        return
    relationships.append({"target_id": target_id, "type": relation_type, "label": label})


def enrich_relationships(records: list[dict[str, object]]) -> None:
    """Build typed, bounded links instead of an unexplained flat related-ID list."""
    by_id = {str(record["id"]): record for record in records}
    for record in records:
        record["relationships"] = []
        for target_id in record.get("related_ids", []):
            if str(record["id"]).startswith("check:support-case:"):
                relation_type, label = "case_context", "이 문의가 연결된 문서"
            elif str(target_id).startswith("check:support-case:"):
                relation_type, label = "support_case", "관련 문의 대응 사례"
            elif str(record["id"]).startswith("check:enrichment:") or str(
                target_id
            ).startswith("check:enrichment:"):
                relation_type, label = "case_collection", "문의 사례 묶음"
            else:
                relation_type, label = "screen_reference", "본문에서 언급"
            add_relationship(record, str(target_id), relation_type, label)

    manual_records = [
        record
        for record in records
        if record.get("source") == PDF_NAME
        and re.fullmatch(r"\d+(?:-\d+)?", str(record.get("source_locator") or ""))
    ]
    manual_records.sort(key=lambda item: int(str(item["source_locator"]).split("-")[0]))
    for index, record in enumerate(manual_records):
        if index:
            add_relationship(record, str(manual_records[index - 1]["id"]), "previous", "매뉴얼 이전 항목")
        if index + 1 < len(manual_records):
            add_relationship(record, str(manual_records[index + 1]["id"]), "next", "매뉴얼 다음 항목")

    token_map = {str(record["id"]): semantic_tokens(record) for record in records}
    document_frequency = Counter(token for tokens in token_map.values() for token in tokens)
    for record in records:
        source_tokens = token_map[str(record["id"])]
        if not source_tokens:
            continue
        scores: list[tuple[float, str]] = []
        for candidate in records:
            if candidate["id"] == record["id"]:
                continue
            candidate_tokens = token_map[str(candidate["id"])]
            shared = source_tokens & candidate_tokens
            if not shared:
                continue
            weighted = sum(1 / max(1, document_frequency[token]) for token in shared)
            category_bonus = 0.15 if record.get("category") == candidate.get("category") else 0
            score = weighted / max(1, len(source_tokens | candidate_tokens)) + category_bonus
            if score > 0.04:
                scores.append((score, str(candidate["id"])))
        existing = {item["target_id"] for item in record["relationships"]}
        added = 0
        for _, target_id in sorted(scores, reverse=True):
            if target_id in existing:
                continue
            add_relationship(record, target_id, "semantic", "같은 업무·용어")
            added += 1
            if added == 3:
                break

    for record in records:
        record["relationships"] = [
            item for item in record["relationships"] if item["target_id"] in by_id
        ]
        record["related_ids"] = [item["target_id"] for item in record["relationships"]]


def export_knowledge() -> dict[str, int]:
    """Export generated Markdown as stable JSONL records and human navigation indexes."""
    if KNOWLEDGE_DIR.exists():
        shutil.rmtree(KNOWLEDGE_DIR)
    KNOWLEDGE_DIR.mkdir(parents=True)

    records: list[dict[str, object]] = []
    for path in sorted(OUTPUT_DIR.rglob("*.md")):
        raw = path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n?(.*)$", raw, re.DOTALL)
        if not match:
            continue
        metadata = yaml.safe_load(match.group(1)) or {}
        body = match.group(2).strip()
        relative = path.relative_to(ROOT / "content").as_posix()
        code = str(metadata.get("screen_code", "")) or None
        knowledge_id = (
            metadata.get("knowledge_id")
            or f"check:doc:{path.relative_to(OUTPUT_DIR).with_suffix('').as_posix()}"
        )
        related_codes = sorted(
            {
                found
                for found in re.findall(
                    r"(?im)(?:^\s*[-*]?\s*|화면\s*)(\d{4})\s*(?:[-–—:(]|번)", body
                )
                if found != code
            }
        )
        metadata_related_ids = [str(item) for item in metadata.get("related_ids", [])]
        document_type = metadata.get("document_type")
        record = {
            "schema_version": "1.0",
            "id": knowledge_id,
            "type": document_type
            or ("screen" if code else ("excel" if "excel-premium" in relative else "manual")),
            "title": metadata.get("title", path.stem),
            "aliases": metadata.get("aliases", []),
            "category": metadata.get("category"),
            "screen_code": code,
            "source": metadata.get("source"),
            "source_locator": metadata.get("source_pages")
            or metadata.get("sheet")
            or metadata.get("row_start")
            or metadata.get("source_locator"),
            "review_status": metadata.get("review_status"),
            "mapping_status": metadata.get("mapping_status"),
            "signal_count": metadata.get("signal_count"),
            "case_type": metadata.get("case_type"),
            "case_facets": metadata.get("case_facets", []),
            "case_topic": metadata.get("case_topic"),
            "case_topics": metadata.get("case_topics", []),
            "candidate_id": metadata.get("candidate_id"),
            "related_screen_codes": related_codes,
            "related_ids": metadata_related_ids,
            "markdown_path": relative,
            "text": body,
        }
        records.append(record)

    screen_ids_by_code: dict[str, list[str]] = {}
    for record in records:
        if record["type"] == "screen" and record["screen_code"]:
            screen_ids_by_code.setdefault(str(record["screen_code"]), []).append(str(record["id"]))
    for record in records:
        detected_related_ids = [
            related_id
            for related_code in record.pop("related_screen_codes")
            for related_id in screen_ids_by_code.get(str(related_code), [])
        ]
        record["related_ids"] = sorted(set(record["related_ids"] + detected_related_ids))

    records_by_id = {str(record["id"]): record for record in records}
    for record in records:
        if not str(record["id"]).startswith(("check:enrichment:", "check:support-case:")):
            continue
        for target_id in record["related_ids"]:
            target = records_by_id.get(str(target_id))
            if target is not None:
                target["related_ids"] = sorted(set(target["related_ids"] + [record["id"]]))

    enrich_relationships(records)

    with (KNOWLEDGE_DIR / "knowledge.jsonl").open("w", encoding="utf-8", newline="\n") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")

    case_type_counts = Counter(
        str(record.get("case_type"))
        for record in records
        if record.get("type") == "support_case"
    )
    manifest = {
        "schema_version": "1.0",
        "record_count": len(records),
        "screen_count": sum(record["type"] == "screen" for record in records),
        "support_case_count": sum(record["type"] == "support_case" for record in records),
        "support_case_type_counts": dict(sorted(case_type_counts.items())),
        "unmapped_support_case_count": sum(
            record["type"] == "support_case" and record.get("mapping_status") == "unmapped"
            for record in records
        ),
        "source_hashes": source_hashes(),
    }
    manifest_text = json.dumps(manifest, ensure_ascii=False, indent=2)
    write_text(KNOWLEDGE_DIR / "manifest.json", manifest_text)

    api_dir = OUTPUT_DIR / "api"
    api_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(KNOWLEDGE_DIR / "knowledge.jsonl", api_dir / "knowledge.jsonl")
    write_text(api_dir / "manifest.json", manifest_text)
    llms_text = """# CHECK Expert LLM Wiki

Official CHECK Expert+ and Excel Premium manuals converted into a source-traceable knowledge base.

## Human indexes

- /check-expert/화면번호-색인
- /check-expert/업무-기능-색인
- /check-expert/excel-premium/매뉴얼

## Machine-readable resources

- /check-expert/api/manifest.json
- /check-expert/api/knowledge.jsonl
- /check-expert/api/check-manual-wiki-data.zip

Each JSONL record contains id, type, title, aliases, category, screen_code, source,
source_locator, related_ids, markdown_path, and text. Cite id plus source_locator in answers.
For an exact screen query, prefer screen_code or aliases before full-text matching.
"""
    write_text(api_dir / "llms.txt", llms_text)

    screens = sorted(
        (record for record in records if record["type"] == "screen"),
        key=lambda record: str(record["screen_code"]),
    )
    screen_lines = ["# 화면번호 색인", "", "화면번호로 CHECK Expert 도움말을 찾습니다.", ""]
    for record in screens:
        target = Path(str(record["markdown_path"])).with_suffix("").as_posix()
        screen_lines.append(f"- **{record['screen_code']}** — [[{target}|{record['title']}]]")
    write_text(OUTPUT_DIR / "화면번호-색인.md", "\n".join(screen_lines))

    grouped: dict[str, list[dict[str, object]]] = {}
    for record in records:
        category = str(record.get("category") or record["type"])
        grouped.setdefault(category, []).append(record)
    category_lines = ["# 업무·기능 색인", "", "시장과 업무 분류별로 문서를 찾습니다.", ""]
    for category in sorted(grouped):
        category_lines.extend([f"## {category}", ""])
        for record in grouped[category]:
            target = Path(str(record["markdown_path"])).with_suffix("").as_posix()
            category_lines.append(f"- [[{target}|{record['title']}]]")
        category_lines.append("")
    write_text(OUTPUT_DIR / "업무-기능-색인.md", "\n".join(category_lines))
    return {"knowledge_records": len(records), "screen_records": len(screens)}


def build_download_page() -> None:
    download_page = frontmatter(
        title="저장·다운로드",
        description="CHECK Manual Wiki를 오프라인 또는 프로그램 연동용으로 저장합니다.",
        tags=["CHECK Expert", "다운로드", "오프라인"],
        source="CHECK Manual Wiki",
        extra={"knowledge_id": "check:guide:downloads"},
    )
    download_page += """# 저장·다운로드

## 전체 자료

- [Markdown·JSONL 전체 ZIP](api/check-manual-wiki-data.zip)
- [LLM/RAG용 JSONL](api/knowledge.jsonl)
- [버전·원본 무결성 manifest](api/manifest.json)
- [LLM 사용 안내](api/llms.txt)

ZIP에는 사람용 Markdown, 기계 판독 JSONL, 스키마 문서가 들어 있습니다. 원본 PDF와 Excel은
포함하지 않으며 각 레코드의 `source`와 `source_locator`로 근거를 추적할 수 있습니다.

## 현재 문서 저장

브라우저의 **인쇄 → PDF로 저장** 기능으로 현재 문서를 보존할 수 있습니다. 원문 데이터가
필요하면 위 JSONL 또는 전체 ZIP을 사용하세요.
"""
    write_text(OUTPUT_DIR / "다운로드.md", download_page)


def build_download_archive() -> None:
    """Create a reproducible offline archive for people and downstream programs."""
    api_dir = OUTPUT_DIR / "api"
    archive_path = api_dir / "check-manual-wiki-data.zip"
    files: list[tuple[Path, str]] = []
    for path in sorted(OUTPUT_DIR.rglob("*.md")):
        files.append((path, f"content/{path.relative_to(ROOT / 'content').as_posix()}"))
    for path in sorted(KNOWLEDGE_DIR.glob("*")):
        if path.is_file():
            files.append((path, f"knowledge/check-expert/{path.name}"))
    for path in [ROOT / "docs" / "check-expert-knowledge-schema.md", ROOT / "README.md"]:
        if path.exists():
            files.append((path, path.relative_to(ROOT).as_posix()))

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, archive_name in files:
            info = zipfile.ZipInfo(archive_name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def build() -> dict[str, int]:
    if OUTPUT_DIR.exists():
        for path in OUTPUT_DIR.iterdir():
            if path.name == "assets":
                continue
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    stats = build_pdf_wiki()
    excel_documents = 0
    code_documents = 0
    code_records = 0
    with excel_source_dir() as excel_dir:
        manual_specs = [
            ("excel-manual1_menu_template.xls", "메뉴와 템플릿"),
            ("excel-manual2_function.xls", "함수 설명"),
            ("excel-manual3_askWizard.xls", "조회마법사"),
            ("excel-manual4_ezChart.xls", "Ez 차트"),
        ]
        for filename, title in manual_specs:
            excel_documents += build_excel_manual(excel_dir / filename, title)

        for filename, kind in [
            ("JongMokCodeTable_20140616_Uodate02.xlsx", "종목코드표"),
            ("HangMokCodeTable_ExcelPremium_update01.xlsx", "항목코드표"),
        ]:
            documents, records = build_code_workbook(excel_dir / filename, kind)
            code_documents += documents
            code_records += records

    stats["excel_documents"] = excel_documents + code_documents
    stats["code_records"] = code_records
    stats["enrichment_documents"] = build_manual_enrichment() + build_unmapped_enrichment()
    rebuild_support_case_indexes()
    build_home(stats, source_hashes())
    build_download_page()
    stats.update(export_knowledge())
    build_download_archive()
    return stats


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Build CHECK Expert Markdown for Quartz")
    parser.add_argument("--json", action="store_true", help="Print build statistics as JSON")
    args = parser.parse_args()
    stats = build()
    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print(stats)


if __name__ == "__main__":
    main()
