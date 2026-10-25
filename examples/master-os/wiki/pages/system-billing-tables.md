---
type: concept
sources: [raw/2026-10-20-databricks-docs-notes.md]
updated: 2026-10-20
---
# System billing tables

`system.billing.usage` records what was used (DBUs per SKU, per resource). `system.billing.list_prices` records what each SKU costs over time. Join them on SKU, cloud, unit and the price's time window to get list cost. Discounts aren't included.

## Key columns

- **usage:** `usage_date`, `workspace_id`, `sku_name`, `usage_quantity`, `usage_unit`, and `usage_metadata` (`job_id`, `cluster_id`, `warehouse_id`, ...)
- **list_prices:** `sku_name`, `cloud`, `usage_unit`, `price_start_time`, `price_end_time`, and `pricing.effective_list.default`

## Join pattern

Match the usage end time to the price window: `usage_end_time >= price_start_time` and (`price_end_time IS NULL` or `usage_end_time < price_end_time`). The full query is in `.claude/skills/cost-review/sql/dbx_cost_by_resource.sql`.

## Limits

- **List price only:** apply your contract discount separately.
- **Access:** system schemas must be enabled, and readers need `USE` and `SELECT`. See [Unity Catalog privileges](unity-catalog-privileges.md).

## Related

- [Databricks cost levers](databricks-cost-levers.md)
