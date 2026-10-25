# AUT-004 Idle Azure resource scan (org-contoso)

A deterministic Azure Automation runbook. It finds idle and orphaned resources. It reports only and never deletes.

```mermaid
flowchart LR
  T([Azure Automation<br/>Sun 22:00]) --> G[Resource Graph queries<br/>unattached disks, stopped VMs<br/>empty App Service plans, old snapshots]
  T --> C[Cost Management API<br/>last 30 days cost per resource]
  G --> J[Join and rank<br/>by monthly cost]
  C --> J
  J --> F[(stfinops/idle-scan/<br/>YYYY-MM-DD.csv)]
  J --> M[Teams message<br/>top 10 + link to CSV]
```

## Details

- **Code:** `~/work/contoso/finops-jobs/runbooks/idle_scan.py`
- **Runs as:** managed identity `mi-idle-scan` (Reader and Cost Management Reader on both subscriptions)
