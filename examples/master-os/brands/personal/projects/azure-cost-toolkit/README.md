# Azure cost toolkit (open source)

- **Goal:** public scripts for idle-resource scans and Databricks cost queries that anyone can run.
- **Status:** active
- **Code lives in:** `~/code/azure-cost-toolkit` (github.com/<me>/azure-cost-toolkit, public). Not in this OS.
- **Why it's outside:** it's public, has its own CI and releases, and must never pick up OS context by accident.

## Decisions

- 2026-09-02: Python and `az` CLI only, no SDK, so users can read every call.
- 2026-09-10: queries come from the shared `cost-review` skill, generalised before publishing.

## Next actions

1. Add an unattached-disk report.
2. Write a README with sample output.
