# How an AIOS should be structured: lessons from the Q&A

An analysis of the Q&A follow-ups (Nate, Danan and Kierra on a 13-brand, 50-project, 31-skill, 20-automation setup). It's read against the AIOS frameworks already in this repo:

- The 4 Cs (`docs/claude-usage-reference.md`, section 15)
- The context failure modes in the `os-audit` skill
- The executive-assistant layout

The worked example is [`examples/master-os/`](../examples/master-os/README.md).

## Short answer

The 4 Cs say what an AIOS needs:

- **Context:** who you are and how you work
- **Connections:** what it can reach
- **Capabilities:** skills
- **Cadence:** what runs on a schedule

Every Q&A question was about what breaks once that grows: you lose track of what's where, what can touch what, what's running, and why things are where they are. Nate's point was that "the setup is fine; the pain is visibility." So the structure needs two more layers, Boundaries and Visibility. Context also splits in two: standing context, and knowledge held in an LLM wiki. A router sits across all of them:

| Layer | Question it answers | Driven by (Q&A) | Lives in (example) | Loaded |
|---|---|---|---|---|
| **Router** | Where do I go for this task? | One folder; routing and rules keep brands separate | Root and brand `CLAUDE.md` | Root always; brand on entry |
| **Context** | Who am I, how do I write, what matters now? | Claude knows the business | `context/`, `brands/*/context/` | Stable facts imported; priorities on demand |
| **Knowledge** (LLM wiki) | What do we know, and where did it come from? | "Claude knows the business but only opens deliverables when asked" | `wiki/`, `brands/*/wiki/` | Index first, then pages on demand |
| **Connections** | What can Claude and each automation reach? | Claude can read anything local *or connected* | `connections/registry.csv` | On demand |
| **Capabilities** | What can it do, and for which brand? | Skills at the top vs nested by brand | `.claude/skills/`, `brands/*/.claude/skills/` | Descriptions always; body on use |
| **Cadence** | What runs without me, with what access? | One log sheet; a flowchart per agent | `automations/registry.csv`, `automations/flows/` | On demand |
| **Boundaries** *(new)* | What's in vs out, and what's enforced? | Separate Claude from automations; clients outside; pointers | `.claude/settings.json`, `.gitignore`, `clients/*.md` | Enforced, not read |
| **Visibility** *(new)* | Can I see it all, and why is each thing here? | Drill-down map; annotated file map; Doctor | `decisions/`, `tools/os_map.py`, `/checkup` | On demand |

## What each Q&A answer means for the structure

| Q&A point | Structural requirement | How to test it |
|---|---|---|
| The second brain has to make sense to *you* | Shape folders around how you look for things. For an Azure and Databricks provider that's who it's for (brand), then the workstream (tickets, cost, migration), then the artifact. Use the same shape in every brand. | Pick 3 recent artifacts and click down to each without search. |
| Claude can read anything local or connected unless denied | Access is its own layer. List every connection, then guard it in config. A connector isn't scoped by folder, so routing alone doesn't silo it. | Ask Claude to read `.env` or send an email. Both are refused or prompted. |
| Separate what Claude Code can touch from what each automation can touch | Two access planes: interactive (you, broad, deny rules) and automation (narrow; own identity, tool list and working folder). | Every automation row names a credential that has a row in the connections registry. |
| One folder; routing and rules keep brands apart | One root router, one router per brand, data partitioned per brand and gitignored. Separation is by rule plus enforcement, not by separate repos. | A fresh session asked a brand question opens only that brand's files. |
| One log sheet of live automations | A single source of truth for Cadence: trigger, runs on, skills, reads, writes, credential, flowchart, last reviewed. "No row means it doesn't run." | The registry matches what is actually scheduled. |
| Skills at the top (Nate) vs nested by brand (Danan) | Place by **reuse** and **portability**. Shared if 2 or more brands use it; nested if one brand uses it or it must hand over intact. | No shared skill is used by only one brand. |
| The pain is visibility; build a drill-down | Generate the view **from** the source files (file map, registries, flowcharts), so it can't drift. Never maintain a separate diagram. | The map rebuilds with one command and matches the disk. |
| Annotated map of why each file exists (Kierra) | A "why" layer: one reason per folder, plus a moves log. Grill Me fills it in. | The checkup lists folders with no reason. |
| Doctor or `/checkup` when overwhelmed | A maintenance layer: mechanical checks (script) plus judgment checks (skill), run weekly. | The checkup is green except known exceptions. |
| Client projects live outside the OS | The OS holds context and routing, not work products. It syncs to your GitHub; client work has its own owner, repo and confidentiality. | `clients/` holds only `.md` files. |
| Where the pointers go | One pointer file per external thing: facts plus paths. Claude knows the business but opens deliverables only when asked. The same pattern works for org repos and data sources. | Client facts live in exactly one file. |
| An n8n-style flowchart per agent (Danan) | Each automation gets a visual flow linked from its registry row, readable by people as well as Claude. | Every registry row has a flowchart, and every flowchart has a row. |

