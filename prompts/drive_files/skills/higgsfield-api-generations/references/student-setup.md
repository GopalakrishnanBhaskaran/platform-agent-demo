# Student setup

## What students need

1. A Higgsfield API account at <https://console.higgsfield.ai>.
2. A funded API dollar balance. A normal higgsfield.ai subscription does not fund the API.
3. An API credential copied at creation time. It contains a key ID and secret separated by a colon.
4. Python 3.9 or newer. The bundled helper uses only the Python standard library.

## Install the skill

Copy the entire `higgsfield-api-generations` folder into one of these locations:

- Codex project: `.agents/skills/higgsfield-api-generations/`
- Claude Code project: `.claude/skills/higgsfield-api-generations/`
- Personal Codex install: `%USERPROFILE%\.codex\skills\higgsfield-api-generations\` on Windows

Keep the folder intact because `SKILL.md` links to `references/`, `examples/`, and `scripts/` with relative paths.

## Add the credential

Create or edit `.env` in the project root:

```env
# Higgsfield API key. Create it at https://console.higgsfield.ai
HIGGSFIELD_API_KEY=YOUR_KEY_ID:YOUR_KEY_SECRET
```

Rules:

- Keep `.env` out of git.
- Never paste the key into chat, source code, screenshots, or frontend JavaScript.
- Rotate it in Higgsfield Console if it may have been exposed.
- The helper also accepts `HF_KEY` or `HF_CREDENTIALS` for compatibility with official SDK examples.

## Verify without spending

From the project root, run the copy that matches the install location:

```bash
python .agents/skills/higgsfield-api-generations/scripts/higgsfield_api.py models
```

Then run a cost-only preflight:

```bash
python .agents/skills/higgsfield-api-generations/scripts/higgsfield_api.py generate video --prompt "A paper airplane crossing a sunlit studio"
```

The helper will not submit until `--yes` is present.

## First generation

```bash
python .agents/skills/higgsfield-api-generations/scripts/higgsfield_api.py generate video --prompt "A paper airplane crossing a sunlit studio" --yes
```

Outputs and `run.json` are saved under:

```text
projects/higgsfield-api-generations/outputs/
```

## Suggested student prompts

- “Use Higgsfield API Generations to list the video models I can access.”
- “Estimate a five-second 16:9 video of a robot learning pottery.”
- “Generate that video with the default model.”
- “Create a product image with Recraft and tell me the exact API cost.”
- “Resume this Higgsfield request from the run.json file.”

