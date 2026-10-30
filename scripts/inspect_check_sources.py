from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
from pypdf import PdfReader
from pypdf.errors import PdfReadError

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path(os.environ.get("CHECK_SRC", ROOT / "sources" / "check-expert")).resolve()


def compact(value: object, limit: int = 160) -> str:
    text = " ".join(str(value).split())
    return text[:limit]


def inspect_pdf(path: Path) -> None:
    reader = PdfReader(path)
    print(f"PDF: {path.name}")
    print(f"pages: {len(reader.pages)}")
    print(f"metadata: {reader.metadata}")
    try:
        outline = reader.outline
        destinations: list[tuple[int, object]] = []

        def walk(items: list[object], depth: int = 0) -> None:
            for item in items:
                if isinstance(item, list):
                    walk(item, depth + 1)
                else:
                    destinations.append((depth, item))

        walk(outline)
        print(f"outline_items: {len(destinations)}")
        for depth, item in destinations[:240]:
            try:
                page_number = reader.get_destination_page_number(item) + 1
            except (KeyError, TypeError, ValueError, PdfReadError):
                page_number = "?"
            title = getattr(item, "title", compact(item))
            print(f"  outline: depth={depth} page={page_number} title={compact(title, 220)}")
    except (KeyError, TypeError, ValueError, PdfReadError) as exc:  # pragma: no cover
        print(f"outline_error: {exc}")

    for number in range(min(15, len(reader.pages))):
        text = reader.pages[number].extract_text() or ""
        print(f"  page {number + 1}: chars={len(text)} sample={compact(text, 260)}")


def inspect_workbook(path: Path) -> None:
    print(f"WORKBOOK: {path.name}")
    workbook = pd.ExcelFile(path, engine="calamine")
    for sheet in workbook.sheet_names:
        frame = pd.read_excel(path, sheet_name=sheet, header=None, engine="calamine")
        nonempty = frame.dropna(how="all").dropna(axis=1, how="all")
        sample = []
        for row in nonempty.head(6).itertuples(index=False, name=None):
            sample.append([compact(value, 80) for value in row if pd.notna(value)])
        print(
            f"  sheet={sheet!r} shape={frame.shape} nonempty_shape={nonempty.shape} "
            f"sample={sample[:3]}"
        )


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    inspect_pdf(SOURCE_DIR / "CHECKPlus_Manual.pdf")
    for path in sorted(SOURCE_DIR.glob("*.xls*")):
        inspect_workbook(path)


if __name__ == "__main__":
    main()
