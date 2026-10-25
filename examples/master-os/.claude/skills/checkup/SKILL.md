---
name: checkup
description: Health check of the master OS for when it feels messy or I feel overwhelmed. Flags misplaced skills, wrong or dead routing, automations missing from the registry, client work inside the OS, and folders with no recorded reason. Use when I say "checkup", "doctor", "I'm lost" or "where does this go". Read-only.
---

# Checkup

Read-only. Don't move, rename or delete anything until I approve the fixes.

## 1. Run the mechanical checks

```bash
python3 tools/os_map.py --check
```

This catches:

- Broken routing paths and skill folders with no `SKILL.md`
- Registry rows that point to missing skills or flowcharts
- Automations whose credential has no row in `connections/registry.csv`, and connections used across brands
- Stale `last_reviewed` dates, and "As of" dates over 90 days old
- Client folders inside `clients/`, and folders missing from `decisions/file-map.md`
- Wiki lint: pages missing from an index, broken links, raw sources not yet ingested, a `hot.md` over 14 days old, and org or client names in the shared wiki

## 2. Make the judgment calls the script can't

- **Skill placement:** is each shared skill used by 2 or more brands? If only one brand uses it, it belongs in that brand. If a brand skill is now used by others, it moves up to `.claude/skills/`.
- **Routing:** does every row in the root `CLAUDE.md` routing table still match how I actually ask for things? Is there work I do often that has no row?
- **Brand CLAUDE.md files:** under about 100 lines? Do any repeat root rules or contradict each other?
- **Siloing:** is any brand's data, a client name or a figure sitting in a shared file or shared skill?
- **Registry and reality:** for each live automation, do the reads, writes and credential in its row still match the flowchart and the code?
- **Connections:** is any connector or CLI in use that has no row? Can any connection write more than its row says?
- **Expertise vs situational:** does any always-loaded file (root or brand `CLAUDE.md`, `context/me.md`) hold a live number or status? Replace it with a pointer to the source of truth.
- **Clashes:** spot-check 3 key facts. Does each live in one place, with pointers everywhere else?

## 3. Report

A table: Severity (fix now, fix soon, note) | Finding | Proposed fix. Put the top 3 at the top. Then ask which fixes to apply.

For a deeper freshness and drift audit, use the `os-audit` skill if you have it installed.
