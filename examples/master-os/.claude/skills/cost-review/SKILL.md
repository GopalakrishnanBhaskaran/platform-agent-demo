---
name: cost-review
description: Review Azure and Databricks spend for one brand or client and list savings with estimated monthly value. Use when I ask for a cost review, savings ideas, why spend went up, or idle resources.
---

# Cost review

Run this for one brand or client at a time. Use that brand's workspaces and subscriptions from its `context/` files.

## Steps

1. **Scope:** confirm the workspaces, subscriptions and date range. Default to the last 30 days against the 30 days before.
2. **Databricks spend:** run `sql/dbx_cost_by_resource.sql` (in this skill's folder) on a SQL warehouse in the brand's workspace. Set `:days` to the date range.
3. **Azure spend:** `az costmanagement query` or Cost Management exports, grouped by resource group and service.
4. **Find savings.** Check these first:
   - All-purpose clusters running scheduled jobs (move them to job clusters)
   - No auto-termination, or auto-termination over 60 minutes
   - SQL warehouses that never scale down, or are oversized for their query load
   - Photon on workloads that don't benefit from it
   - Idle VMs, unattached disks, old snapshots, empty App Service plans
   - Storage that belongs in the cool or archive tier
5. **Size each saving:** estimated monthly saving, effort (S, M or L), risk, and owner.

## Output

A table: Opportunity | Evidence | Est. monthly saving | Effort | Risk | Next step. Add the confirmed rows to the brand's savings tracker.

Read-only. Never resize, stop or delete anything. Propose the change and let me run it.
