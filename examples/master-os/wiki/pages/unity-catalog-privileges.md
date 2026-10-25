---
type: concept
sources: [raw/2026-10-20-databricks-docs-notes.md]
updated: 2026-10-22
---
# Unity Catalog privileges

To read a table, a principal needs three grants: `USE CATALOG` on the catalog, `USE SCHEMA` on the schema, and `SELECT` on the table (or on a parent, since grants inherit downward). Most "I can't see or query it" tickets are a missing `USE` grant, not a missing `SELECT`.

## How grants work

- **Inheritance:** a grant on a catalog applies to every schema and table inside it, and a grant on a schema applies to its tables.
- **BROWSE:** shows an object's metadata in Catalog Explorer without giving data access. Useful for discovery.
- **Groups, not users:** grant to account groups, so access follows group membership and survives people moving teams.

## Check access

```sql
SHOW GRANTS ON CATALOG <catalog>;
SHOW GRANTS ON SCHEMA <catalog>.<schema>;
SHOW GRANTS `<group>` ON TABLE <catalog>.<schema>.<table>;
```

## Related

- [System billing tables](system-billing-tables.md): reading system tables needs the same `USE` and `SELECT` grants.
