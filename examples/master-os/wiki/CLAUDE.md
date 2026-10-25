# Wiki schema (shared tech wiki)

Generic Azure and Databricks knowledge that every brand can use. This file loads when you work in `wiki/`. Brand wikis follow this schema plus their own rules.

## Layout

- `raw/`: immutable sources, such as doc notes, release notes and course notes. Read them only to ingest. Never edit them.
- `pages/`: pages you write and maintain, one topic per page.
- `index.md`: every page, with a one-line summary. Read it first for any question.
- `log.md`: an append-only record of every ingest, filed-back answer and lint.

## Page format

```markdown
---
type: concept | howto | fix | decision | incident
sources: [raw/<file>]
updated: YYYY-MM-DD
---
# Title

The answer first, in one paragraph. Then the detail. Link related pages with relative links, for example [UC privileges](unity-catalog-privileges.md).
```

## Operations

- **Ingest:** read one raw source. Update every page it affects, and create a page only when a topic has no home. Update `index.md`, then append a row to `log.md` naming the source file and the pages touched.
- **Query:** read `index.md`, then only the pages you need, and cite them in the answer. If the answer took real work and will be asked again, file it back as a page and log it as `file-back`.
- **Lint:** run `python3 tools/os_map.py --check` for index, link and ingest gaps. Then look for:
  - Contradictions between pages
  - Claims superseded by newer sources
  - Topics mentioned on 3 or more pages with no page of their own

## Rules

- Nothing specific to an organisation or a person: no org, client or person names, no internal URLs, and no figures from a real environment. Use generic examples.
- When sources disagree, keep both claims with their dates and sources, and flag the conflict at the top of the page.
- Prefer the newest official documentation, and put the date you read it in `sources`.
