# Master OS example: personal, org and client work in one folder

A working template of the "one master OS folder" setup for an Azure and Databricks solution provider. Copy it, rename Contoso (the employer) and Fabrikam (a client), and fill in `context/`.

```
master-os/
├── CLAUDE.md                  Root router: routing table, data rules, skill and automation rules
├── .claude/
│   ├── settings.json          Hard deny and ask rules (enforced)
│   └── skills/                Shared skills: email-reply, email-coach, cost-review, checkup, grill-me
├── context/                   me.md, voice.md, priorities.md (used by every brand)
├── connections/registry.csv   Every connector, CLI profile and identity: brand, write actions, guard, secret location
├── brands/
│   ├── personal/              CLAUDE.md, projects/, data/ (gitignored), .claude/skills/linkedin-post
│   └── org-contoso/           CLAUDE.md, context/, projects/, data/ (gitignored), .claude/skills/ticket-triage
├── clients/                   One pointer .md per client. The work itself lives outside.
├── automations/
│   ├── registry.csv           The one log sheet of live automations
│   └── flows/                 One n8n-style Mermaid flowchart per automation
├── brainstorms/               grill-me captures
├── decisions/                 file-map.md (why every folder lives where it does), log.md (OS decisions)
└── tools/os_map.py            Drill-down HTML map plus mechanical checkup
```

For why the AIOS is structured in these layers, see [docs/aios-structure.md](../../docs/aios-structure.md).

## Where each point from the call lives

