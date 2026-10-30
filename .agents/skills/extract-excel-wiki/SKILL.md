---
name: extract-excel-wiki
description: Convert Excel manuals, lookup sheets, and large code tables into searchable Markdown and machine-readable knowledge records. Use for .xls or .xlsx extraction, sheet-aware manuals, chunked code tables, stable metadata, or completeness validation for Quartz, RAG, and AI call-center systems.
---

# Extract Excel Wiki

Convert workbooks into human-searchable pages and programmatic records while preserving workbook and sheet provenance.

## Workflow

1. Inventory workbooks, sheets, used ranges, merged cells, record counts, and object-heavy layouts.
2. Classify each sheet as narrative manual, lookup table, or mixed layout.
3. Emit narrative cell text in source order, removing only exact duplicates.
4. Detect real table headers; preserve identifiers as text and chunk large tables into bounded pages.
5. Add stable ID, aliases, source file, sheet, row range, function, market, category, and record count.
6. Build human indexes and matching JSONL records using the same IDs.
7. Reconcile source and output counts; inspect first, middle, and final chunks.

## Rules

- Run Python through `uv`; never system Python or global `pip`.
- Prefer `calamine` for read-only `.xls` and `.xlsx` extraction.
- Preserve leading zeros, ordering, and domain labels.
- Do not edit or resave source workbooks.
- State when pictures, shapes, formatting, or formulas require the original workbook.
- Keep pages small enough for Quartz search and RAG chunk retrieval.

For this repository, use `scripts/build_check_wiki.py` and follow [tables.md](references/tables.md).
