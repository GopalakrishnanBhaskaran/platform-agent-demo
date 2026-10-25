# AUT-003 Weekly Databricks cost report (org-contoso)

A deterministic Databricks Job. Claude helped build it with the `cost-review` skill, but no LLM runs at run time.

```mermaid
flowchart LR
  T([Databricks Job<br/>Mon 07:00]) --> Q[SQL task<br/>last 7 days list cost<br/>by workspace, SKU, resource]
  S1[(system.billing.usage)] --> Q
  S2[(system.billing.list_prices)] --> Q
  Q --> D[(ops.finops.weekly_cost)]
  D --> K[SQL task<br/>top 10 movers<br/>vs prior week]
  K --> E[Job notification<br/>platform-team list]
```

## Details

- **Code:** `~/work/contoso/finops-jobs` (Azure DevOps), deployed with Databricks Asset Bundles
- **Query:** based on `.claude/skills/cost-review/sql/dbx_cost_by_resource.sql`
- **Runs as:** `sp-finops-reader` (USE and SELECT on `system.billing`; write only on `ops.finops`)
