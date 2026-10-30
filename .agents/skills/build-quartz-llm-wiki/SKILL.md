---
name: build-quartz-llm-wiki
description: Build and validate high-performance Quartz knowledge bases for human browsing, LLM retrieval, and programmatic AI call-center use. Use when integrating generated manuals, preserving repository conventions, designing cross-links and stable IDs, exporting JSONL, testing search quality, or producing a reproducible offline static site without publishing.
---

# Build Quartz LLM Wiki

Create one knowledge base with linked human and machine views instead of separate, drifting copies.

## Workflow

1. Read repository instructions, handovers, sync scripts, ignore rules, and Quartz configuration.
2. Identify authoritative sources, generated `content/`, and publish artifacts. Never hand-edit generated content when a pipeline exists.
3. Define a stable schema: ID, title, aliases, intent, market, screen code, inputs, outputs, steps, cautions, related IDs, and source provenance.
4. Generate small Markdown pages, navigation hubs, backlinks, and relation links for people.
5. Export the same normalized records to JSONL for RAG, APIs, and call-center ingestion.
6. Add intent and synonym indexes so screen numbers, business terms, and natural-language questions converge on the same page.
7. Build locally with locked Python and Node environments.
8. Validate structural integrity, search quality, source traceability, broken links, external requests, page sizes, and representative Korean rendering.
9. Report without pushing or publishing unless explicitly requested.

## Quality gates

- Human: a user can reach common tasks by screen number, market, feature, or problem in at most a few navigation steps.
- Retrieval: each chunk has stable ID, focused scope, aliases, and direct provenance.
- Programmatic: JSONL schema is documented, versioned, deterministic, and referentially valid.
- Answer safety: procedures distinguish required inputs, results, cautions, and unsupported claims.
- Performance: no oversized pages or search-index hotspots; large code tables are chunked.
- Reproducibility: source hashes, dependency locks, commands, and validation reports are recorded.

## Rules

- Preserve unrelated changes and existing offline assets, locale, and deployment tooling.
- Keep sources and generated content out of Git when repository rules define them as generated data.
- Keep scripts, locks, skills, schemas, and validators in Git.
- Use `uv` for Python and the pinned Node version for Quartz.
- Never publish, push, or change remotes without explicit authorization.

Read [repository-rules.md](references/repository-rules.md) before building this project.