| Point | In this example |
|---|---|
| The second brain must make sense to you | Every brand has the same shape: `brands/<brand>/projects/<project>/README.md`. The reasons are in `decisions/file-map.md`. |
| Claude can read anything unless you deny it | Hard blocks go in `.claude/settings.json`, not in CLAUDE.md, which only guides Claude ([permissions docs](https://code.claude.com/docs/en/permissions)). |
| Separate what Claude Code can touch from what each automation can touch | `settings.json` governs your sessions. Each automation has its own `credential` and `allowed_tools` in the registry, and starts in its brand folder. Every credential has a row in `connections/registry.csv`. |
| One folder, with routing and rules keeping brands apart | Root `CLAUDE.md` has the routing table and data rules. Each brand's `CLAUDE.md` holds that brand's rules. `data/` is gitignored per brand. |
| One log sheet of live automations | `automations/registry.csv`: trigger, runs on, skills, reads, writes, credential, flowchart, last reviewed. |
| Skills at the top vs nested by brand | Both. Shared skills sit in `.claude/skills/`. Brand-only skills sit in `brands/<brand>/.claude/skills/`, so the brand can be handed over intact. |
| The pain is visibility | `python3 tools/os_map.py` writes `os-map.html`: a searchable folder tree with the reason beside each folder, plus the registry and flowcharts. |
| Annotated map of every file | Run grill-me with the prompt in `brainstorms/README.md`. It fills in `decisions/file-map.md`. |
| Doctor / `/checkup` | `/checkup` runs `tools/os_map.py --check` and then makes the judgment calls (misplaced skills, routing that no longer fits). |
| Client projects outside the OS | `clients/*/` is gitignored, and the checkup flags any client folder. |
| Where the pointers go | `clients/fabrikam.md`: start date, first project price, main contact, deliverables and transcript paths. |
| An n8n-style flowchart per agent | `automations/flows/AUT-00X-*.md`. Mermaid renders on GitHub and in `os-map.html`. |

## Personal vs org vs client: where each thing lives

| | Personal | Org (employer) | Client |
|---|---|---|---|
| Routing and notes | `brands/personal/` | `brands/org-contoso/` | `clients/<client>.md` |
| Code | In the OS if small; its own repo if you publish it | The org's Azure DevOps or GitHub, cloned to `~/work/<org>/` | The client's repo |
| Data | `brands/personal/data/` (gitignored) | Left at its source; temporary extracts go in `brands/org-contoso/data/` (gitignored) | The client's OneDrive or SharePoint |
| Skills | Brand or shared | Brand-only, so they hand over intact | Shared skills only (for example cost-review) |
| Credentials | Yours | Org service principal or managed identity | Client-owned |

**If your employer doesn't allow internal notes in a personal GitHub repo,** make `brands/org-contoso/` a git submodule that points to a repo in the org's Azure DevOps. The master repo then stores only a pointer, and the org content lives in, and is handed over from, the org's repo. Check with your security team first.

## Set it up

1. **Copy and init:**

   ```bash
   cp -r examples/master-os ~/master-os && cd ~/master-os && git init
   ```

   Push it to a **private** GitHub repo.
2. **Fill in `context/`:** edit `me.md`, and paste 2 real sent emails into `voice.md`.
3. **Rename the examples:** rename `org-contoso` to your org, then edit its `CLAUDE.md` and `context/environments.md`. Replace `fabrikam.md` with your real clients, using `clients/_template.md`.
4. **Test the blocks:**
   - Start `claude` in `~/master-os` and run `/permissions` to see the active rules.
   - Create a dummy `.env` and ask Claude to `cat .env`. It should be refused.
5. **Register what can reach and what runs:**
   - Add a row per connector, CLI profile and identity to `connections/registry.csv`.
   - Add a row per live automation to `automations/registry.csv`, with a flowchart for each (prompt below).
6. **Check it:** run `python3 tools/os_map.py`, open `os-map.html`, then run `/checkup`. In this example, AUT-004 and its identity CON-07 are flagged as not reviewed for over 90 days on purpose, so you can see a finding.
7. **Keep it up:** run `/checkup` weekly. Run a grill-me file-map session every quarter.

## Prompts to reuse

**Annotated map (grill-me):**

> Grill me about every file in here. For each folder, ask why it lives where it does. Recommend a move when the answer doesn't hold up. Record each reason in `decisions/file-map.md` and each move in its moves log. Don't move anything until I say yes.

**Flowchart for one automation:**

> Read row AUT-00X in `automations/registry.csv` and the code at <path>. Draw an n8n-style Mermaid flowchart, left to right: trigger, each step, each data store as a cylinder, and the outputs. Save it to `automations/flows/<id>-<name>.md` and set `flow_doc` in the row.

**Improve the visualization (iterate with any model):**

> Open `os-map.html` and look at it. Change `tools/os_map.py` so that <one change, for example "each brand has its own colour" or "clicking a skill shows which automations use it">. Keep it standard-library Python. Regenerate the map and show me a screenshot.

**New automation:**

> I want <what> to run <when>. Before building, add a draft row to `automations/registry.csv` with status `pilot`: reads, writes, credential and allowed tools, using the least access that works. Draw its flowchart. Ask me to approve both, then build it.

## Enforced vs guidance

| Mechanism | What it does | Limit |
|---|---|---|
| CLAUDE.md and skills | Tell Claude where things are and how to behave | Guidance only. Claude usually follows it, but nothing enforces it. |
| `settings.json` deny and ask rules | Block or prompt for Claude's file tools and for `cat`, `head` and similar shell reads | They don't stop a script that opens files itself. Turn on the [sandbox](https://code.claude.com/docs/en/sandboxing) for OS-level blocks. |
| Working directory | Reads outside it need approval. In a `dontAsk` automation they're denied. | That's why brand automations start in `brands/<brand>/`. |
| Nested brand skills | Load when Claude opens a file in that brand ([skills docs](https://code.claude.com/docs/en/skills)) | A headless run must start inside the brand to use them. |
| `.gitignore` | Keeps `data/`, secrets and client folders out of GitHub | Claude can still read gitignored files on your machine. |

**Note for this repo:** these are real Claude Code files. If a session in this repo opens files under `examples/master-os/`, its CLAUDE.md files and skills load. That's expected.
