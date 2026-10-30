# PDF extraction quality

- Record source SHA-256, metadata, page count, bookmark count, and parser warnings.
- Require stable ID, source file, page range, aliases, category, and tags on each page.
- Measure source-page coverage, empty pages, duplicate paths, replacement characters, and size outliers.
- Inspect the first feature, one screen, one table-heavy page, and the final section against the PDF.
- Export matching JSONL records for RAG or call-center ingestion.
- Keep claims traceable to source pages; mark inferred metadata separately.
