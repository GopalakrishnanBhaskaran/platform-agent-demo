# Contoso environments

Example values. Replace them with yours.

| Workspace | Region | Purpose | Owner | Unity Catalog metastore |
|---|---|---|---|---|
| dbx-prod-weu | West Europe | Production pipelines | Data Eng | uc-weu |
| dbx-dev-weu | West Europe | Development | Data Eng | uc-weu |
| dbx-analytics-weu | West Europe | BI and SQL warehouses | Analytics | uc-weu |

| Subscription | Purpose | Cost owner |
|---|---|---|
| sub-data-prod | Prod data platform | Platform team |
| sub-data-dev | Dev and sandboxes | Platform team |

## Service principals used by automations

| Name | Used by | Access |
|---|---|---|
| sp-finops-reader | AUT-003 weekly cost report | USE and SELECT on `system.billing`, `system.compute` |
| mi-idle-scan | AUT-004 idle resource scan | Reader and Cost Management Reader on both subscriptions |
| svc-jira-triage | AUT-005 ticket triage | Jira: browse and comment on project PLAT |
