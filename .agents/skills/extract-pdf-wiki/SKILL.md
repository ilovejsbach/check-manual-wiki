---
name: extract-pdf-wiki
description: Extract bookmarked manuals and reference PDFs into source-traceable Markdown wiki pages. Use when building human- and LLM-searchable knowledge from PDFs, splitting by bookmarks or page ranges, preserving provenance, or validating extraction coverage and quality.
---

# Extract PDF Wiki

Convert PDFs into deterministic, reviewable Markdown. Preserve originals and treat Markdown as rebuildable output.

## Workflow

1. Inspect metadata, hashes, page count, bookmarks, text coverage, encryption, and parser warnings.
2. Choose boundaries in this order: bookmarks, detected headings, then fixed page chunks.
3. Extract every page once and cache text for the run.
4. Create one page per useful topic or screen, with stable ID, title, aliases, category, source pages, and tags.
5. Preserve subsection headings and page-level provenance. State that images and complex tables require the original PDF.
6. Derive explicit fields useful to humans and RAG: screen code, purpose, inputs, outputs, steps, cautions, related screens, and synonyms when supported by the source.
7. Validate page coverage, duplicate paths, empty sections, encoding, extreme sizes, and representative output against the PDF.

## Rules

- Use the repository `uv` environment; never global `pip` or system Python.
- Use `pypdf` for bookmark and text extraction. Use PDF rendering when layout fidelity matters.
- Do not OCR text-bearing PDFs by default. Measure extraction coverage first.
- Normalize conservatively and never invent domain facts.
- Keep human Markdown and machine-readable records linked by the same stable document ID.
- Never overwrite sources; keep the build reproducible.

For this repository, use `scripts/build_check_wiki.py` and read [quality.md](references/quality.md).
