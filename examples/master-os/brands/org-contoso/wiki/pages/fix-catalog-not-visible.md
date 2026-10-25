---
type: fix
category: access
sources: [moved from projects/ticket-resolution/kb/access.md]
updated: 2026-10-02
---
# Fix: user can't see a catalog in Catalog Explorer

The user has `SELECT` on tables but no `USE CATALOG` or `USE SCHEMA`. Grant both to the user's group, not to the user.

- **Symptom:** the catalog is missing for the user but visible to admins.
- **Check:** `SHOW GRANTS ON CATALOG <catalog>`
- **Fix:** `GRANT USE CATALOG ON CATALOG <catalog> TO <group>` and `GRANT USE SCHEMA ON SCHEMA <catalog>.<schema> TO <group>`
- **Verified:** 2026-10-02 on dbx-prod-weu

## Background

How grants inherit, and what `BROWSE` adds: [Unity Catalog privileges](../../../../wiki/pages/unity-catalog-privileges.md) (shared wiki).
