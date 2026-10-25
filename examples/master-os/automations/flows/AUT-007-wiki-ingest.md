# AUT-007 Wiki ingest and lint (org-contoso)

Every Friday it ingests the week's new raw sources (postmortems, meeting notes, ticket exports) into the Contoso wiki, then lints it.

```mermaid
flowchart LR
  T([Schedule<br/>Fri 16:00]) --> R[(data/raw/<br/>gitignored)]
  R --> N{File already<br/>in log.md?}
  N -- yes --> S[Skip]
  N -- no --> I[wiki skill: ingest<br/>update pages first]
  I --> P[(wiki/pages/)]
  I --> X[(index.md + log.md)]
  I --> G{Generic fact?}
  G -- yes --> Q[Propose generalised page<br/>for shared wiki]
  P --> L[wiki skill: lint<br/>os_map.py --check]
  L --> O[(Lint row in log.md)]
```

## Run command

```bash
cd ~/master-os/brands/org-contoso && claude -p "/wiki ingest brands/org-contoso/wiki" \
  --add-dir ../../wiki \
  --permission-mode dontAsk --permission-prompts none \
  --allowedTools "Edit(./wiki/**)"
```

- It reads the shared schema through `--add-dir`, but can only edit the Contoso wiki. Promoting a fact to the shared wiki stays a proposal that I apply.
- Raw sources are gitignored, so this runs on the laptop, not as a cloud task.
