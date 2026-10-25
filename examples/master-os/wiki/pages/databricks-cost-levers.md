---
type: howto
sources: [raw/2026-10-20-databricks-docs-notes.md]
updated: 2026-10-20
---
# Databricks cost levers

Check these in order. The first three usually hold most of the savings, and none of them changes results.

| # | Lever | How to spot it | Typical fix |
|---|---|---|---|
| 1 | Scheduled jobs on all-purpose compute | Job runs with a `cluster_id` from an interactive cluster | Move them to job compute (a lower DBU rate) |
| 2 | Clusters that never stop | Auto-termination off, or over 60 minutes | Set 15 to 30 minutes, and enforce it with a cluster policy |
| 3 | Oversized or always-on SQL warehouses | Low query load against warehouse size; auto-stop off | Smaller size, auto-stop, or serverless |
| 4 | Photon where it doesn't pay | Photon on, with run time not much shorter | Turn it off for that workload. Photon costs more DBUs per hour, so it has to finish faster to save money. |
| 5 | No policies | Users pick any node type and size | Cluster policies with node-type and auto-termination limits |

## Size each saving

Use the billing tables to price the current spend for the resource, then estimate the change. See [System billing tables](system-billing-tables.md) for the query.

## Related

- [Unity Catalog privileges](unity-catalog-privileges.md): you need access to `system.billing` before you can measure anything.
