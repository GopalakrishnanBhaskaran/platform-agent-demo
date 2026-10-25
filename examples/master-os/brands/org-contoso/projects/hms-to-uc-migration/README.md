# HMS to Unity Catalog migration

- **Goal:** move all Hive metastore tables in `dbx-prod-weu` to Unity Catalog by Q1 2027, with no broken jobs.
- **Status:** planning
- **Code lives in:** `~/work/contoso/uc-migration` (Azure DevOps): UCX config, migration notebooks, validation SQL.

## Plan

1. Run the UCX assessment and save the summary in `assessment.md` (counts only, no table names in this OS).
2. Map HMS databases to catalog and schema in `mapping.md`.
3. Migrate in waves of about 10 schemas. Validate row counts and job runs after each wave.
4. Repoint jobs, then set the HMS tables to read-only.

## Decisions

- 2026-10-12: external tables are upgraded in place with `SYNC`. Managed Delta tables on DBFS root are copied with `DEEP CLONE`.
