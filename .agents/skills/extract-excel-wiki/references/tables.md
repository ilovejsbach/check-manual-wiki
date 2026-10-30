# Workbook-to-wiki rules

- Detect headers from content; do not assume row 1.
- Drop only completely empty rows and columns.
- Preserve text identifiers, source order, and source row bounds.
- Escape Markdown pipes and normalize embedded newlines.
- Chunk large tables by fixed row count and link all chunks from an index.
- Reconcile emitted records with source data rows.
- Export the same records as JSONL with stable IDs and provenance.
- Warn when merged cells, shapes, or images carry unrepresented information.