## Where the LLM wiki fits

The LLM wiki (Karpathy's pattern) is level 2 of the five second-brain levels. It splits Context in two:

- **Standing context:** who you are and how you work. Small, stable, always loaded.
- **Knowledge:** what you know. It grows with every ticket, incident and doc you read, so it can't be preloaded. It has to be indexed and read on demand.

### Its three layers and three operations

| Part | What it is | Who writes it |
|---|---|---|
| `raw/` | Immutable sources: doc notes, postmortems, meeting notes, ticket exports | You (or an export) |
| `pages/` | One topic per page, cross-linked, each with its sources and an updated date | Claude only |
| `CLAUDE.md` | The schema: page format, and how to ingest, query and lint | You |
| `index.md` | A one-line catalog of every page. Claude reads it first. | Claude |
| `log.md` | Append-only record of each ingest, file-back and lint | Claude |

- **Ingest:** one source updates every page it touches, then the index and the log.
- **Query:** read the index, then only the pages you need, citing them. A good answer gets filed back as a page.
- **Lint:** find contradictions, superseded claims, orphans and missing pages.

### The multi-brand question: one wiki or one per brand?

It's the same question Nate and Danan answered for skills, and the same rule applies: **place by reuse and portability.**

| Tier | Holds | Raw sources | Why |
|---|---|---|---|
| Shared `wiki/` | Generic Azure and Databricks knowledge: UC privileges, cost levers, system tables | `wiki/raw/` (public, committed) | Reused by org tickets, client cost reviews and LinkedIn posts |
| `brands/<brand>/wiki/` | That brand's fixes, incidents and decisions, plus `hot.md` | `brands/<brand>/data/raw/` (gitignored) | Brand facts stay siloed and travel with the brand on handover |
| Clients | None in the OS | (n/a) | Client knowledge stays with the client's files. The pointer file is enough. |

**Knowledge flows one way.** A brand fix that turns out to be generic gets generalised and promoted to the shared wiki. Brand facts are never copied down into it. This is also the safe pipeline for LinkedIn content: posts are built from shared-wiki pages, which by rule hold no org or client names.

### How the wiki maps onto the other layers

- **Router:** the root `CLAUDE.md` routes generic questions to `wiki/index.md`; the brand `CLAUDE.md` routes to its own wiki and `hot.md`.
- **Capabilities:** one shared `wiki` skill runs ingest, file-back and lint for every wiki. Brand skills read their wiki (ticket-triage reads `fix` pages and files new fixes back).
- **Cadence:** scheduled ingest is an automation like any other, with a registry row and a flowchart (AUT-007).
- **Boundaries:** brand raw sources sit in gitignored `data/raw/`. Only distilled pages, with no personal data, are committed.
- **Visibility:** the wiki's lint is part of `/checkup`. The script checks index completeness, broken links, raw files not yet in the log (pulled but not ingested), a stale `hot.md`, and org or client names in the shared wiki.

### Where wikis go wrong, and the guard for each

| Failure | How it shows up | Guard |
|---|---|---|
| Poisoning | A page states an old limit or price as current | `sources` and `updated` on every page; lint for superseded claims; prefer the newest official docs |
| Bloat | The wiki or `hot.md` gets loaded wholesale | Read the index first; `hot.md` under 30 lines; never answer from `raw/` |
| Confusion | Raw files pile up but never reach the pages | The checkup flags any raw file that isn't named in `log.md` |
| Clash | Two pages, or the shared and brand wiki, say different things | One topic per page; conflicts flagged at the top of the page; one-way promotion |

### When to go past level 2

Stay at the wiki until grep and the index stop finding answers, which is usually hundreds of pages. Semantic search (level 3) comes next. Even then, keep the wiki as the source the search indexes.

## Six design rules

1. **Keep the router small, and load facts on demand.** Always-loaded files (CLAUDE.md, `me.md`) hold stable rules and pointers only. Live numbers (costs, ticket counts, savings status) live at the source or in a project tracker. This is the os-audit's "expertise vs situational" split.
2. **One source of truth per fact, with pointers everywhere else.** Write precedence down: the registry wins for automations, the client file for client facts, system tables for cost. When two files disagree, Claude asks.
3. **Enforce boundaries in config and explain them in CLAUDE.md.** CLAUDE.md is guidance. Deny and ask rules, the working directory, per-automation identities and `.gitignore` are what actually hold.
4. **Place things by reuse and portability.** This one rule decides shared vs brand skills, inside vs outside the OS, and the OS repo vs a separate repo.
5. **Generate the view from the files.** The map, the counts and the checkup all read the same registries and file map, so the picture can't contradict the disk.
6. **Everything has a record.** Every folder has a reason, every automation a row, every connection an owner and a guard, and every OS decision a log entry.

## How the structure prevents the 4 context failures

| Failure (os-audit) | How it shows up in a multi-brand OS | Structural guard |
|---|---|---|
| **Poisoning** (false facts) | A stale cost figure or client status in an always-loaded file | Pointers instead of copies; "As of" dates; `last_reviewed`; the checkup flags anything over 90 days |
| **Bloat** (too much loaded) | A root CLAUDE.md that grows with every brand | Brand routers load on entry; nested skills load on demand; data stays at source |
| **Confusion** (missing or off-topic) | Unmapped folders; Claude reading the wrong brand | A routing table for every brand; a file-map reason for every folder; one brand per task |
| **Clash** (contradictions) | The same fact in two brands or two files, at two ages | One source of truth per fact; written precedence; one registry per layer |

## Applied to your setup (personal, org, clients)

- **Connectors map to brands.** Gmail and Upwork are personal; Microsoft 365 is the org. Claude Code doesn't scope them by folder, so:
  - Interactive sessions: `ask` rules on send, forward and delete tools (`mcp__*send*` and similar)
  - Automations: only the tools on their allowed list
- **The org layer depends on policy.**
  - If your employer allows org notes in your private GitHub, keep `brands/org-contoso/` in the OS.
  - If not, make it a submodule that points to the org's repo.
  - If the org has its own Claude Team or Enterprise account, org work may belong there instead. Check this before connecting org systems to a personal account.
- **Keep deterministic work deterministic.** Cost reports and idle-resource scans run as Databricks Jobs or Azure Automation (AUT-003, AUT-004). The AIOS documents and builds them; no agent runs them.
- **Second-brain level:** level 1 (CLAUDE.md plus folders) plus a level-2 LLM wiki in two tiers (see "Where the LLM wiki fits"). The ticket `kb/` became the Contoso brand wiki.
- **Where automations run:** laptop cron stops when the laptop sleeps. Move anything production-critical to Azure (a Container Apps job) or to Claude Code cloud scheduled tasks, and record the move in the registry.

## Gaps this analysis found in the first example, and what changed

| Gap | Why it matters | Change in `examples/master-os/` |
|---|---|---|
| No Connections layer | You can't guard what isn't listed, and connectors cross brand folders | Added `connections/registry.csv`. The checkup now flags automations whose credential has no row, and connections used across brands. |
| No current priorities | Context without priorities answers like a stranger | Added `context/priorities.md` with an "As of" date. The checkup warns after 90 days. |
| No precedence rule | Duplicated facts become clashes | Added a "Sources of truth" section to the root `CLAUDE.md`. |
| No OS decision log | The reasons behind structural choices get lost | Added `decisions/log.md`. |
| No guard on connector sends | Folder routing doesn't scope connectors | Added `ask` rules for `mcp__*send*`, `*forward*`, `*delete*` and `*trash*`. |
| No archive rule | Finished projects confuse routing | Added an archive rule to the root `CLAUDE.md`. |
| No knowledge layer | Known fixes sat in one project folder, with no index, log or lint, and generic knowledge had no shared home | Two-tier LLM wiki, a shared `wiki` skill, AUT-007 weekly ingest, and wiki lint in the checkup. The ticket `kb/` moved into the Contoso wiki. |

## Open decisions for you

1. Does your employer allow org notes in a personal GitHub repo? This decides whether org content lives in the OS or in a submodule.
2. Should org connectors live in a personal Claude account, or in the org's Claude account?
3. Which automations are production-critical enough to move off the laptop?
