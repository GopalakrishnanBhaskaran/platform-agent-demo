# Brand: org-contoso (employer)

Contoso platform team. We run Azure and Databricks for the data teams. My part: ticket resolution, cost savings, and automating manual platform work. Root rules in `../../CLAUDE.md` still apply.

## Where things live

| Need | Path |
|---|---|
| Ticket playbook and known fixes | `projects/ticket-resolution/` |
| Cost savings tracker | `projects/dbx-cost-savings/` |
| HMS to Unity Catalog migration | `projects/hms-to-uc-migration/` |
| Workspaces, subscriptions, owners | `context/environments.md` |
| Org-only skills | `.claude/skills/` (ticket-triage) |
| Local extracts (gitignored) | `data/` |

## Rules

- **Code lives in Contoso's repos:** `~/work/contoso/<repo>` (Azure DevOps). Projects here hold the README, decisions and pointers only.
- **Data stays at its source.** Query system tables, Jira and Cost Management in place. Pull only what the task needs into `data/`, and delete it afterwards.
- Investigate with read-only commands: `databricks jobs get-run`, `az role assignment list`, `SELECT` on system tables. Ask before any write.
- Internal emails: put the ticket ID in the subject and say what changed.
- Never move Contoso content into the personal brand, a client file or public content.
