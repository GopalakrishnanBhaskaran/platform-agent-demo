# Claude Usage Reference

Practical rules for using Claude Code (and Claude Design) in projects, distilled from about 22 hours of course and tutorial transcripts. Start with **Top rules** and the **CLAUDE.md starter block**. The topic sections have the detail, and each point links to the moment in the video it came from.

## Contents

- [Sources](#sources)
- [How to use this file](#how-to-use-this-file)
- [Top rules](#top-rules)
- [CLAUDE.md starter block](#claudemd-starter-block)
- [1. The core loop: plan, build, verify, evolve](#1-the-core-loop-plan-build-verify-evolve)
- [2. Prompting and planning](#2-prompting-and-planning)
- [3. CLAUDE.md, memory and project structure](#3-claudemd-memory-and-project-structure)
- [4. Context, tokens, models and cost](#4-context-tokens-models-and-cost)
- [5. Skills](#5-skills)
- [6. Sub-agents, agent teams and parallel work](#6-sub-agents-agent-teams-and-parallel-work)
- [7. Connecting tools: API, MCP, CLI](#7-connecting-tools-api-mcp-cli)
- [8. Permissions, security and privacy](#8-permissions-security-and-privacy)
- [9. Hooks and notifications](#9-hooks-and-notifications)
- [10. Automation, scheduling and deployment](#10-automation-scheduling-and-deployment)
- [11. Verification, QA and evals](#11-verification-qa-and-evals)
- [12. Git, GitHub and worktrees](#12-git-github-and-worktrees)
- [13. Browser automation](#13-browser-automation)
- [14. Websites and Claude Design](#14-websites-and-claude-design)
- [15. Knowledge bases, AI OS and executive assistant](#15-knowledge-bases-ai-os-and-executive-assistant)
- [16. Delivering client projects](#16-delivering-client-projects)
- [17. Applying this to Azure and Databricks work](#17-applying-this-to-azure-and-databricks-work)
- [18. Commands and shortcuts](#18-commands-and-shortcuts)
- [19. Prompt templates](#19-prompt-templates)
- [20. Time-sensitive claims to re-check](#20-time-sensitive-claims-to-re-check)
- [Appendix: chapter index](#appendix-chapter-index)

## Sources

Videos come from the Watch links in the course sheet. Four are the course-length videos (2 to 10 hours). The other two are long-form tutorials that the courses build on.

| Code | Video | Length | Presenter |
|---|---|---|---|
| C10 | [Build & Sell with Claude Code (10+ Hour Course)](https://www.youtube.com/watch?v=mpALXah_PBg) | ~10h | Nate Herk |
| NC6 | [Claude Code for Non-Coders (6 Hour Course)](https://www.youtube.com/watch?v=jdbOVepEtUE) | ~6h | Nate Herk |
| OS2 | [Build & Sell Claude Code Operating Systems (2+ Hour Course)](https://www.youtube.com/watch?v=bCljOfCH8Ms) | ~2.5h | Nate Herk |
| DM2 | [Claude Design 2 HOUR COURSE (Beginner to Pro)](https://www.youtube.com/watch?v=ovabeVoWrA0) | ~2h | Nate Herk |
| D3D | [Claude Design Builds Beautiful 3D Websites Instantly](https://www.youtube.com/watch?v=TcFeSjwTo7g) | ~35m | Nate Herk |
| H60 | [How to Use Claude Code Better Than 98% of People](https://www.youtube.com/watch?v=RzLV8sfFdMM) | ~1h | Nate Herk with Cole Medin |

Notes:
- Citations like [C10 2:47:00](https://www.youtube.com/watch?v=mpALXah_PBg&t=10020s) open the video at that point. Where a point draws on several videos, all of them are cited.
- C10 stitches together earlier standalone videos, so some topics appear more than once. They're merged here.
- Model names, prices, plan limits and some commands are as stated when the videos were recorded. Section 20 lists the ones to re-check.
- DM2 notes come from its chapter list and the companion PDF guide, since its second half reuses the D3D build.

## How to use this file

1. Copy the [CLAUDE.md starter block](#claudemd-starter-block) into a project's `CLAUDE.md`, then trim it to fit. Keep the whole file under about 150 to 200 lines.
2. Keep this file as a reference doc. Don't paste it into CLAUDE.md; point to it instead (for example "For Claude Code practices, see `docs/claude-usage-reference.md`"). Pointing to files instead of inlining them is called routing ([section 3](#3-claudemd-memory-and-project-structure)).
3. Use [section 19](#19-prompt-templates) for copy-paste prompts.

## Top rules

These are the points most of the videos agree on.

1. **Plan, build, verify, evolve.** Spend more effort on planning and verification than on building. [H60 9:16](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=556s) [H60 19:52](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=1192s)
2. **Start non-trivial work in plan mode** and have Claude ask questions (one at a time) until it is about 95% confident. [C10 47:35](https://www.youtube.com/watch?v=mpALXah_PBg&t=2855s) [C10 8:00:40](https://www.youtube.com/watch?v=mpALXah_PBg&t=28840s) [NC6 5:31:30](https://www.youtube.com/watch?v=jdbOVepEtUE&t=19890s)
3. **Define "done" before building**: the exact output, how it will be proven, and when to stop. [C10 1:46:44](https://www.youtube.com/watch?v=mpALXah_PBg&t=6404s) [H60 12:41](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=761s)
4. **Make Claude prove its work** with tests, screenshots or browser runs, and put those checks into its to-do list. First passes land around 60 to 70%; with verification they reach about 80 to 92%. [NC6 37:49](https://www.youtube.com/watch?v=jdbOVepEtUE&t=2269s) [H60 12:41](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=761s) [C10 8:00:40](https://www.youtube.com/watch?v=mpALXah_PBg&t=28840s)
5. **CLAUDE.md is a lean router**: role, never-forget rules, and where things live. Detail goes in files it points to. [C10 3:06:07](https://www.youtube.com/watch?v=mpALXah_PBg&t=11167s) [C10 7:42:48](https://www.youtube.com/watch?v=mpALXah_PBg&t=27768s)
6. **Every mistake becomes a permanent upgrade.** Say "update CLAUDE.md / the skill so this never happens again". [H60 51:15](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=3075s) [NC6 48:10](https://www.youtube.com/watch?v=jdbOVepEtUE&t=2890s) [OS2 43:54](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=2634s)
7. **Manage context actively.** Check `/context`, and clear or hand off before quality drops (Nate uses about 60%; see section 4). Use one task per session. [C10 52:20](https://www.youtube.com/watch?v=mpALXah_PBg&t=3140s) [H60 26:55](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=1615s) [NC6 1:55:47](https://www.youtube.com/watch?v=jdbOVepEtUE&t=6947s)
8. **Turn anything you repeat into a skill**, whether it's a process or an instruction, and refine it over 10 to 30 runs. [C10 6:21:18](https://www.youtube.com/watch?v=mpALXah_PBg&t=22878s) [OS2 1:21:40](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=4900s)
9. **Send heavy reading and research to sub-agents** so only summaries reach the main context. They can run on a cheaper model. [C10 6:52:03](https://www.youtube.com/watch?v=mpALXah_PBg&t=24723s) [NC6 2:19:34](https://www.youtube.com/watch?v=jdbOVepEtUE&t=8374s)
10. **Prefer a CLI or direct API (plus a saved reference doc) over MCP** when you only need a few operations. MCP tool definitions cost tokens on every turn. [OS2 39:05](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=2345s) [C10 8:07:38](https://www.youtube.com/watch?v=mpALXah_PBg&t=29258s) [C10 7:27:13](https://www.youtube.com/watch?v=mpALXah_PBg&t=26833s)
11. **Secrets live in `.env` (gitignored) or a secret store.** Never put them in chat, CLAUDE.md, skills or code. [C10 1:32:22](https://www.youtube.com/watch?v=mpALXah_PBg&t=5542s) [NC6 59:21](https://www.youtube.com/watch?v=jdbOVepEtUE&t=3561s)
12. **A prompt is not a permission layer.** Remove tools, scope keys and add deny rules. [H60 44:34](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=2674s) [NC6 3:23:20](https://www.youtube.com/watch?v=jdbOVepEtUE&t=12200s) [NC6 1:09:01](https://www.youtube.com/watch?v=jdbOVepEtUE&t=4141s)
13. **Use allow/deny lists instead of "dangerously skip permissions".** Deny always wins. [C10 8:09:56](https://www.youtube.com/watch?v=mpALXah_PBg&t=29396s) [NC6 1:13:48](https://www.youtube.com/watch?v=jdbOVepEtUE&t=4428s)
14. **Use deterministic code when the steps are fixed** ("boring is beautiful"). Put the model inside a workflow, and deploy scripts rather than agents. [C10 1:00:38](https://www.youtube.com/watch?v=mpALXah_PBg&t=3638s) [NC6 3:17:32](https://www.youtube.com/watch?v=jdbOVepEtUE&t=11852s) [H60 39:48](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=2388s)
15. **Save research once.** Write endpoints and doc notes to a reference file, and hardcode IDs that never change. [NC6 1:04:12](https://www.youtube.com/watch?v=jdbOVepEtUE&t=3852s) [C10 6:22:32](https://www.youtube.com/watch?v=mpALXah_PBg&t=22952s)
16. **Correct early.** Press Esc when it drifts, and push back on mediocre output. [C10 8:04:06](https://www.youtube.com/watch?v=mpALXah_PBg&t=29046s)
17. **Test locally. Push or deploy only when you say so.** [C10 4:37:55](https://www.youtube.com/watch?v=mpALXah_PBg&t=16675s)
18. **Run a security review before anything goes public**: exposed keys, open webhooks, what an outsider could do. [C10 2:20:58](https://www.youtube.com/watch?v=mpALXah_PBg&t=8458s) [C10 4:08:17](https://www.youtube.com/watch?v=mpALXah_PBg&t=14897s)
19. **Ask Claude to explain and to verify, not for its opinion.** "Does this look good?" always gets a yes. [H60 24:37](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=1477s) [C10 41:37](https://www.youtube.com/watch?v=mpALXah_PBg&t=2497s)

## CLAUDE.md starter block

This is built from the rules the videos recommend putting in CLAUDE.md. Replace the placeholders and remove what doesn't apply.

```markdown
# Project: <name>
<One paragraph: what this project does, for whom, and the end goal.>

## How to work
- Start non-trivial tasks in plan mode. Ask me questions one at a time until you are ~95% confident.
- Before building, state the definition of done and how you will prove it (tests, screenshots, sample runs).
- Put verification steps in your to-do list. Don't move to the next step until the current one is verified.
- Test locally. Never push, deploy, publish or send anything external until I explicitly say so.
- Use sub-agents for broad exploration or research; bring back only what's needed.
- If you research something we'll need again (API endpoints, doc details), save it to `references/` and add a pointer below.
- When I correct you, update this file or the relevant skill so it doesn't happen again.
- When something fails repeatedly or you find a workaround, add a one-line bullet under "Applied learning" (under 15 words).

## Secrets and safety
- Secrets live only in `.env` (gitignored) or the platform's secret store. Never print, commit or paste them.
- Ask before deleting files, dropping data, or running anything destructive or irreversible.

## Where things live
- `references/` - API notes and cheat sheets (read only when needed)
- `.claude/skills/` - project skills
- `docs/claude-usage-reference.md` - Claude Code practices

## Applied learning
-
```

---

## 1. The core loop: plan, build, verify, evolve

- **Loop for any task:** plan with context, build, verify, then improve the system. Most people skip the planning and the validation, which matter most. Only say "go rip through this" once there's a detailed spec and a defined proof of done. [H60 9:16](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=556s) [H60 25:48](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=1548s)
- **Spend more time planning than building.** Write one markdown spec with the goal, what success looks like, the validation strategy, and integration points (files to create or edit). Load context docs first, research with sub-agents, then build the plan together with Claude and have it ask lots of questions. [H60 19:52](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=1192s)
- **Verification:** "prove to me it's done and working". Without checks, first passes land around 65 to 70%; with a verification harness, about 92%. Ask "how would the agent verify this the way a user would?" Having it review its own code isn't enough. [H60 12:41](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=761s)
- **Don't optimize for speed.** Let long tasks run 30 to 90 minutes while you work in another session, and judge only the final handoff. [H60 42:11](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=2531s)
- **Chain sessions for big work:** a plan agent writes the spec, an implement agent writes an execution report, and a validate agent reviews it. Split work into phases with one agent each and a handoff report between them. Use this for anything that won't fit before quality drops. [H60 32:50](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=1970s)
- **Evolve:** after any issue, ask which rule, doc or skill change would prevent it. Ask "how could this go wrong?", write a test for that edge case, fix it, and retest. [H60 51:15](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=3075s)
- **Your role shifts from builder to architect and quality owner.** "You no longer write code; you assure the quality." [C10 1:50:15](https://www.youtube.com/watch?v=mpALXah_PBg&t=6615s) [C10 2:47:00](https://www.youtube.com/watch?v=mpALXah_PBg&t=10020s)

## 2. Prompting and planning

- **Treat Claude as a brilliant contractor who is new to your project.** Give it context, constraints and the expected outcome. Vague in, vague out. Voice dictation helps you give fuller context. [C10 45:10](https://www.youtube.com/watch?v=mpALXah_PBg&t=2710s)
- **Prompt levers:** a role ("you are a master content strategist"), background and *why*, negative instructions (what not to do), and a verification ask. [NC6 37:49](https://www.youtube.com/watch?v=jdbOVepEtUE&t=2269s) Give the intent; the official guidance for the latest models also stresses explaining why. [H60 1:05:06](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=3906s)
- **Bad vs better:** "build me a website for my dog walking business" versus naming the business, its sections, services with prices, a contact form, and the style and colors. Then let plan mode ask the rest. [C10 46:21](https://www.youtube.com/watch?v=mpALXah_PBg&t=2781s)
- **Brain-dump pattern for new builds:** the goal, the data needed ("look into different APIs or MCP servers"), "let me know if there are any skills that would help", the deliverable, and "any recommendations for things I haven't thought of". [C10 2:02:01](https://www.youtube.com/watch?v=mpALXah_PBg&t=7321s) [C10 10:48](https://www.youtube.com/watch?v=mpALXah_PBg&t=648s)
- **Read the plan before accepting it.** Correct it ("No, keep planning"), comment on parts of it in the IDE, and @-tag the exact files to use. [C10 13:10](https://www.youtube.com/watch?v=mpALXah_PBg&t=790s) [C10 1:15:52](https://www.youtube.com/watch?v=mpALXah_PBg&t=4552s) [C10 36:44](https://www.youtube.com/watch?v=mpALXah_PBg&t=2204s)
- **Ask for a PRD:** "Here's a rough idea, help me turn this into a solid PRD / project requirement doc." [C10 1:46:44](https://www.youtube.com/watch?v=mpALXah_PBg&t=6404s)
- **Define done:** "I need exactly 75 LinkedIn profiles of CEOs at tech companies in a spreadsheet with name, company, email and profile link. Once you have 75, you're done." [C10 1:46:44](https://www.youtube.com/watch?v=mpALXah_PBg&t=6404s)
- **Pose problems, not just commands** ("How should we handle growth tracking?"), then ask Claude to explain its assumptions. [C10 7:59:25](https://www.youtube.com/watch?v=mpALXah_PBg&t=28765s)
- **Make it ask:** "Use your AskUserQuestion tool and keep asking until you're 95% confident you understand what I need." [C10 8:00:40](https://www.youtube.com/watch?v=mpALXah_PBg&t=28840s)
- **Grill-me** (the original 5-sentence prompt is in [section 19](#19-prompt-templates)). Grilling up front gets a skill to about 90% on the first iteration instead of about 70%. Run it again when you learn something new. [NC6 4:23:58](https://www.youtube.com/watch?v=jdbOVepEtUE&t=15838s)
- **Goal prompts:** `/goal` sets a completion condition, and Claude keeps working until it's met. [NC6 35:23](https://www.youtube.com/watch?v=jdbOVepEtUE&t=2123s)
- **"ultrathink"** gives Claude the maximum thinking budget. Use it for architecture, complex debugging, or when it's stuck after a few tries. [C10 8:09:56](https://www.youtube.com/watch?v=mpALXah_PBg&t=29396s)
- **Push back on mediocre output:** "Scrap that, do a more elegant version" or "try a completely different approach". Then have it update the skill or CLAUDE.md so the lesson sticks. [C10 8:04:06](https://www.youtube.com/watch?v=mpALXah_PBg&t=29046s)
- **Clearing context between closely related steps can lose details** (it forgot a workflow ID). Stay in the thread or write a handoff first. [C10 3:54:04](https://www.youtube.com/watch?v=mpALXah_PBg&t=14044s)
- **Under-specified prompts cause most misses** (for example, it kept using bold markdown). Be explicit about format. [C10 4:00:03](https://www.youtube.com/watch?v=mpALXah_PBg&t=14403s)

## 3. CLAUDE.md, memory and project structure

- **CLAUDE.md is the project's system prompt** and is read before every message, so its size matters. [C10 55:10](https://www.youtube.com/watch?v=mpALXah_PBg&t=3310s) [C10 57:02](https://www.youtube.com/watch?v=mpALXah_PBg&t=3422s)
- **What to put in it:** project overview, stack, architecture, coding conventions, common commands, constraints, and where to find more context. Think of it as what, why and how. [C10 3:06:07](https://www.youtube.com/watch?v=mpALXah_PBg&t=11167s) [C10 57:02](https://www.youtube.com/watch?v=mpALXah_PBg&t=3422s)
- **Keep it under about 150 to 200 lines and use it as a table of contents** ("I know where everything lives"). Rules you only need sometimes, like email style, go in a rules file it points to. [C10 3:06:07](https://www.youtube.com/watch?v=mpALXah_PBg&t=11167s) [C10 7:42:48](https://www.youtube.com/watch?v=mpALXah_PBg&t=27768s) [C10 8:03:01](https://www.youtube.com/watch?v=mpALXah_PBg&t=28981s)
- **Be specific** ("use 2-space indentation", not "format it nicely"). Treat it as a living document; Nate updates his daily. [C10 3:06:07](https://www.youtube.com/watch?v=mpALXah_PBg&t=11167s) [OS2 20:17](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=1217s)
- **Point to cheat sheets instead of inlining them.** A concise CLAUDE.md links to, say, `firecrawl-cheatsheet.md` with a decision guide, which Claude reads only when it needs it. [C10 5:05:27](https://www.youtube.com/watch?v=mpALXah_PBg&t=18327s)
- **Run `/init`** in an existing project to generate CLAUDE.md from the code. In a new project, have Claude draft it from your goal, stack and rules. [C10 58:15](https://www.youtube.com/watch?v=mpALXah_PBg&t=3495s) [C10 7:56:57](https://www.youtube.com/watch?v=mpALXah_PBg&t=28617s)
- **Layers:** a global `~/.claude/CLAUDE.md` for preferences across every project (for example an "AI phrase kill list"), the project `CLAUDE.md`, and a private `CLAUDE.local.md`. Skills and sub-agents also come in global and project versions. [NC6 52:11](https://www.youtube.com/watch?v=jdbOVepEtUE&t=3131s) [NC6 2:01:37](https://www.youtube.com/watch?v=jdbOVepEtUE&t=7297s)
- **Settings files:** `~/.claude/settings.json` holds personal defaults, `.claude/settings.json` holds team standards and gets committed, and `.claude/settings.local.json` holds your local overrides. A deny at any level blocks the action. [C10 3:13:08](https://www.youtube.com/watch?v=mpALXah_PBg&t=11588s)
- **Auto memory** (`~/.claude/projects/<project>/memory/`, indexed by `MEMORY.md`, managed with `/memory`) stores learned facts across sessions. Say "remember that I always prefer X". Think of CLAUDE.md as rules plus a map, and memory as learned facts. [NC6 2:01:37](https://www.youtube.com/watch?v=jdbOVepEtUE&t=7297s) [C10 3:09:35](https://www.youtube.com/watch?v=mpALXah_PBg&t=11375s) [C10 5:52:46](https://www.youtube.com/watch?v=mpALXah_PBg&t=21166s)
- **A self-updating "Applied learning" section:** "When something fails repeatedly or a workaround is found, add a one-line bullet (under 15 words)." Save decisions, not conversations, and review the section for bloat. [NC6 5:31:30](https://www.youtube.com/watch?v=jdbOVepEtUE&t=19890s)
- **Folder structure keeps both you and Claude oriented.** Typical folders are `workflows/`, `tools/` or `scripts/`, `.tmp/`, `references/` and `brand_assets/`. When a project grows, ask "help me figure out a strategy to clean this up", or have it move loose scripts into `scripts/` and update every reference to them. [C10 1:08:57](https://www.youtube.com/watch?v=mpALXah_PBg&t=4137s) [C10 5:26:52](https://www.youtube.com/watch?v=mpALXah_PBg&t=19612s)
- **`.gitignore`** keeps `.env`, OAuth JSON and private files out of git. In VS Code, ignored files show grey, new files green, and modified files yellow. [C10 3:15:34](https://www.youtube.com/watch?v=mpALXah_PBg&t=11734s)
- **Stay tool-agnostic:** plain folders and markdown move to Codex, Antigravity and others in minutes. Keep an `AGENTS.md` copy for Codex, or reference it from CLAUDE.md. [OS2 0:00](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=0s) [NC6 4:13:15](https://www.youtube.com/watch?v=jdbOVepEtUE&t=15195s) [NC6 1:36:34](https://www.youtube.com/watch?v=jdbOVepEtUE&t=5794s)

## 4. Context, tokens, models and cost

**How context fills**
- The context window holds the system prompt, tools, CLAUDE.md, MCP tool definitions, skills metadata, conversation history and files. Every message rereads the whole conversation. In one example, message 30 cost about 31 times as much as message 1, and a 100+ message chat spent 98.5% of its tokens rereading history. [NC6 5:26:41](https://www.youtube.com/watch?v=jdbOVepEtUE&t=19601s) [C10 51:09](https://www.youtube.com/watch?v=mpALXah_PBg&t=3069s)
- **Context rot and "lost in the middle":** quality drops as tokens grow, and the middle of the context is recalled worst. If Claude starts making things up, compact or start fresh. [C10 52:20](https://www.youtube.com/watch?v=mpALXah_PBg&t=3140s) [H60 26:55](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=1615s)
- **The "dumb zone"** (as stated in H60) starts around 250K tokens for Opus and earlier for smaller models. A 1M window gives false security. [H60 26:55](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=1615s)
- **A fresh session already costs about 22K to 55K tokens** before you type, depending on MCP servers, skills and agents. [C10 53:32](https://www.youtube.com/watch?v=mpALXah_PBg&t=3212s) [C10 7:45:09](https://www.youtube.com/watch?v=mpALXah_PBg&t=27909s) [NC6 1:55:47](https://www.youtube.com/watch?v=jdbOVepEtUE&t=6947s)

**Habits**
- Watch `/context` and `/cost`, and set up `/statusline` (model, context %, cost). [C10 53:32](https://www.youtube.com/watch?v=mpALXah_PBg&t=3212s) [C10 7:56:57](https://www.youtube.com/watch?v=mpALXah_PBg&t=28617s) [NC6 5:31:30](https://www.youtube.com/watch?v=jdbOVepEtUE&t=19890s)
- **Clear or compact early.** Nate's rule is to compact or clear at about 60% used. `/compact` takes instructions, for example "/compact keep the API integration decisions and database schema". After 3 or 4 compacts, write a summary and `/clear`. [C10 1:18:06](https://www.youtube.com/watch?v=mpALXah_PBg&t=4686s) [C10 7:58:11](https://www.youtube.com/watch?v=mpALXah_PBg&t=28691s) [NC6 5:31:30](https://www.youtube.com/watch?v=jdbOVepEtUE&t=19890s)
- **Hand off instead of auto-compacting.** A session-handoff skill writes where things started, decisions locked, what shipped, key files, running state, verification, deferred items, open questions and "pick up here". Then `/clear` and paste it in. Auto-compact kicks in late and is slow. [NC6 1:55:47](https://www.youtube.com/watch?v=jdbOVepEtUE&t=6947s)
- **Save plans to files and work in phases**, starting a new session per phase ("look at this plan doc, you're on phase one"). [C10 7:46:24](https://www.youtube.com/watch?v=mpALXah_PBg&t=27984s)
- **Run at most 3 or 4 parallel sessions** so you can keep track of context and review quality. [C10 7:47:31](https://www.youtube.com/watch?v=mpALXah_PBg&t=28051s)
- **Give Claude only what the task needs.** Paste the relevant part of a log, not the whole file, and reference files surgically with `@file`. [C10 7:58:11](https://www.youtube.com/watch?v=mpALXah_PBg&t=28691s) [NC6 5:31:30](https://www.youtube.com/watch?v=jdbOVepEtUE&t=19890s)
- **Remove unused MCP servers, agents and skills** the way you'd cancel unused subscriptions. One MCP server can cost about 18 to 20K tokens per message, so prefer CLIs. [NC6 5:26:41](https://www.youtube.com/watch?v=jdbOVepEtUE&t=19601s) [H60 26:55](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=1615s) [C10 7:45:09](https://www.youtube.com/watch?v=mpALXah_PBg&t=27909s)
- **Batch related asks** into one message, and edit or regenerate instead of sending follow-up corrections. Deny commands whose output floods the context. [NC6 5:26:41](https://www.youtube.com/watch?v=jdbOVepEtUE&t=19601s) [NC6 5:31:30](https://www.youtube.com/watch?v=jdbOVepEtUE&t=19890s)
- **Watch Claude work** and stop it when it loops. Every token spent going the wrong way is wasted. [NC6 5:31:30](https://www.youtube.com/watch?v=jdbOVepEtUE&t=19890s) [C10 8:04:06](https://www.youtube.com/watch?v=mpALXah_PBg&t=29046s)
- **Local semantic search** can cut tokens sharply compared with grep on large codebases (C10 cites up to 97%). [C10 7:48:48](https://www.youtube.com/watch?v=mpALXah_PBg&t=28128s)

**Models and cost (as stated in the videos)**
- Haiku is fastest and cheapest, Sonnet is the balanced daily driver, and Opus is for the heaviest reasoning. A common split: Sonnet for about 80% of work, Opus for planning and tricky bugs (under 20%), Haiku for sub-agents and bulk reading. Nate personally runs Opus for most things. [C10 48:47](https://www.youtube.com/watch?v=mpALXah_PBg&t=2927s) [NC6 5:31:30](https://www.youtube.com/watch?v=jdbOVepEtUE&t=19890s)
- Effort levels: Nate keeps effort high and switches models instead of turning effort up. Fast mode costs more. [NC6 1:14:59](https://www.youtube.com/watch?v=jdbOVepEtUE&t=4499s)
- **Prompt caching:** cached reads cost about 10% of normal input. Switching models mid-session breaks the cache. Don't leave a session idle for long (cache TTL); hand off instead. Start fresh when switching tasks. [NC6 5:31:30](https://www.youtube.com/watch?v=jdbOVepEtUE&t=19890s)
- Sub-agents cost about 7 to 10 times the tokens of a single session, and an agent team with N members costs about N times. [NC6 5:31:30](https://www.youtube.com/watch?v=jdbOVepEtUE&t=19890s) [C10 7:26:03](https://www.youtube.com/watch?v=mpALXah_PBg&t=26763s)
- Ask Claude to estimate a task's tokens and cost up front. Hitting limits is a sign of a power user, not a failure. Start on Pro and upgrade when you hit limits. [NC6 42:36](https://www.youtube.com/watch?v=jdbOVepEtUE&t=2556s) [NC6 5:31:30](https://www.youtube.com/watch?v=jdbOVepEtUE&t=19890s) [C10 4:10:30](https://www.youtube.com/watch?v=mpALXah_PBg&t=15030s)

## 5. Skills

**What and why**
- A skill is a reusable SOP for the agent: `.claude/skills/<name>/SKILL.md` with YAML frontmatter (`name`, plus a `description` saying what it does and when to use it), followed by step-by-step instructions. It can include `references/`, `scripts/` and assets, and can call APIs, run scripts, and spawn or be called by sub-agents. [C10 6:13:04](https://www.youtube.com/watch?v=mpALXah_PBg&t=22384s) [C10 6:14:16](https://www.youtube.com/watch?v=mpALXah_PBg&t=22456s) [OS2 1:13:22](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=4402s)
- **The value is leverage**, for you and your team: one person's best method becomes everyone's skill once it's committed to git. [C10 6:11:51](https://www.youtube.com/watch?v=mpALXah_PBg&t=22311s) [OS2 1:11:00](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=4260s)
- **There are two types.** *Capability uplift* skills teach Claude to do something better (frontend-design, for example) and may become obsolete as models improve. *Encoded preference* skills capture your specific sequence of steps and stay useful. [C10 6:35:31](https://www.youtube.com/watch?v=mpALXah_PBg&t=23731s)
- **Progressive disclosure:** at startup only the frontmatter of each skill is read (~100 tokens each). The full SKILL.md is read when the skill is chosen (~1 to 2K tokens), and references and scripts only when needed. Keep SKILL.md under 500 lines. [C10 6:20:10](https://www.youtube.com/watch?v=mpALXah_PBg&t=22810s) [C10 6:21:18](https://www.youtube.com/watch?v=mpALXah_PBg&t=22878s)
- **Triggering:** use `/skill-name` or plain language. Claude matches your request against the skill descriptions and otherwise falls back to general knowledge. [C10 6:18:58](https://www.youtube.com/watch?v=mpALXah_PBg&t=22738s)
- **Location:** project skills go in `.claude/skills`; global skills go in `~/.claude/skills` (for example frontend-design, company context, tone of voice). Ask Claude which one it installed into. [C10 2:13:50](https://www.youtube.com/watch?v=mpALXah_PBg&t=8030s) [C10 6:34:19](https://www.youtube.com/watch?v=mpALXah_PBg&t=23659s)
- **Skills plus a CLI beat MCP:** the CLI gives access, and the skill says how to use it in your workflow. [H60 1:01:40](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=3700s)

**Building**
- Build a skill whenever you repeat a process or keep repeating an instruction ("no em dashes"). A skill can be 50 lines, or even 2 sentences. [C10 6:24:55](https://www.youtube.com/watch?v=mpALXah_PBg&t=23095s) [NC6 1:48:30](https://www.youtube.com/watch?v=jdbOVepEtUE&t=6510s)
- **Easiest path:** do the task with Claude once, then say "This is something I do once a day. Let's turn this into a skill. Ask me more questions so you have all the information you need." [C10 6:21:18](https://www.youtube.com/watch?v=mpALXah_PBg&t=22878s) [NC6 1:38:58](https://www.youtube.com/watch?v=jdbOVepEtUE&t=5938s)
- **Six-step framework:** (1) name and trigger phrases, (2) a one-sentence goal and output, (3) the step-by-step process including decisions, (4) reference files, (5) rules and guardrails for what could go wrong, (6) a self-improvement loop. [C10 6:24:55](https://www.youtube.com/watch?v=mpALXah_PBg&t=23095s)
- **Use Anthropic's skill-creator** (install it from the `/plugin` menu, then restart). It builds skills, runs evals against example outputs, benchmarks with and without the skill (pass rate, time, tokens), and tunes descriptions when you have 10+ skills that misfire. Re-run evals when a new model ships; retire a skill if the base model beats it. [C10 6:38:00](https://www.youtube.com/watch?v=mpALXah_PBg&t=23880s) [C10 6:40:23](https://www.youtube.com/watch?v=mpALXah_PBg&t=24023s) [NC6 1:38:58](https://www.youtube.com/watch?v=jdbOVepEtUE&t=5938s)
- **Have Claude research the official docs** on skill and sub-agent file format once, and save the result so every new skill follows it. [C10 6:04:40](https://www.youtube.com/watch?v=mpALXah_PBg&t=21880s)
- **Migrate custom GPTs and Claude Projects:** "turn this into a skill for me." [C10 6:07:04](https://www.youtube.com/watch?v=mpALXah_PBg&t=22024s)
- **Vet third-party skills** for malicious or injected instructions. Skills are portable to Cursor, Codex and Antigravity. [C10 6:18:58](https://www.youtube.com/watch?v=mpALXah_PBg&t=22738s) [NC6 2:39:31](https://www.youtube.com/watch?v=jdbOVepEtUE&t=9571s)

**Improving**
- **Feedback cycle:** invoke it, watch it work, give feedback, have it update the skill, and repeat. It gets noticeably better by run 10 to 30. On the first test run, say "make sure you're updating your skill document with your findings from this run". It will add a known-issues section. [C10 6:21:18](https://www.youtube.com/watch?v=mpALXah_PBg&t=22878s) [C10 5:20:59](https://www.youtube.com/watch?v=mpALXah_PBg&t=19259s)
- **Token savers you'll spot by watching:** hardcode stable IDs (such as list IDs) instead of looking them up every run; delegate heavy searching to a specialist sub-agent; scrape the docs once into `reference.md` instead of web-searching each run. [C10 6:22:32](https://www.youtube.com/watch?v=mpALXah_PBg&t=22952s)

**Debugging**

| Symptom | Fix |
|---|---|
| Wrong steps or wrong order | Edit the SKILL.md instructions |
| Missing tone, style or context | Add reference files and point to them |
| Same mistake repeated | Add a rule |
| Struggles with a tool or keeps searching | Add a reference doc for that tool |
| Good but not great | Run it repeatedly and nitpick |
| Doesn't trigger | Make the YAML description more specific |
| Triggers too often | `disable-model-invocation` (slash-command only) |

Other frontmatter fields: `allowed-tools`, `argument-hint`, `model`, `context`, `hooks`, `agent`. [C10 6:32:01](https://www.youtube.com/watch?v=mpALXah_PBg&t=23521s) [C10 6:33:10](https://www.youtube.com/watch?v=mpALXah_PBg&t=23590s)

## 6. Sub-agents, agent teams and parallel work

**Sub-agents**
- The main session delegates to specialists (reviewer, test runner, researcher...). Each starts with a **fresh context**, its own model and its own tools, and returns only a summary. In one demo, a sub-agent used about 40K tokens while the main session stayed at about 29K in total. [C10 6:52:03](https://www.youtube.com/watch?v=mpALXah_PBg&t=24723s) [C10 7:05:04](https://www.youtube.com/watch?v=mpALXah_PBg&t=25504s)
- **Why use them:** to keep the main context clean, to enforce tool restrictions for risky actions, to reuse configs across projects and teams, for specialization, and to control cost (Haiku for research). [C10 6:54:24](https://www.youtube.com/watch?v=mpALXah_PBg&t=24864s)
- **When:** delegate self-contained work, large reads, parallel independent tasks, or anything that needs a fresh, unbiased reviewer. Stay in the main thread for back-and-forth, quick edits, sequential dependent steps, and work that needs the whole conversation or needs to ask you questions. [C10 6:56:53](https://www.youtube.com/watch?v=mpALXah_PBg&t=25013s) [NC6 2:39:31](https://www.youtube.com/watch?v=jdbOVepEtUE&t=9571s)
- **Built-in agents:** Explore (Haiku, read-only), Plan (inherits the model, read-only) and general-purpose (all tools). [C10 6:59:13](https://www.youtube.com/watch?v=mpALXah_PBg&t=25153s)
- **Create one with `/agents`** (in the terminal), choose "generate with Claude" and describe it. Then pick tools, model, color and memory, and trim the generated description. Files live in `.claude/agents/` or `~/.claude/agents/`. [C10 7:00:25](https://www.youtube.com/watch?v=mpALXah_PBg&t=25225s) [NC6 2:30:12](https://www.youtube.com/watch?v=jdbOVepEtUE&t=9012s)
- **The description drives delegation**, for example "Use immediately after writing or modifying code". If an agent misfires, ask Claude to compare the agent's description with your prompt and explain why it didn't fire. [C10 6:58:01](https://www.youtube.com/watch?v=mpALXah_PBg&t=25081s) [NC6 2:30:12](https://www.youtube.com/watch?v=jdbOVepEtUE&t=9012s)
- **Patterns:** small single-purpose agents work best; run research in parallel and then synthesize; chain agents in a fixed order (a deterministic sequence of non-deterministic steps); skills can delegate to agents, and agents can preload skills. Ctrl+B sends an agent to the background and Ctrl+O expands its output. [C10 7:07:29](https://www.youtube.com/watch?v=mpALXah_PBg&t=25649s) [C10 7:05:04](https://www.youtube.com/watch?v=mpALXah_PBg&t=25504s)
- **Weak spot:** sub-agents are great at research and gathering scattered context but poor at handing work to each other. [H60 39:48](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=2388s)

**Agent teams (experimental)**
- A team lead, a shared task list, and teammates who **message each other** and work in parallel (for example, QA sends work back to the developers until it passes). Turn it on with the env var from the docs in `.claude/settings.local.json`, then start a new session. [C10 7:11:03](https://www.youtube.com/watch?v=mpALXah_PBg&t=25863s) [C10 7:14:27](https://www.youtube.com/watch?v=mpALXah_PBg&t=26067s) [NC6 4:30:59](https://www.youtube.com/watch?v=jdbOVepEtUE&t=16259s)
- **Prompt pattern:** goal, then "create a team of N teammates using <model>", then each teammate's role, deliverable and who to message when done, then the final deliverables. Say "use the team create function" or it may spawn plain sub-agents instead. [C10 7:16:44](https://www.youtube.com/watch?v=mpALXah_PBg&t=26204s) [NC6 4:30:59](https://www.youtube.com/watch?v=jdbOVepEtUE&t=16259s)
- **Do:** give each agent its own files, define outputs, name who receives what, use 3 to 5 teammates, and give full context (they start with none but inherit permissions, files, MCP servers and skills). Plan-approval mode makes teammates plan before they act. [C10 7:17:54](https://www.youtube.com/watch?v=mpALXah_PBg&t=26274s) [C10 7:23:39](https://www.youtube.com/watch?v=mpALXah_PBg&t=26619s)
- **Pitfalls:** constant permission prompts (pre-approve commands), overwritten work (assign file owners), idle agents (give explicit work), token burn (use fewer agents), lost work (save to temp files). Shut the team down cleanly instead of force-killing it. [C10 7:24:51](https://www.youtube.com/watch?v=mpALXah_PBg&t=26691s) [C10 7:26:03](https://www.youtube.com/watch?v=mpALXah_PBg&t=26763s)
- **Skip teams** for sequential work, shared-file work, simple tasks, or when the agents don't need to talk. Use sub-agents instead. [C10 7:26:03](https://www.youtube.com/watch?v=mpALXah_PBg&t=26763s)
- **Debate panels and adversarial review:** personas research and argue to consensus, or a separate session is told to "be mean" about the first session's work. [H60 57:10](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=3430s)

**Parallel sessions**
- Boris Cherny (who created Claude Code) runs about 5 sessions in the terminal plus 5 to 10 on the web. [C10 33:16](https://www.youtube.com/watch?v=mpALXah_PBg&t=1996s) For most people, 3 or 4 that they actually track is the practical limit. [C10 7:47:31](https://www.youtube.com/watch?v=mpALXah_PBg&t=28051s)
- Use git worktrees so parallel sessions don't overwrite each other ([section 12](#12-git-github-and-worktrees)). [C10 8:07:38](https://www.youtube.com/watch?v=mpALXah_PBg&t=29258s)
- Dynamic workflows that spawn dozens of sub-agents burn session limits fast. [NC6 2:39:31](https://www.youtube.com/watch?v=jdbOVepEtUE&t=9571s)

## 7. Connecting tools: API, MCP, CLI

- **Every tool has a way in:** MCP, API, CLI or browser automation. Map your core tools first: revenue, customers, calendar, comms, tasks, meetings, knowledge. [OS2 14:21](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=861s) [NC6 1:19:53](https://www.youtube.com/watch?v=jdbOVepEtUE&t=4793s)
- **An API key is a password.** Have Claude create `.env` with a placeholder, paste the key in yourself, confirm `.env` is in `.gitignore`, then have Claude make a test request. [NC6 59:21](https://www.youtube.com/watch?v=jdbOVepEtUE&t=3561s) [C10 1:32:22](https://www.youtube.com/watch?v=mpALXah_PBg&t=5542s)
- **Prefer direct APIs plus a reference doc:** "Use the API because it's more token efficient than the MCP server. Research the API documentation, set up a reference markdown file with all endpoints so you don't research again, create a .env and I'll put my key in it." Then copy only the endpoints a skill needs into that skill. [OS2 39:05](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=2345s)
- **MCP:** one standard interface to all of a service's actions. Install it with the vendor's documented command, and restart or reload (Ctrl+Shift+P, "Developer: Reload Window") afterwards. `.mcp.json` can contain real tokens, so don't share it. If Claude runs an install command that includes a key, that key ends up in the conversation history; run high-risk ones yourself. [C10 1:32:22](https://www.youtube.com/watch?v=mpALXah_PBg&t=5542s) [C10 5:04:15](https://www.youtube.com/watch?v=mpALXah_PBg&t=18255s) [C10 3:48:04](https://www.youtube.com/watch?v=mpALXah_PBg&t=13684s)
- **Use MCP only for what you need.** If you only read one database, a hardcoded endpoint beats loading the whole MCP server. [C10 8:07:38](https://www.youtube.com/watch?v=mpALXah_PBg&t=29258s)
- **CLIs are lightweight:** the Google Workspace CLI (`gws`) covers Drive, Gmail, Calendar, Docs, Sheets and Slides with JSON output and recipe skills; BigQuery `bq` lets you ask questions in plain English; Playwright CLI handles the browser. [C10 5:28:01](https://www.youtube.com/watch?v=mpALXah_PBg&t=19681s) [C10 8:09:56](https://www.youtube.com/watch?v=mpALXah_PBg&t=29396s) [C10 7:27:13](https://www.youtube.com/watch?v=mpALXah_PBg&t=26833s)
- **The Context7 MCP** pulls current, version-specific library docs so Claude doesn't use deprecated APIs. [C10 8:11:10](https://www.youtube.com/watch?v=mpALXah_PBg&t=29470s)
- **Write a cheat sheet after connecting:** "create a <tool> cheat sheet markdown: the tools and when to use each". [C10 5:04:15](https://www.youtube.com/watch?v=mpALXah_PBg&t=18255s)
- **Desktop-app connectors** (one-click OAuth) are easy but tie you to that app. `.env`, API and CLI connections work in any harness. [NC6 1:36:34](https://www.youtube.com/watch?v=jdbOVepEtUE&t=5794s)
- **Give the AI its own account and scoped key**, read-only where possible. Separate keys per agent also show spend per automation. [OS2 35:37](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=2137s) [NC6 1:09:01](https://www.youtube.com/watch?v=jdbOVepEtUE&t=4141s)
- **"No, you do it."** Give raw install URLs and have Claude run the install steps; it will say when something truly needs you. [C10 3:46:54](https://www.youtube.com/watch?v=mpALXah_PBg&t=13614s) [C10 2:05:26](https://www.youtube.com/watch?v=mpALXah_PBg&t=7526s)

## 8. Permissions, security and privacy

- **Modes:** plan (read, think, search; no edits), accept edits (edits files, asks before running commands), auto (a classifier checks risky actions), and bypass (full autonomy; enable it in settings). Typical flow: plan, approve, then let it run. [C10 47:35](https://www.youtube.com/watch?v=mpALXah_PBg&t=2855s) [NC6 1:09:01](https://www.youtube.com/watch?v=jdbOVepEtUE&t=4141s) [OS2 42:41](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=2561s)
- **A prompt is not a permission layer.** Assume the agent will use anything it can reach. "Never delete the DB" eventually fails; blocking DELETE is better; but it can still write a script that deletes. Real incidents: an agent emailed a discount code to an entire list, and a forgotten routine posted private stats into public channels. [H60 44:34](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=2674s) [NC6 3:23:20](https://www.youtube.com/watch?v=jdbOVepEtUE&t=12200s) [NC6 3:28:10](https://www.youtube.com/watch?v=jdbOVepEtUE&t=12490s)
- **Least privilege:** if an agent should only draft, don't give it a send tool. Scope keys (named per purpose, credit caps, limited endpoints). "Would you give a new hire a credit card and say don't spend?" [NC6 3:23:20](https://www.youtube.com/watch?v=jdbOVepEtUE&t=12200s) [NC6 1:09:01](https://www.youtube.com/watch?v=jdbOVepEtUE&t=4141s)
- **Deny lists:** "Here's X, Y, Z I want to never happen. Help me update the settings file so you physically cannot do those things", then test them. Allow known-safe commands and deny destructive ones; deny wins over allow. [NC6 1:13:48](https://www.youtube.com/watch?v=jdbOVepEtUE&t=4428s) [C10 8:09:56](https://www.youtube.com/watch?v=mpALXah_PBg&t=29396s)
- **Unattended runs** (scheduled tasks, routines) need tighter permissions, for example denying delete and remove commands. [C10 2:51:54](https://www.youtube.com/watch?v=mpALXah_PBg&t=10314s)
- **Security review before publishing:** "do a full security review of anything I've pushed... make sure I don't have credentials exposed". Check exposed webhooks (anyone could spam them and burn your credits) and "what could people do now that this is out there?" [C10 2:20:58](https://www.youtube.com/watch?v=mpALXah_PBg&t=8458s) [C10 4:04:50](https://www.youtube.com/watch?v=mpALXah_PBg&t=14690s) [C10 4:08:17](https://www.youtube.com/watch?v=mpALXah_PBg&t=14897s)
- **Webhook hardening:** HTTPS, signature or token verification, no sensitive data in URLs, rate limits. Also guard against prompt injection. [C10 9:41:38](https://www.youtube.com/watch?v=mpALXah_PBg&t=34898s) [C10 9:42:52](https://www.youtube.com/watch?v=mpALXah_PBg&t=34972s)
- **Privacy:** closed models send data to the provider. Don't put sensitive or regulated company data into Claude without approval. For strict data-sovereignty needs, use self-hosting or local models. [NC6 1:17:25](https://www.youtube.com/watch?v=jdbOVepEtUE&t=4645s) [C10 9:44:02](https://www.youtube.com/watch?v=mpALXah_PBg&t=35042s)
- **Keep an inventory of running automations**, and vet them before leaving them unattended. [NC6 3:28:10](https://www.youtube.com/watch?v=jdbOVepEtUE&t=12490s)
- **Vet extensions, skills and agents** before installing: verified publisher, a real person behind it, no outbound calls or remote scripts. [C10 8:22:59](https://www.youtube.com/watch?v=mpALXah_PBg&t=30179s) [NC6 2:39:31](https://www.youtube.com/watch?v=jdbOVepEtUE&t=9571s)

## 9. Hooks and notifications

- **Hooks run your code on events** (session start or end, before a tool runs...). [H60 46:45](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=2805s)
- **Uses:**
  - Pre-tool-use security checks (block reads of `.env`, deletes, forbidden folders).
  - Writing a summary to a daily log on compaction or session end.
  - A sound when Claude finishes or needs input, which helps when you're running many sessions.

  [H60 46:45](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=2805s) [C10 2:54:15](https://www.youtube.com/watch?v=mpALXah_PBg&t=10455s) [C10 8:05:15](https://www.youtube.com/watch?v=mpALXah_PBg&t=29115s)
- **Setup is one sentence:** "Set up a hook: play a sound every time you finish talking to me." [C10 2:55:23](https://www.youtube.com/watch?v=mpALXah_PBg&t=10523s)

## 10. Automation, scheduling and deployment

**Choose the simplest design**
- **The AI systems pyramid**, from least to most autonomy, cost and risk: chatbot or human-triggered skill, then a deterministic workflow, then an AI workflow (fixed steps with one AI step), then an agent. Pick the simplest one that does the job. [NC6 3:17:32](https://www.youtube.com/watch?v=jdbOVepEtUE&t=11852s)
- **Rebuilding agents as workflows pays off.** Inbox agents with huge prompts and many tools were unreliable. Rebuilt as workflows with objective routing rules and AI only for extraction and summaries, they had near-zero failures and were cheaper and easier to debug. [NC6 3:23:20](https://www.youtube.com/watch?v=jdbOVepEtUE&t=12200s)
- **Self-healing only happens interactively.** Once deployed, you ship the workflows and tools, not the agent, so a deployed job behaves like normal code. Battle-test it before deploying. [C10 2:29](https://www.youtube.com/watch?v=mpALXah_PBg&t=149s) [C10 1:49:03](https://www.youtube.com/watch?v=mpALXah_PBg&t=6543s) [C10 2:16:10](https://www.youtube.com/watch?v=mpALXah_PBg&t=8170s)
- **Webhooks beat polling** ("doorbell vs checking the door every 10 minutes"), and template fills don't need AI. [NC6 5:17:23](https://www.youtube.com/watch?v=jdbOVepEtUE&t=19043s)

**In-session and desktop scheduling**
- **`/loop`** ("every 5 minutes check the deploy") and one-off reminders work on every surface. They run in the current session (so context grows), are tied to that session, expire after 3 days, and don't catch up on missed runs. Use them for "help me now" monitoring. [C10 2:56:38](https://www.youtube.com/watch?v=mpALXah_PBg&t=10598s) [C10 3:02:31](https://www.youtube.com/watch?v=mpALXah_PBg&t=10951s)
- **Desktop scheduled tasks:**
  - Set up from the Schedule tab or `/schedule`. The computer must be on and the app open; missed runs catch up.
  - Each run is a fresh session, so lock down permissions and run the task once by hand to confirm it never needs approval.
  - "Turn my morning-coffee skill into a scheduled task at 6 a.m."

  [C10 2:47:00](https://www.youtube.com/watch?v=mpALXah_PBg&t=10020s) [C10 2:50:39](https://www.youtube.com/watch?v=mpALXah_PBg&t=10239s)
- **Memory across stateless runs:** keep one status file per task that each run overwrites (last run, what happened, known issues). Read it first, then do the task, then overwrite it. End with "send me a message when done". [C10 2:53:06](https://www.youtube.com/watch?v=mpALXah_PBg&t=10386s) [C10 2:55:23](https://www.youtube.com/watch?v=mpALXah_PBg&t=10523s)

**Cloud routines (remote)**
- They need a GitHub repo, which is cloned fresh for each run. Put keys in the cloud environment's env vars, since `.env` isn't in git, and say so explicitly: "Use it directly from the environment. Don't look for a .env."
- Network access set to "Trusted" can block APIs; "Full" carries more risk.
- Browser sessions that need cookies fail.
- Use a specific one-shot prompt that names the skill and the order of steps, keep the repo lean, add "if this fails, send me a Slack message", and test with Run now.

[OS2 1:38:13](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=5893s) [OS2 1:39:31](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=5971s) [NC6 4:45:07](https://www.youtube.com/watch?v=jdbOVepEtUE&t=17107s)

**Deploying code**
- **Modal:** pay per run, secrets store, deployment history, logs, Run now. Paste a failed run's log back into Claude to fix it. Run a security review before deploying. [C10 2:19:46](https://www.youtube.com/watch?v=mpALXah_PBg&t=8386s) [C10 2:23:24](https://www.youtube.com/watch?v=mpALXah_PBg&t=8604s)
- **Trigger.dev:** scheduled tasks, automatic retries, queues, orchestration, and dev and prod environments. Add env vars for both environments, connect the GitHub repo, and pushes to the main branch deploy to prod. Split jobs into small tasks (find leads, then create each lead) so one failure retries alone, and ask for idempotency and dedup up front. [C10 2:27:01](https://www.youtube.com/watch?v=mpALXah_PBg&t=8821s) [C10 2:37:38](https://www.youtube.com/watch?v=mpALXah_PBg&t=9458s) [C10 2:42:16](https://www.youtube.com/watch?v=mpALXah_PBg&t=9736s)
- **Think through risk per automation:** cap spend on keys, add provider fallbacks, and hardcode destinations ("how can you prove to me it can only send to my DM?"). Have Claude run the deploy commands while you only do the browser login. [NC6 5:11:27](https://www.youtube.com/watch?v=jdbOVepEtUE&t=18687s)
- **After a successful deploy:** "store this in CLAUDE.md or create a skill so next time you push to Modal you have all that information". [C10 2:25:45](https://www.youtube.com/watch?v=mpALXah_PBg&t=8745s)

## 11. Verification, QA and evals

- **Make it prove its work:** "If a human handed you this, how would you verify it?" Then have Claude do exactly that and report what it ran and why it's confident. [NC6 37:49](https://www.youtube.com/watch?v=jdbOVepEtUE&t=2269s) [H60 12:41](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=761s)
- **Put checks in the to-do list:** build, then screenshot and check, then do a functional check in the browser. "Don't move on until you're 95% confident this step is good." [C10 8:00:40](https://www.youtube.com/watch?v=mpALXah_PBg&t=28840s)
- **Visual loops:** Puppeteer or Playwright screenshots compared against a reference (2 or 3 passes before v1). Give Claude Chrome DevTools so it can see its own output, for example generated slides. [C10 4:20:13](https://www.youtube.com/watch?v=mpALXah_PBg&t=15613s) [C10 8:05:15](https://www.youtube.com/watch?v=mpALXah_PBg&t=29115s) [C10 5:37:29](https://www.youtube.com/watch?v=mpALXah_PBg&t=20249s)
- **Automated QA:** "spin up the server, use browser automation to fill fields and click through, note bugs and fix them; run headed so I can watch". It loops until the tests pass; then turn that into a QA skill. [C10 7:29:32](https://www.youtube.com/watch?v=mpALXah_PBg&t=26972s) [C10 7:33:05](https://www.youtube.com/watch?v=mpALXah_PBg&t=27185s)
- **Evals:** a golden dataset of about 100 to a few hundred input and expected-output pairs. Re-run it before production and before model changes. [NC6 3:31:46](https://www.youtube.com/watch?v=jdbOVepEtUE&t=12706s) [C10 6:40:23](https://www.youtube.com/watch?v=mpALXah_PBg&t=24023s)
- **Edge cases:** "I'm concerned about what could go wrong. Help me figure out all the edge cases and how to make sure failures are safe failures." Then add guardrails: notify on error, auto-shutdown, logs. [NC6 3:31:46](https://www.youtube.com/watch?v=jdbOVepEtUE&t=12706s) [C10 9:47:28](https://www.youtube.com/watch?v=mpALXah_PBg&t=35248s)
- **Ask it to explain and verify, not to give an opinion.** Use `/btw` to ask side questions without polluting the main context. [H60 24:37](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=1477s) [H60 56:03](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=3363s)

## 12. Git, GitHub and worktrees

- **Git** is local version control: repo, commit (snapshot), branch, push, pull, merge. **GitHub** hosts it in the cloud for backup, collaboration, pull requests, history, and using the same project on another device. Just state what you want ("save my work", "roll back", "share this") and Claude handles the git commands. [C10 7:50:03](https://www.youtube.com/watch?v=mpALXah_PBg&t=28203s) [C10 7:52:23](https://www.youtube.com/watch?v=mpALXah_PBg&t=28343s)
- **Put your assistant or OS project in a private repo** so it syncs across machines and plugs into cloud harnesses. [C10 5:52:46](https://www.youtube.com/watch?v=mpALXah_PBg&t=21166s) [OS2 1:35:50](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=5750s)
- **Rule for websites and apps:** test on localhost and push only when you say so. A push to GitHub then auto-deploys through Vercel or Trigger.dev. [C10 4:37:55](https://www.youtube.com/watch?v=mpALXah_PBg&t=16675s) [C10 2:43:29](https://www.youtube.com/watch?v=mpALXah_PBg&t=9809s)
- **Check what `.gitignore` excludes:** a site broke on Vercel because its animation frames were ignored. [C10 4:55:50](https://www.youtube.com/watch?v=mpALXah_PBg&t=17750s)
- **Worktrees** check out branches in separate folders so parallel Claude sessions don't collide (`claude --worktree <feature>`). Merge the branches back when done. [C10 7:55:49](https://www.youtube.com/watch?v=mpALXah_PBg&t=28549s) [C10 8:07:38](https://www.youtube.com/watch?v=mpALXah_PBg&t=29258s)

## 13. Browser automation

- In plan mode, ask Claude to compare browser tools and install one. Playwright CLI was preferred over the Chrome DevTools MCP because the MCP's tool definitions eat context. Run `/init` afterwards. [C10 7:27:13](https://www.youtube.com/watch?v=mpALXah_PBg&t=26833s) [C10 7:28:21](https://www.youtube.com/watch?v=mpALXah_PBg&t=26901s)
- Pair the Playwright scripts it writes with a skill so browser tasks become repeatable. [C10 7:29:32](https://www.youtube.com/watch?v=mpALXah_PBg&t=26972s)
- **Scraping:** it switched search engines when blocked. Give it a hard stop condition ("don't stop until you find five phone numbers"). [C10 7:35:30](https://www.youtube.com/watch?v=mpALXah_PBg&t=27330s) [C10 7:36:47](https://www.youtube.com/watch?v=mpALXah_PBg&t=27407s)
- **Logged-in sites:** use a persistent browser profile, log in by hand once, and the session is reused. Correct it with precise UI hints ("sort by newest; a liked post shows a yellow icon"). It took about 4 or 5 iterations, then became a skill. [C10 7:37:57](https://www.youtube.com/watch?v=mpALXah_PBg&t=27477s) [C10 7:40:23](https://www.youtube.com/watch?v=mpALXah_PBg&t=27623s)

## 14. Websites and Claude Design

**Websites with Claude Code**
- **CLAUDE.md rule:** "Always invoke the frontend-design skill before writing any frontend code, every session, no exceptions." Put the logo and guidelines in a `brand_assets/` folder and @-tag them. [C10 4:16:27](https://www.youtube.com/watch?v=mpALXah_PBg&t=15387s) [C10 4:17:43](https://www.youtube.com/watch?v=mpALXah_PBg&t=15463s)
- **Screenshot loop:** "Set up Puppeteer to take screenshots" and compare in 2 passes. Define how screenshots are named, or delete them after. Turn the loop off for animated backgrounds, or it over-engineers chasing a match. [C10 4:20:13](https://www.youtube.com/watch?v=mpALXah_PBg&t=15613s) [C10 4:26:11](https://www.youtube.com/watch?v=mpALXah_PBg&t=15971s) [C10 4:30:47](https://www.youtube.com/watch?v=mpALXah_PBg&t=16247s)
- **Clone an inspiration site** (Dribbble, Godly, Awwwards): take a full-size screenshot (DevTools, Ctrl+Shift+P, "Capture full size screenshot"), copy the styles, ask for a clone, then say "work in our brand assets". Add components from 21st.dev. [C10 4:22:32](https://www.youtube.com/watch?v=mpALXah_PBg&t=15752s) [C10 4:23:44](https://www.youtube.com/watch?v=mpALXah_PBg&t=15824s) [C10 4:29:38](https://www.youtube.com/watch?v=mpALXah_PBg&t=16178s)
- **3D scroll sites:** generate start and end frames with an image model, animate them with a video model, then extract frames with FFmpeg and map them to scroll position. After each build: "make sure everything I liked or disliked is reflected in the SKILL.md". [C10 4:40:07](https://www.youtube.com/watch?v=mpALXah_PBg&t=16807s) [C10 4:43:52](https://www.youtube.com/watch?v=mpALXah_PBg&t=17032s) [C10 4:53:26](https://www.youtube.com/watch?v=mpALXah_PBg&t=17606s)
- **Deploy:** connect GitHub to Vercel; each push redeploys. Check mobile layout with the F12 device toggle. Add a custom domain through DNS records, with Claude walking you through it. [C10 4:34:22](https://www.youtube.com/watch?v=mpALXah_PBg&t=16462s) [D3D 18:53](https://www.youtube.com/watch?v=TcFeSjwTo7g&t=1133s)

**Claude Design**
- **B.R.A.N.D.:** Brainstorm in Claude Chat, Reference real things, Architect one design system, Navigate with the in-canvas tools (one visual change per prompt), Distribute (export, hand off, deploy). Don't use Design for brainstorming or for small manual fixes. [DM2 1:49:26](https://www.youtube.com/watch?v=ovabeVoWrA0&t=6566s)
- **Build one design system first** (name, logo PNG, palette, type, notes on feel) and reuse it everywhere. Review each section; it tends to redraw logos, so say "the logo should not be modified from the PNG I uploaded". [DM2 5:24](https://www.youtube.com/watch?v=ovabeVoWrA0&t=324s)
- **Save quota:** brainstorm and write specs or outlines in Chat, sketch layout boxes first, use comments and inline edits instead of new prompts, and ask for a Tweaks panel ("add a bunch of things I can tweak: colors, sliders, panels"). [D3D 3:36](https://www.youtube.com/watch?v=TcFeSjwTo7g&t=216s) [D3D 10:38](https://www.youtube.com/watch?v=TcFeSjwTo7g&t=638s) [DM2 19:50](https://www.youtube.com/watch?v=ovabeVoWrA0&t=1190s)
- **Quota drains:** Opus for everything, skipping wireframes, design-system ingestion, and long threads. Claude Design has its own usage meter; when it runs out, export and continue in Claude Code. [D3D 27:04](https://www.youtube.com/watch?v=TcFeSjwTo7g&t=1624s)
- **Hand off to Claude Code:** download the ZIP, open it in VS Code with Claude Code, push to a private repo, then deploy to Vercel. One fix needed was renaming the main HTML to `index.html`. [D3D 18:53](https://www.youtube.com/watch?v=TcFeSjwTo7g&t=1133s)

## 15. Knowledge bases, AI OS and executive assistant

- **AI OS = the 4 Cs, in order:** Context (who you are, your business, your voice), Connections (data it can reach), Capabilities (skills built from SOPs), Cadence (it acts on a schedule). Test it by asking a question in a fresh session: does it answer like a teammate or a stranger? [OS2 10:42](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=642s)
- **Executive assistant build:**
  1. Create a home folder with git.
  2. Run an interview prompt that builds `context/` (me, work, team, priorities, goals), a `decisions/` log, `projects/<name>/README.md`, `references/`, `templates/`, a communication-style rule, and a short CLAUDE.md that routes to all of them.
  3. Add a first skill that connects your task tool.
  4. Use it as your only assistant for a week.

  [C10 5:44:27](https://www.youtube.com/watch?v=mpALXah_PBg&t=20667s) [C10 5:49:19](https://www.youtube.com/watch?v=mpALXah_PBg&t=20959s) [C10 5:57:32](https://www.youtube.com/watch?v=mpALXah_PBg&t=21452s)
- **Onboarding inputs:** paragraphs about you, your offer and your customers (dictate them); 1 or 2 verbatim writing samples per channel for voice; 2 or 3 priorities for the next 90 days. Refresh priorities from the source system each quarter. [OS2 29:46](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=1786s)
- **LLM wiki** (after Karpathy's idea): `raw/` sources and `wiki/` pages written by the LLM, plus `index.md`, `log.md` and a CLAUDE.md schema. Point other projects at it ("read hot.md, then the index; don't read the wiki unless you need it"), and lint it periodically. A wiki works without a vector database until you're at very large scale. [OS2 2:04:17](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=7457s) [OS2 2:18:35](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=8315s)
- **Five levels of second brain:** CLAUDE.md plus folders; an LLM wiki; semantic search; a knowledge graph; an always-on synced brain. Pick the lowest level that fixes a real pain, and design storage from how you'll query it. Keep summaries and aggregations as full markdown rather than chunks. [NC6 3:52:11](https://www.youtube.com/watch?v=jdbOVepEtUE&t=13931s)
- **Ingest evergreen context** (decisions, quarterly goals, meeting outcomes). Leave fast-changing data (Slack, email, CRM) at its source, and teach Claude where to look and in what order. The biggest gap is usually getting knowledge out of your head; grill-me sessions help. [NC6 4:13:15](https://www.youtube.com/watch?v=jdbOVepEtUE&t=15195s)
- **RAG:** Claude can build a multimodal embedding pipeline and chat app from plain language. Quality depends on descriptions and metadata. Ask it how the system "thinks" when results are off. [C10 3:17:50](https://www.youtube.com/watch?v=mpALXah_PBg&t=11870s) [C10 3:29:57](https://www.youtube.com/watch?v=mpALXah_PBg&t=12597s)
- **Daily loop:** plan the day each morning; at the end of the day, note missing context, corrections and copy-pastes, then patch them. Audit weekly. Move deterministic steps into scripts. [OS2 2:26:58](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=8818s)
- **Dashboards:** prove the idea with a live artifact first, and build a custom dashboard only if you check it constantly. [OS2 2:23:27](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=8607s)

## 16. Delivering client projects

- **Sell outcomes (time, money, focus), not agents.** The sequence is diagnose, solve, value, price. For example: 5 hours a week of onboarding, 80% automated, is about $10K a year saved, priced at $3K. [C10 8:25:16](https://www.youtube.com/watch?v=mpALXah_PBg&t=30316s) [C10 8:28:48](https://www.youtube.com/watch?v=mpALXah_PBg&t=30528s)
- **The PRICE framework:**
  - **P**repare: think in value, not hours.
  - **R**esearch: map the manual process (trigger, who does it, time, tools, cost).
  - **I**dentify the ROI: aim for about 10x in year one.
  - **C**ommunicate: what's included, how QA works, what you need from the client.
  - **E**xpand: maintenance, optimization, V2.

  Track and report impact metrics after go-live. [C10 9:30:56](https://www.youtube.com/watch?v=mpALXah_PBg&t=34256s) [C10 9:34:32](https://www.youtube.com/watch?v=mpALXah_PBg&t=34472s)
- **Ownership:** decide whose GitHub, hosting account and domain the solution lives under. The client should own and pay for hosting and API keys. If keys must be shared, use a one-time encrypted link, never chat or email. [C10 9:35:45](https://www.youtube.com/watch?v=mpALXah_PBg&t=34545s) [C10 9:44:02](https://www.youtube.com/watch?v=mpALXah_PBg&t=35042s)
- **QA before handover:**
  - Get real (anonymized) sample data before signing.
  - Agree success criteria and a "must never happen" list.
  - Test bad, empty and duplicate inputs.
  - Log the input, intermediate steps and output for each run.
  - Check AI output for correctness, tone and safety, and consistency.

  [C10 9:46:19](https://www.youtube.com/watch?v=mpALXah_PBg&t=35179s) [C10 9:48:33](https://www.youtube.com/watch?v=mpALXah_PBg&t=35313s)
- **Handover:** keep separate test and production copies, with automated backups, clear naming and notes, no embedded secrets, a Loom walkthrough and documentation. **Contract:** scope and definition of done, a separate maintenance retainer, simple SLAs, IP terms, and an exit process. New asks go to a V2 backlog. [C10 9:50:53](https://www.youtube.com/watch?v=mpALXah_PBg&t=35453s) [C10 9:53:18](https://www.youtube.com/watch?v=mpALXah_PBg&t=35598s) [C10 9:55:46](https://www.youtube.com/watch?v=mpALXah_PBg&t=35746s)

## 17. Applying this to Azure and Databricks work

*These are my suggestions for mapping the video practices onto Azure and Databricks projects. They aren't from the videos.*

- **CLI over MCP:** have Claude use `az` and the `databricks` CLI, and save the exact commands you rely on to `references/azure-cli.md` and `references/databricks-cli.md` so it doesn't re-research them.
- **Scoped access:** one service principal per automation with least-privilege RBAC (for example Reader for cost analysis). In Unity Catalog, grant only the catalogs and schemas the job needs. In production, secrets go in Key Vault or Databricks secret scopes, not `.env`.
- **Deny destructive commands** in `.claude/settings.json`, then test the rules. Check the current permission-rule syntax in the Claude Code docs.

  ```json
  {
    "permissions": {
      "deny": [
        "Read(./.env)",
        "Bash(az group delete:*)",
        "Bash(az resource delete:*)",
        "Bash(databricks fs rm:*)"
      ]
    }
  }
  ```

- **Verify before applying:** ask for `az deployment group what-if` or `terraform plan` output, run SQL against a sample before running it fully, and get the definition of done in writing (for example "cluster policy applied to all jobs; list the job IDs changed").
- **Skill candidates:**
  - Cost-optimization review over `system.billing.usage`.
  - Ticket triage that drafts a reply.
  - HMS to Unity Catalog migration checklist.
  - Weekly idle-resource report.

  Encode your steps, the decisions you make, and the guardrails.
- **Deterministic jobs as code:** recurring cost reports and cleanups belong in Databricks Jobs, Azure Functions or Automation runbooks. Claude writes and tests them; don't leave an agent running them.

## 18. Commands and shortcuts

Availability varies by version and surface (terminal, desktop or IDE). Run `/help` to see what you have.

| Command / key | What it does |
|---|---|
| `/init` | Scan the project and generate CLAUDE.md |
| `/clear` | Wipe the conversation (CLAUDE.md and files remain) |
| `/compact [what to keep]` | Summarize history, keeping what you name |
| `/context` | Show what's using the context window |
| `/cost` | Token usage and cost |
| `/statusline` | Configure the status line (model, context %, cost) |
| `/model` | Switch model |
| `/rewind` | Roll back to an earlier point |
| `/resume` | Reopen a past session |
| `/memory` | Edit or toggle auto memory |
| `/agents` | Create and manage sub-agents (terminal) |
| `/mcp` | Manage MCP servers |
| `/permissions`, `/config` | Permissions and settings |
| `/plugin` | Install plugins such as skill-creator (shown as `/plugins` in C10) |
| `/doctor`, `/status` | Diagnostics and version info |
| `/loop` | Recurring prompt in this session |
| `/schedule` | Scheduled task (desktop app) |
| `/remote-control` | Continue a local session from the phone app |
| `/btw` | Side question without polluting context |
| `/goal` | Keep working until a completion condition is met (as shown in NC6) |
| `ultrathink` | Maximum thinking budget for hard problems |
| `@file` | Reference a specific file |
| Shift+Tab | Cycle permission modes |
| Esc | Interrupt and redirect |
| Ctrl+B / Ctrl+O | Background a running agent / expand its output |
| `claude --worktree <name>` | Session in an isolated git worktree |
| `claude --agent <name>` | Start a session as a specific agent |

## 19. Prompt templates

**Plan a new build (plan mode)**
```text
I want to build <outcome> for <who>. Inputs: <data/sources>. Output: <deliverable and format>.
Look into which APIs, CLIs or MCP servers fit, and whether any skills would help.
Ask me questions one at a time until you're 95% confident, and tell me what I haven't thought of.
```

**Turn an idea into a PRD**
```text
Here's a rough idea: <idea>. Help me turn this into a solid PRD: goal, success criteria,
how we'll verify it, files/integrations involved, edge cases, and what "done" means.
```

**Definition of done**
```text
Done means: <exact output, count, format, location>. Prove it by <test/screenshot/sample run>.
Once that's true, stop and report what you ran and why you're confident.
```

**Grill me (Matt Pocock's original)**
```text
Interview me relentlessly about every aspect of this plan until we reach a shared understanding.
Walk down each branch of the design tree, resolving dependencies between decisions one by one.
For each question, provide your recommended answer. Ask questions one at a time.
If a question can be answered by exploring the codebase, explore the codebase instead.
```

**Turn what we just did into a skill**
```text
Look back at the steps we just did. This is something I do <frequency>. Turn it into a skill
with a clear name and a description that says when to use it. Ask me questions so you have
everything you need, and put any reference material in the skill's references folder.
```

**Create a new skill**
```text
Create a skill called <name>. It <does what> when I <trigger>. Inputs: <...>. Output: <...>.
Rules: <guardrails, e.g., always let me review before anything is published>.
Ask me clarifying questions one at a time until you're 95% confident.
```

**After a run: improve the skill**
```text
Here's what I liked: <...>. Here's what I didn't: <...>. Update the SKILL.md (and a known-issues
section) so the next run gets this right without me repeating it.
```

**Correction that sticks**
```text
I don't like <specific problem>. Fix it, then update CLAUDE.md (or the <name> skill) so you
don't do this again.
```

**Save research so it isn't repeated**
```text
Save what you just learned about <tool/API> (endpoint, auth, gotchas) to references/<tool>.md
and add a one-line pointer in CLAUDE.md. Don't research this again next session.
```

**Connect an API safely**
```text
I want to connect you to <tool> via its API (more token efficient than MCP). Research its
API docs, write references/<tool>-api.md with the endpoints we need, and create a .env with a
placeholder. I'll paste the key myself. Then make a test request to confirm it works.
```

**Security review before publishing**
```text
Do a full security review of this project before we push/deploy: exposed keys or tokens,
secrets in code or git history, unprotected webhooks, overly broad permissions, and what an
outsider could do once this is live. List findings by severity with fixes.
```

**Safe failures**
```text
I'm concerned about what could go wrong. Help me find the edge cases (bad, empty, duplicate,
unexpected input; API down; cost runaway) and make sure every failure is a safe failure:
notify me, stop cleanly, never send anything external, and log what happened.
```

**Lock down permissions**
```text
Here are things I never want to happen: <deleting files, force-pushing, dropping tables, ...>.
Update the project settings so you physically cannot do them, then test each rule.
```

**Delegate to sub-agents**
```text
Use sub-agents for this: one researches <A>, one researches <B>, in parallel, on a cheaper
model. Return only the key findings, then synthesize them here.
```

**Agent team**
```text
Goal: <end result and how I'll check it>.
Create an agent team using the team create function: <N> teammates using <model>.
1) <role>: owns <files>, produces <deliverable>, messages <teammate> when done.
2) <role>: ...
3) QA: tests <...>, sends failures back to the owner, approves when all pass.
Final deliverables: <running app / report / doc of decisions and how to run it>.
```

**Session handoff (before /clear)**
```text
Write a handoff doc: where we started, decisions locked, what shipped, key files, current
state, how it was verified, deferred items, open questions, and "pick up here".
```

**Applied learning rule (add to CLAUDE.md)**
```text
When something fails repeatedly or a workaround is found, add a one-line bullet under
"Applied learning" in CLAUDE.md (under 15 words, no explanation).
```

## 20. Time-sensitive claims to re-check

These were accurate for the videos at the time of recording but change often. Check current docs before relying on them:
- Model names and versions (Opus 4.x, Sonnet 4.x and 5, Fable), prices per token, and which model is the default.
- Plan limits (5-hour and weekly limits, routine runs per day, Claude Design quota), peak-hour effects, and prompt-cache lifetimes.
- Context thresholds (the "dumb zone" figures, the 200K versus 1M windows, starting overhead).
- Experimental or new features: agent teams (env var name), `/goal`, dynamic workflows, `/voice`, desktop-only scheduled tasks, `ultrathink` budget, remote control.
- Third-party tools: Google Workspace CLI (pre-1.0), Pixel Agents (Windows-only at the time), Context7, Playwright CLI, Modal and Trigger.dev free tiers.

## Appendix: chapter index

Chapter lists from each video's description, linked to the start of each chapter.

### C10: Build & Sell with Claude Code (10+ Hour Course)

- [0:00](https://www.youtube.com/watch?v=mpALXah_PBg&t=0s) Course Outline
- [1:14](https://www.youtube.com/watch?v=mpALXah_PBg&t=74s) Why Learn This
- [26:08](https://www.youtube.com/watch?v=mpALXah_PBg&t=1568s) Getting Set Up
- [41:25](https://www.youtube.com/watch?v=mpALXah_PBg&t=2485s) Operations
- [50:53](https://www.youtube.com/watch?v=mpALXah_PBg&t=3053s) Tokens and Context Windows
- [55:10](https://www.youtube.com/watch?v=mpALXah_PBg&t=3310s) Claude.md
- [58:57](https://www.youtube.com/watch?v=mpALXah_PBg&t=3537s) Building Your First Workflow
- [1:25:05](https://www.youtube.com/watch?v=mpALXah_PBg&t=5105s) Building Second Workflow
- [1:50:43](https://www.youtube.com/watch?v=mpALXah_PBg&t=6643s) Deploying Automations
- [3:05:46](https://www.youtube.com/watch?v=mpALXah_PBg&t=11146s) Project Architecture & Commands
- [3:17:39](https://www.youtube.com/watch?v=mpALXah_PBg&t=11859s) RAG
- [3:32:59](https://www.youtube.com/watch?v=mpALXah_PBg&t=12779s) Turning n8n Workflow into App
- [4:12:42](https://www.youtube.com/watch?v=mpALXah_PBg&t=15162s) Website Building Hacks
- [4:40:07](https://www.youtube.com/watch?v=mpALXah_PBg&t=16807s) 3D Animated Websites
- [5:00:02](https://www.youtube.com/watch?v=mpALXah_PBg&t=18002s) APIs and MCPs
- [5:28:16](https://www.youtube.com/watch?v=mpALXah_PBg&t=19696s) Google CLI
- [5:39:42](https://www.youtube.com/watch?v=mpALXah_PBg&t=20382s) Building Your Own Executive Assistant
- [6:08:03](https://www.youtube.com/watch?v=mpALXah_PBg&t=22083s) Skills
- [6:51:30](https://www.youtube.com/watch?v=mpALXah_PBg&t=24690s) Sub-agents
- [7:11:20](https://www.youtube.com/watch?v=mpALXah_PBg&t=25880s) Agent Teams
- [7:27:30](https://www.youtube.com/watch?v=mpALXah_PBg&t=26850s) Browser Automation
- [7:42:30](https://www.youtube.com/watch?v=mpALXah_PBg&t=27750s) Permissions & Context Management
- [7:50:09](https://www.youtube.com/watch?v=mpALXah_PBg&t=28209s) GitHub & Worktrees
- [7:56:45](https://www.youtube.com/watch?v=mpALXah_PBg&t=28605s) Fun Hacks
- [8:25:06](https://www.youtube.com/watch?v=mpALXah_PBg&t=30306s) The Selling AI Mindset
- [8:39:41](https://www.youtube.com/watch?v=mpALXah_PBg&t=31181s) Finding Clients
- [8:54:01](https://www.youtube.com/watch?v=mpALXah_PBg&t=32041s) First Client in 7 Days
- [9:14:56](https://www.youtube.com/watch?v=mpALXah_PBg&t=33296s) Pricing AI Workflows
- [9:35:36](https://www.youtube.com/watch?v=mpALXah_PBg&t=34536s) Delivering AI Projects
- [9:58:55](https://www.youtube.com/watch?v=mpALXah_PBg&t=35935s) Thank You! Join AIS FREE

### NC6: Claude Code for Non-Coders (6 Hour Course)

- [0:00](https://www.youtube.com/watch?v=jdbOVepEtUE&t=0s) Intro: From Beginner to AI Native
- [1:00](https://www.youtube.com/watch?v=jdbOVepEtUE&t=60s) What Is Claude Code (Chat, Cowork, Code)
- [5:04](https://www.youtube.com/watch?v=jdbOVepEtUE&t=304s) Models vs Context (The Core Analogy)
- [6:48](https://www.youtube.com/watch?v=jdbOVepEtUE&t=408s) The 12 Mindset Shifts
- [14:52](https://www.youtube.com/watch?v=jdbOVepEtUE&t=892s) Prompt Engineering vs Context Engineering
- [17:33](https://www.youtube.com/watch?v=jdbOVepEtUE&t=1053s) Taste, Iteration & Building Your Jarvis
- [24:20](https://www.youtube.com/watch?v=jdbOVepEtUE&t=1460s) One Passion, Many Branches
- [31:44](https://www.youtube.com/watch?v=jdbOVepEtUE&t=1904s) Installing Claude Code & Your First Prompts
- [34:09](https://www.youtube.com/watch?v=jdbOVepEtUE&t=2049s) Working With Local Files (Excel, HTML)
- [38:18](https://www.youtube.com/watch?v=jdbOVepEtUE&t=2298s) Prompt Engineering & Verifying the Output
- [43:25](https://www.youtube.com/watch?v=jdbOVepEtUE&t=2605s) Tokens & Choosing Your Model
- [48:10](https://www.youtube.com/watch?v=jdbOVepEtUE&t=2890s) Setting Up a Project (claude.md & settings.json)
- [1:00:06](https://www.youtube.com/watch?v=jdbOVepEtUE&t=3606s) Connecting Tools: API Keys & .env
- [1:09:59](https://www.youtube.com/watch?v=jdbOVepEtUE&t=4199s) Permission Modes, Scoped Keys & Privacy
- [1:20:31](https://www.youtube.com/watch?v=jdbOVepEtUE&t=4831s) Building Your AI Operating System
- [1:25:08](https://www.youtube.com/watch?v=jdbOVepEtUE&t=5108s) Connecting Google Workspace: CLIs vs MCPs
- [1:40:28](https://www.youtube.com/watch?v=jdbOVepEtUE&t=6028s) Skills Deep Dive
- [1:56:13](https://www.youtube.com/watch?v=jdbOVepEtUE&t=6973s) The Context Window & Session Handoff
- [2:03:17](https://www.youtube.com/watch?v=jdbOVepEtUE&t=7397s) Memory & Your Second Brain
- [2:11:35](https://www.youtube.com/watch?v=jdbOVepEtUE&t=7895s) Constraints, Metrics & Mapping Your Process
- [2:20:23](https://www.youtube.com/watch?v=jdbOVepEtUE&t=8423s) Sub-Agents Explained
- [2:31:41](https://www.youtube.com/watch?v=jdbOVepEtUE&t=9101s) Building a Sub-Agent: The Plan Roaster
- [2:43:46](https://www.youtube.com/watch?v=jdbOVepEtUE&t=9826s) When to Use Sub-Agents
- [2:47:27](https://www.youtube.com/watch?v=jdbOVepEtUE&t=10047s) Installing in the Terminal + Free Resources
- [2:53:11](https://www.youtube.com/watch?v=jdbOVepEtUE&t=10391s) Building & Cloning Websites
- [3:10:54](https://www.youtube.com/watch?v=jdbOVepEtUE&t=11454s) Deploying With GitHub & Vercel
- [3:18:58](https://www.youtube.com/watch?v=jdbOVepEtUE&t=11938s) The AI Systems Pyramid & Trusting the Output
- [3:36:15](https://www.youtube.com/watch?v=jdbOVepEtUE&t=12975s) Building a Second Brain
- [3:56:28](https://www.youtube.com/watch?v=jdbOVepEtUE&t=14188s) The 5 Levels of a Second Brain
- [4:13:43](https://www.youtube.com/watch?v=jdbOVepEtUE&t=15223s) Knowledge Graphs & the Grill-Me Skill
- [4:31:50](https://www.youtube.com/watch?v=jdbOVepEtUE&t=16310s) Sub-Agents vs Agent Teams
- [4:45:35](https://www.youtube.com/watch?v=jdbOVepEtUE&t=17135s) Scheduled Automations & Cloud Routines
- [5:03:03](https://www.youtube.com/watch?v=jdbOVepEtUE&t=18183s) Building a Research Automation
- [5:27:13](https://www.youtube.com/watch?v=jdbOVepEtUE&t=19633s) Token Management & Prompt Caching
- [5:58:20](https://www.youtube.com/watch?v=jdbOVepEtUE&t=21500s) Final Thoughts

### OS2: Build & Sell Claude Code Operating Systems (2+ Hour Course)

- [0:00](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=0s) Intro
- [3:30](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=210s) The Three Ms of AI
- [11:30](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=690s) The Four Cs of an AIOS
- [15:00](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=900s) Mapping Your Tools
- [20:30](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=1230s) Cloning the Repo & VS Code Setup
- [29:00](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=1740s) The Onboarding Skill
- [36:30](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=2190s) Connecting ClickUp
- [47:30](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=2850s) Audit & Level Up Skills
- [51:30](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=3090s) Google Workspace CLI
- [1:06:00](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=3960s) Capabilities & Building Skills
- [1:25:30](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=5130s) Live Skill Build
- [1:35:30](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=5730s) Cadence & Cloud Routines
- [1:56:30](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=6990s) Loop & Reminders
- [2:05:00](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=7500s) Karpathy's LLM Wiki
- [2:23:30](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=8610s) Dashboards with Artifacts
- [2:27:30](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=8850s) Daily Loop & Success Criteria
- [2:32:00](https://www.youtube.com/watch?v=bCljOfCH8Ms&t=9120s) Final Thoughts

### DM2: Claude Design 2 HOUR COURSE (Beginner to Pro)

- [0:00](https://www.youtube.com/watch?v=ovabeVoWrA0&t=0s) What Is Claude Design
- [5:24](https://www.youtube.com/watch?v=ovabeVoWrA0&t=324s) Why Design Systems Matter
- [8:55](https://www.youtube.com/watch?v=ovabeVoWrA0&t=535s) Ideating the Tally Brand
- [11:33](https://www.youtube.com/watch?v=ovabeVoWrA0&t=693s) Creating the Design System
- [19:50](https://www.youtube.com/watch?v=ovabeVoWrA0&t=1190s) Pitch Deck Build
- [34:01](https://www.youtube.com/watch?v=ovabeVoWrA0&t=2041s) Landing Page Wireframes
- [40:45](https://www.youtube.com/watch?v=ovabeVoWrA0&t=2445s) High-Fidelity Website Build
- [57:51](https://www.youtube.com/watch?v=ovabeVoWrA0&t=3471s) Mobile App Prototype
- [1:09:00](https://www.youtube.com/watch?v=ovabeVoWrA0&t=4140s) Launch Video with HyperFrames
- [1:22:05](https://www.youtube.com/watch?v=ovabeVoWrA0&t=4925s) Final Live Build
- [1:42:01](https://www.youtube.com/watch?v=ovabeVoWrA0&t=6121s) GitHub & Vercel Deploy
- [1:49:26](https://www.youtube.com/watch?v=ovabeVoWrA0&t=6566s) Stretching Your Session Limit
- [1:57:00](https://www.youtube.com/watch?v=ovabeVoWrA0&t=7020s) Final Thoughts

### D3D: Claude Design Builds Beautiful 3D Websites Instantly (full tutorial)

- [0:00](https://www.youtube.com/watch?v=TcFeSjwTo7g&t=0s) What We're Building
- [1:41](https://www.youtube.com/watch?v=TcFeSjwTo7g&t=101s) Planning the Brand
- [4:13](https://www.youtube.com/watch?v=TcFeSjwTo7g&t=253s) Live Build in Claude Design
- [8:15](https://www.youtube.com/watch?v=TcFeSjwTo7g&t=495s) Inspiration from Motions.ai
- [10:24](https://www.youtube.com/watch?v=TcFeSjwTo7g&t=624s) Tweaks & Iteration
- [14:06](https://www.youtube.com/watch?v=TcFeSjwTo7g&t=846s) Grab my FREE Skills
- [14:48](https://www.youtube.com/watch?v=TcFeSjwTo7g&t=888s) Back to the Build
- [19:23](https://www.youtube.com/watch?v=TcFeSjwTo7g&t=1163s) Deploying with GitHub & Vercell
- [25:44](https://www.youtube.com/watch?v=TcFeSjwTo7g&t=1544s) Mobile Optimization
- [27:04](https://www.youtube.com/watch?v=TcFeSjwTo7g&t=1624s) Stretching Your Limits

### H60: How to Use Claude Code Better Than 98% of People

- [0:00](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=0s) Intro
- [5:46](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=346s) Sponsorship
- [7:41](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=461s) Stop Vibe Coding, Start Directing
- [13:17](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=797s) Make the Agent Prove Its Work
- [19:46](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=1186s) Why You Plan More Than You Build
- [27:01](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=1621s) The Dumb Zone
- [33:38](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=2018s) Harness Engineering and the Ralph Loop
- [44:23](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=2663s) The Security Problem Nobody Plans For
- [51:22](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=3082s) Every Bug Is a Permanent Upgrade
- [59:54](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=3594s) Top 3 Claude Code Features
- [1:07:56](https://www.youtube.com/watch?v=RzLV8sfFdMM&t=4076s) Outro
