# Databricks and Azure cost savings (FY26)

- **Goal:** cut platform spend by 15% against the FY25 run rate.
- **Status:** active
- **Code lives in:** `~/work/contoso/finops-jobs` (Azure DevOps). The weekly report job (AUT-003) is deployed from there.
- **How findings are made:** the shared `cost-review` skill, run for Contoso only.

## Savings tracker

| # | Opportunity | Est. monthly saving | Status | Owner | Verified |
|---|---|---|---|---|---|
| 1 | Move 14 scheduled jobs from all-purpose to job clusters | $4,200 | done | me | 2026-09-30 |
| 2 | Auto-termination to 30 min on dev clusters | $1,100 | done | me | 2026-10-07 |
| 3 | Downsize analytics SQL warehouse from Large to Medium | $2,600 | in review | Analytics | |
| 4 | Delete 2.1 TB of unattached managed disks | $310 | approved | me | |

Count a saving only after it shows in a week of billing data. Put the query result in the Verified column.

## Next actions

1. Get sign-off on #3 from the Analytics lead.
2. Add serverless SQL to the weekly report.
