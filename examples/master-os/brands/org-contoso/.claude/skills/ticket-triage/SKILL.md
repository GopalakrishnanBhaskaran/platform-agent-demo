---
name: ticket-triage
description: Triage a Contoso platform ticket for Azure or Databricks. Classify it, find the likely cause with read-only checks, and draft an internal note and a user reply. Use for Jira PLAT tickets, a pasted ticket, or when the ticket triage automation (AUT-005) runs.
---

# Ticket triage (Contoso only)

This skill lives inside the org brand so the whole Contoso setup can be handed over intact.

## 1. Classify

Pick one category:

- **access:** Unity Catalog grants, workspace access, Azure RBAC
- **job-failure:** job or cluster errors, library conflicts, out-of-memory
- **cost-quota:** quota limits, cluster policy blocks, budget alerts
- **network:** private endpoints, firewall, VNet injection
- **request:** new workspace, catalog, cluster policy or service principal

## 2. Check known fixes

Read `brands/org-contoso/projects/ticket-resolution/kb/<category>.md`. If a known fix matches, use it.

## 3. Gather evidence (read-only)

- Job failure: `databricks jobs get-run <run_id>`, then the error in the run output
- Access: `SHOW GRANTS ON <object>`, `az role assignment list --assignee <id>`
- Audit trail: `system.access.audit` for the user and time window

## 4. Draft

- **Internal note:** category, cause, evidence (commands and results), fix steps
- **User reply:** follows `context/voice.md`, 3 steps at most

## 5. Learn

If the fix is new, propose a kb entry (symptom, cause, fix, verified on date).

**Never** change grants, restart or resize clusters, or edit jobs without asking.
