# Raw source: Databricks docs notes

- **Captured:** 2026-10-20
- **Sources (read and paraphrased):**
  - Unity Catalog privileges and securable objects (docs.databricks.com, Azure Databricks docs)
  - Billable usage system table reference (`system.billing.usage`)
  - Pricing system table reference (`system.billing.list_prices`)
  - Best practices for cost optimization

Immutable: don't edit this file. Pages in `pages/` distil it.

## Notes

- To query a table, a principal needs `USE CATALOG` on its catalog, `USE SCHEMA` on its schema, and `SELECT` on the table.
- Privileges granted on a catalog or schema are inherited by the objects inside it.
- `BROWSE` lets a principal see an object's metadata in Catalog Explorer without reading its data.
- Best practice: grant to groups, not to individual users.
- `system.billing.usage` holds one row per usage record, with `usage_date`, `sku_name`, `usage_quantity`, `usage_unit`, `workspace_id`, and a `usage_metadata` struct (`job_id`, `cluster_id`, `warehouse_id` and more).
- `system.billing.list_prices` holds list prices per SKU over time (`price_start_time`, `price_end_time`, and a `pricing` struct including `effective_list.default`).
- List prices don't include negotiated discounts.
- System schemas have to be enabled. Access is granted with `USE` and `SELECT` like any other schema.
- Cost guidance: use jobs compute for scheduled work, set auto-termination, right-size and auto-stop SQL warehouses, and use cluster policies to enforce limits.
