# File map: why everything lives where it does

Built by running the `grill-me` skill with "grill me about every file in here". `tools/os_map.py` reads the table below to annotate the drill-down map, and `/checkup` flags any folder that has no row.

Every folder needs a row. Files are covered by their folder's row unless they need their own reason.

| Path | Why it lives here |
|---|---|
| `CLAUDE.md` | Root router: routing table and rules for every brand. Loaded in every session, so keep it short. |
| `.gitignore` | Keeps secrets, brand `data/` and stray client folders out of my personal GitHub. |
| `.claude/` | Claude Code config for the whole OS. |
| `.claude/settings.json` | Hard deny and ask rules. CLAUDE.md only guides; this file enforces. |
| `.claude/skills/` | Shared skills: anything 2 or more brands use. |
| `.claude/skills/email-reply/` | Shared: every brand gets email. Picks the brand from the sender, then loads only that brand. |
| `.claude/skills/email-coach/` | Shared: pairs with email-reply. Compares drafts with what I sent. |
| `.claude/skills/cost-review/` | Shared: I do cost reviews for Contoso and for clients. |
| `.claude/skills/cost-review/sql/` | Generic system-table queries with no brand data, so they're safe to share. |
| `.claude/skills/checkup/` | Shared: health check of the OS itself. |
| `.claude/skills/grill-me/` | Shared: interviews me and writes the answers to `brainstorms/`. |
| `context/` | Who I am and how I write. Used by every brand. |
| `context/priorities.md` | 90-day priorities with an "As of" date. Situational, so CLAUDE.md points to it rather than importing it. |
| `connections/` | Everything Claude or an automation can reach: connectors, CLI profiles, service identities. |
| `connections/registry.csv` | One row per connection: account, brand, write actions, guard, where the secret lives, which automations use it. |
| `brands/` | One folder per brand. Each brand is self-contained so it can be handed over intact. |
| `brands/personal/` | My own brand: content, open-source toolkit, freelance pipeline. |
| `brands/personal/.claude/` | Personal-only Claude config. |
| `brands/personal/.claude/skills/` | Personal-only skills. They load once Claude opens a file in this brand. |
| `brands/personal/.claude/skills/linkedin-post/` | Only the personal brand posts publicly. |
| `brands/personal/projects/` | One folder per personal project: README, decisions, next actions. |
| `brands/personal/projects/linkedin-content/` | Drafts and post log. Markdown only, so it lives here. |
| `brands/personal/projects/azure-cost-toolkit/` | Notes only. The code is public and lives in its own repo. |
| `brands/personal/projects/freelance-pipeline/` | Leads and proposals. A won lead becomes a `clients/` pointer. |
| `brands/personal/data/` | Local extracts for personal only. Gitignored. |
| `brands/org-contoso/` | Employer brand. Routing and notes only; code stays in Contoso's Azure DevOps. |
| `brands/org-contoso/.claude/` | Contoso-only Claude config. |
| `brands/org-contoso/.claude/skills/` | Contoso-only skills, kept here so the Contoso setup can be handed over intact. |
| `brands/org-contoso/.claude/skills/ticket-triage/` | Uses Contoso's ticket categories and kb, so it doesn't belong at the root. |
| `brands/org-contoso/context/` | Contoso workspaces, subscriptions and service principals. |
| `brands/org-contoso/projects/` | One folder per Contoso project. |
| `brands/org-contoso/projects/ticket-resolution/` | Ticket playbook. Tickets themselves stay in Jira. |
| `brands/org-contoso/projects/ticket-resolution/kb/` | Known fixes per category. ticket-triage reads these. |
| `brands/org-contoso/projects/dbx-cost-savings/` | Savings tracker. The job code lives in the finops-jobs repo. |
| `brands/org-contoso/projects/hms-to-uc-migration/` | Migration plan and decisions. UCX code lives in the uc-migration repo. |
| `brands/org-contoso/data/` | Local extracts and email logs for Contoso only. Gitignored. |
| `clients/` | One pointer file per client. Client work lives outside the OS. |
| `automations/` | Everything that runs without me. |
| `automations/registry.csv` | The one log sheet of live automations: trigger, skills, reads, writes, credential. |
| `automations/flows/` | One flowchart per automation, linked from the registry. |
| `brainstorms/` | Raw grill-me captures. Polished results move to a project. |
| `decisions/` | This map and other "why" records. |
| `decisions/log.md` | Append-only log of decisions that change how the OS works. |
| `tools/` | Scripts for the OS itself: the map and the checkup checks. |

## Moves log

| Date | Moved | From, to | Why |
|---|---|---|---|
| 2026-10-18 | cost SQL | `brands/org-contoso/projects/dbx-cost-savings/sql/` to `.claude/skills/cost-review/sql/` | Used for clients too. Generic, with no Contoso data. |
| 2026-10-18 | ticket-triage | `.claude/skills/` to `brands/org-contoso/.claude/skills/` | Only Contoso uses it, and it should travel with the brand. |
