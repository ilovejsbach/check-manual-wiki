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
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
import yaml
from pypdf import PdfReader
from pypdf.errors import PdfReadError

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path(os.environ.get("CHECK_SRC", ROOT / "sources" / "check-expert")).resolve()
OUTPUT_DIR = ROOT / "content" / "check-expert"
KNOWLEDGE_DIR = ROOT / "knowledge" / "check-expert"
PDF_NAME = "CHECKPlus_Manual.pdf"
CODE_TABLE_ROWS = 750


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
        line = re.sub(r"\s+", " ", raw_line).strip()
        if not line or line == previous:
            continue
        if re.fullmatch(rf"[|\s]*{page_number}[|\s]*", line):
            continue
        line = re.sub(rf"^\|?\s*{page_number}\s*\|?\s*", "", line)
        if line:
            cleaned.append(line)
            previous = line
    return "\n".join(cleaned)


def screen_code(title: str) -> str | None:
    match = re.search(r"(?<!\d)(\d{4})(?!\d)", title)
    return match.group(1) if match else None


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
    body += f"> 출처: `{PDF_NAME}`, PDF {start_page + 1}-{end_page}쪽. 자동 추출 문서이므로 도표와 화면 이미지는 원본을 함께 확인하세요.\n\n"

    headings_by_page: dict[int, list[str]] = {}
    for child in child_headings:
        headings_by_page.setdefault(child.page, []).append(child.title)

    seen_headings: set[str] = set()
    for page in range(start_page, end_page):
        for heading in headings_by_page.get(page, []):
            normalized = heading.strip()
            if normalized and normalized not in seen_headings and normalized != title:
                body += f"## {normalized}\n\n"
                seen_headings.add(normalized)
        text = clean_pdf_text(page_texts[page], page + 1)
        if text:
            paragraphs = re.split(r"\n(?=\d+[.)]\s|[가-힣A-Za-z][^\n]{0,45}$)", text)
            body += "\n\n".join(part.strip() for part in paragraphs if part.strip())
            body += f"\n\n<small>원본 PDF {page + 1}쪽</small>\n\n"
    return body


def build_pdf_wiki() -> dict[str, int]:
    reader = PdfReader(SOURCE_DIR / PDF_NAME)
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
        title = bookmark.title
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

    return {"pdf_pages": len(reader.pages), "pdf_documents": generated, "bookmarks": len(flat)}


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
        rows = normalized_rows(frame)
        sections.append(f"## {sheet}\n")
        seen: set[str] = set()
        for row in rows:
            line = " — ".join(row)
            if line in seen:
                continue
            seen.add(line)
            sections.append(f"- {line}")
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
    document += f"> 출처: `{path.name}`. 그림과 도형은 원본 Excel 파일에서 확인하세요.\n\n"
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
    document += """## 사용 시 주의

- 자동 추출 과정에서 이미지, 도형, 복잡한 표의 배치가 생략될 수 있습니다.
- 실제 화면 조작 전에는 문서에 표시된 원본 PDF 페이지나 Excel 시트를 함께 확인하세요.
- 화면과 데이터는 매뉴얼 작성 이후 변경됐을 수 있습니다.

## 원본 무결성(SHA-256)

"""
    document += hash_lines
    write_text(OUTPUT_DIR / "index.md", document)
    write_text(ROOT / "content" / "index.md", document)


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
        record = {
            "schema_version": "1.0",
            "id": knowledge_id,
            "type": "screen" if code else ("excel" if "excel-premium" in relative else "manual"),
            "title": metadata.get("title", path.stem),
            "aliases": metadata.get("aliases", []),
            "category": metadata.get("category"),
            "screen_code": code,
            "source": metadata.get("source"),
            "source_locator": metadata.get("source_pages")
            or metadata.get("sheet")
            or metadata.get("row_start"),
            "related_screen_codes": related_codes,
            "related_ids": [],
            "markdown_path": relative,
            "text": body,
        }
        records.append(record)

    screen_ids_by_code: dict[str, list[str]] = {}
    for record in records:
        if record["type"] == "screen" and record["screen_code"]:
            screen_ids_by_code.setdefault(str(record["screen_code"]), []).append(str(record["id"]))
    for record in records:
        record["related_ids"] = [
            related_id
            for related_code in record.pop("related_screen_codes")
            for related_id in screen_ids_by_code.get(str(related_code), [])
        ]

    with (KNOWLEDGE_DIR / "knowledge.jsonl").open("w", encoding="utf-8", newline="\n") as stream:
        for record in records:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")

    manifest = {
        "schema_version": "1.0",
        "record_count": len(records),
        "screen_count": sum(record["type"] == "screen" for record in records),
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
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

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
