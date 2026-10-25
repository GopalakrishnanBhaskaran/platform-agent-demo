-- Databricks list cost by workspace, SKU and resource for the last N days.
-- Needs USE and SELECT on system.billing. List price only: apply your discount separately.
-- Change :days, or replace the parameter with a literal, before running.

SELECT
  u.workspace_id,
  u.sku_name,
  COALESCE(u.usage_metadata.job_id,
           u.usage_metadata.warehouse_id,
           u.usage_metadata.cluster_id,
           'other')                                        AS resource_id,
  CASE
    WHEN u.usage_metadata.job_id       IS NOT NULL THEN 'job'
    WHEN u.usage_metadata.warehouse_id IS NOT NULL THEN 'sql_warehouse'
    WHEN u.usage_metadata.cluster_id   IS NOT NULL THEN 'cluster'
    ELSE 'other'
  END                                                      AS resource_type,
  ROUND(SUM(u.usage_quantity), 2)                          AS dbus,
  ROUND(SUM(u.usage_quantity * p.pricing.effective_list.default), 2) AS list_cost_usd
FROM system.billing.usage AS u
JOIN system.billing.list_prices AS p
  ON  u.sku_name   = p.sku_name
  AND u.cloud      = p.cloud
  AND u.usage_unit = p.usage_unit
  AND u.usage_end_time >= p.price_start_time
  AND (p.price_end_time IS NULL OR u.usage_end_time < p.price_end_time)
WHERE u.usage_date >= date_sub(current_date(), :days)
GROUP BY ALL
ORDER BY list_cost_usd DESC
LIMIT 50;
