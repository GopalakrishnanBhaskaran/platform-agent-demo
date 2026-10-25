---
name: wiki
description: Maintain an LLM wiki. Ingest a raw source into the shared wiki or a brand wiki, file a good answer back as a page, or lint a wiki. Use when I say "ingest this", "add this to the wiki", "file that answer", "lint the wiki", or when the wiki ingest automation (AUT-007) runs.
argument-hint: "ingest|file-back|lint <wiki folder> [source]"
---

# Wiki

## 1. Pick the wiki

- Generic Azure or Databricks knowledge, with no organisation facts: `wiki/`
- Anything about one brand's environment, incidents or decisions: `brands/<brand>/wiki/`
- Client knowledge never goes in a wiki here. It stays with the client's files.

Then follow that wiki's `CLAUDE.md`. Its schema sets the page format and the operations.

## 2. Ingest

1. Read the source once and list the facts worth keeping.
2. Update existing pages first. Create a page only for a topic with no home.
3. Update `index.md`. Then append a row to `log.md` with the date, `ingest`, the exact raw file name, and the pages touched.
4. In a brand ingest, if a fact is generic, also write it, generalised, to the shared wiki. Never copy brand facts the other way.

## 3. File back

When an answer took real work and will be asked again, save it as a page, add it to the index, and log it as `file-back`.

## 4. Lint

1. Run `python3 tools/os_map.py --check`. It covers index gaps, broken links, raw sources not yet ingested, a stale `hot.md`, and private names in the shared wiki.
2. Then make the judgment checks in the schema: contradictions, superseded claims, and missing pages.
3. Report the findings. Fix only what I approve, and log the lint.
