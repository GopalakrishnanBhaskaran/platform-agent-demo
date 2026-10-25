# Master OS

My one home for personal work, org work and client pointers. This file is the router: it says where things live and the rules that apply everywhere. Details live in the files it points to.

@context/me.md

## Routing

Read the brand's CLAUDE.md before doing work for that brand.

| If the task is about | Brand | Start here |
|---|---|---|
| My LinkedIn content, my open-source cost toolkit, my freelance pipeline | personal | `brands/personal/CLAUDE.md` |
| Contoso tickets, cost savings, UC migration, platform automation | org-contoso | `brands/org-contoso/CLAUDE.md` |
| A freelance client | client | `clients/<client>.md` |
| A live automation (scheduled or webhook) | (any) | `automations/registry.csv` |
| Why a file or folder lives where it does | (any) | `decisions/file-map.md` |

If you can't tell which brand a task belongs to, ask. Don't guess.

## Data rules

- Work in one brand per task. Don't read another brand's `data/` or `projects/` unless I ask.
- Never copy one brand's data into another brand, a shared skill, or a shared file.
- Leave org data at its source (system tables, Jira, SharePoint). Pull only what the task needs into `brands/org-contoso/data/`, which is gitignored, and delete it when the task is done.
- Client deliverables and call transcripts live outside this folder. Open the path in `clients/<client>.md` only when I ask for that client's files.
- This file guides you. It doesn't enforce anything. The hard blocks are in `.claude/settings.json`.

## Skills

- Shared skills (used by 2 or more brands) go in `.claude/skills/`: email-reply, email-coach, cost-review, checkup, grill-me.
- Brand-only skills go in `brands/<brand>/.claude/skills/` so the brand can be handed over intact. They load once you open a file in that brand.
- New skill: shared only if 2 or more brands need it. Otherwise put it in the brand.

## Automations

- Every live automation has a row in `automations/registry.csv` and a flowchart in `automations/flows/<id>-<name>.md`. No row means it doesn't run.
- When you add or change an automation, update the row and the flowchart in the same change.
- Each automation runs with its own credential and tool list (columns `credential` and `allowed_tools`), never with mine. Brand automations start in the brand folder, so other brands are outside their reach.
- Paths in skills, the registry and flowcharts are from the master OS root.

## How to work

- Plan first on anything non-trivial. State the definition of done and how you'll prove it.
- Investigate Azure and Databricks with read-only commands. Ask before any write, delete, push, deploy or send.
- Emails: follow `context/voice.md`. Draft only. I send.
- New file or folder: add a line to `decisions/file-map.md` saying why it lives there.

## Maintenance

- Feeling lost: run `/checkup`.
- Map of everything: `python3 tools/os_map.py` writes `os-map.html`.

## Applied learning

-
