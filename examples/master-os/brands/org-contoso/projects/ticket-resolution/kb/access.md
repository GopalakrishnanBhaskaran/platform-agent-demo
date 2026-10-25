# Known fixes: access

## User can't see a catalog in Catalog Explorer

- **Symptom:** the catalog is missing for the user but visible to admins.
- **Cause:** the user has `SELECT` on tables but no `USE CATALOG` or `USE SCHEMA`.
- **Fix:** grant `USE CATALOG` and `USE SCHEMA` to the user's group, not to the user.
- **Check:** `SHOW GRANTS ON CATALOG <catalog>`
- **Verified:** 2026-10-02
