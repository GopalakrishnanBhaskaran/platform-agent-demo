# Set Up Fugu Ultra in Claude Code

**For the student (human):** Put this file and a `.env` file in a folder. The `.env` must contain one line:

```
SAKANA_API_KEY=your_sakana_key_here
```

Then open Claude Code in that folder and paste this message:

> My Sakana API key is in the `.env` file. Follow `setup-fugu-ultra-in-claude-code.md` step by step to get Fugu Ultra running inside Claude Code, and tell me when it works.

Your Claude Code agent will do everything below. It takes about 5 minutes.

---

## FOR THE AGENT: read this whole file, then execute the steps in order.

### What you are doing and why

Claude Code speaks the **Anthropic** API format. Sakana Fugu only speaks the **OpenAI** format, so Claude Code cannot talk to it directly (a direct connection returns `404`). You will install a tiny local translator called **`claude-code-router`** (command: `ccr`) that converts between the two formats, then point Claude Code at it.

```
Claude Code  ->  ccr  (http://127.0.0.1:8080, Anthropic format)  ->  api.sakana.ai/v1  (OpenAI format)
```

End state: running `claude` in this folder sends every request to **Fugu Ultra**.

**Rules while you work:**
- Do the steps in order. If a step fails, stop and tell the user exactly what failed. Do not skip ahead.
- The real Sakana key goes in ONE place only: the ccr config file (Step 4). Never write it into the project's `settings.local.json`.
- Do not print the full API key back to the user.
- Detect the operating system and use the matching command block (PowerShell for Windows, bash for macOS/Linux).

---

### Step 0 — Check prerequisites

Run these. All three must succeed.

```bash
node --version      # need v18 or newer
npm --version
claude --version    # the Claude Code CLI
```

- If `node` or `npm` is missing: tell the user to install Node.js (https://nodejs.org) and stop.
- If `claude` is missing: tell the user to install Claude Code and stop.

---

### Step 1 — Read the API key from .env

Read `SAKANA_API_KEY` from the `.env` file in this folder. Hold it for Step 4. (Confirm it is non-empty; do not echo the whole value.)

**bash (macOS/Linux):**
```bash
set -a; . ./.env; set +a
echo "key length: ${#SAKANA_API_KEY}"   # sanity check, not the key itself
```

**PowerShell (Windows):**
```powershell
$key = ((Get-Content .env | Select-String '^SAKANA_API_KEY=') -replace '^SAKANA_API_KEY=','').Trim().Trim('"').Trim("'")
"key length: $($key.Length)"
```

If the key is empty or the file is missing, stop and tell the user to add `SAKANA_API_KEY=...` to `.env`. Write the key with no surrounding quotes: `SAKANA_API_KEY=fish_...`, not `SAKANA_API_KEY="fish_..."`.

> **Important for the agent:** shell variables do NOT persist between separate commands (each command you run is a fresh shell). So `$SAKANA_API_KEY` / `$key` set here will be empty in the next command. The smoke test in Step 2 therefore re-loads the key inside the same command. Follow that pattern any time you need the key.

---

### Step 2 — Confirm the key actually works (smoke test)

Call Sakana directly, before building anything. Expect HTTP `200` and a short reply.

**bash:** (re-loads the key in this same command, since variables do not carry over)
```bash
set -a; . ./.env; set +a
curl -sS -w "\nHTTP:%{http_code}\n" -X POST https://api.sakana.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SAKANA_API_KEY" \
  -d '{"model":"fugu","messages":[{"role":"user","content":"reply with: OK"}]}'
```

**PowerShell:** (re-loads the key in this same command)
```powershell
$key = ((Get-Content .env | Select-String '^SAKANA_API_KEY=') -replace '^SAKANA_API_KEY=','').Trim().Trim('"').Trim("'")
$body = '{"model":"fugu","messages":[{"role":"user","content":"reply with: OK"}]}'
curl.exe -sS -w "`nHTTP:%{http_code}`n" -X POST https://api.sakana.ai/v1/chat/completions `
  -H "Content-Type: application/json" -H "Authorization: Bearer $key" -d $body
```

- `200` with a reply: the key is good, continue.
- `401` or `403`: the key is wrong or inactive. Stop and tell the user.
- `422` (Validation Error): almost always a malformed JSON body, usually from shell quote-mangling, not a key problem. Re-check the `-d` payload is exactly the JSON above (on Windows, prefer the PowerShell block as written). The key itself is fine if Step 1 showed a length around 69.

---

### Step 3 — Install the translator

Same command on every OS:

```bash
npm install -g @musistudio/claude-code-router
```

Confirm it installed: `ccr version` (or `ccr -v`) should print a version. If `ccr` is "command not found", the npm global bin folder is not on PATH; tell the user, or call it by its full path under the npm global directory.

---

### Step 4 — Write the translator config (this holds the real key)

Create this file:

- macOS/Linux: `~/.claude-code-router/config.json`
- Windows: `C:\Users\<your-username>\.claude-code-router\config.json`

Use this exact content, but replace `PASTE_REAL_SAKANA_KEY` with the actual value from Step 1:

```json
{
  "APIKEY": "sakana-fugu-proxy",
  "HOST": "127.0.0.1",
  "PORT": 8080,
  "API_TIMEOUT_MS": 600000,
  "Providers": [
    {
      "name": "sakana",
      "api_base_url": "https://api.sakana.ai/v1/chat/completions",
      "api_key": "PASTE_REAL_SAKANA_KEY",
      "models": ["fugu", "fugu-ultra"]
    }
  ],
  "Router": {
    "default": "sakana,fugu-ultra",
    "background": "sakana,fugu",
    "think": "sakana,fugu-ultra",
    "longContext": "sakana,fugu-ultra",
    "webSearch": "sakana,fugu"
  }
}
```

Notes:
- `APIKEY` is a **local password for the proxy** that you invent. It is NOT the Sakana key. It must match `ANTHROPIC_AUTH_TOKEN` in Step 6. Leave it as `sakana-fugu-proxy` unless you have a reason to change both.
- `Router.default` decides which model handles normal requests. `fugu-ultra` = max quality. Change `default` to `"sakana,fugu"` later if the user wants faster, cheaper responses.

Create the folder first if needed:

**PowerShell:** `New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude-code-router" | Out-Null`
**bash:** `mkdir -p ~/.claude-code-router`

---

### Step 5 — Start the translator

```bash
ccr restart      # use restart so it picks up the new config; ccr start also works the first time
ccr status       # must show: Running, on port 8080
```

If status is not "Running", run `ccr start` and check again. Do not continue until it is running.

---

### Step 6 — Point this project at the translator

Create `.claude/settings.local.json` in THIS project folder with exactly this content (no real key here, only the local proxy password):

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:8080",
    "ANTHROPIC_AUTH_TOKEN": "sakana-fugu-proxy",
    "ANTHROPIC_API_KEY": "",
    "API_TIMEOUT_MS": "3000000",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "fugu-ultra",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "fugu-ultra",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "fugu-ultra",
    "ANTHROPIC_SMALL_FAST_MODEL": "fugu-ultra",
    "CLAUDE_CODE_SUBAGENT_MODEL": "fugu-ultra"
  }
}
```

`ANTHROPIC_AUTH_TOKEN` here must equal `APIKEY` in the ccr config. If you changed one, change both.

---

### Step 7 — Final verification, inside Claude Code

Prove a real Claude Code request reaches Fugu Ultra. Run from this folder:

```bash
claude -p "In one sentence, what is the capital of Japan?" --output-format json
```

In the JSON result, check:
- `is_error` is `false`
- `result` is a correct answer (mentions Tokyo)
- the model field **contains `fugu-ultra`** (it normally appears as `fugu-ultra[1m]`, the 1M-context variant; treat that as a match, not a mismatch)

(`total_cost_usd` will show `0` because Claude Code has no price list for Fugu. That is expected, not an error. A harmless `no stdin data received in 3s` warning may also print before the JSON; ignore it.)

A quicker plain-text check also works:
```bash
claude -p "reply with exactly: FUGU_OK"
```

If this returns a sensible answer, the setup is complete.

---

### Step 8 — Report to the user

Tell them, briefly:
- ✅ Fugu Ultra is now running inside Claude Code, verified (`model: fugu-ultra`).
- **To use it daily:** make sure the translator is running (`ccr start`), then open Claude Code in this folder and use it normally.
- Cost shows `$0` in Claude Code; track real spend on the Sakana console.

---

## Troubleshooting (read if a step fails)

| Symptom | Cause | Fix |
|---|---|---|
| `404 Not Found` when Claude Code runs | `ANTHROPIC_BASE_URL` points at Sakana directly, not the proxy | It must be `http://127.0.0.1:8080` (the translator), per Step 6 |
| Connection refused / cannot reach model | Translator is not running | `ccr start`, then `ccr status` shows Running |
| `401` / `invalid api key` from the proxy | `ANTHROPIC_AUTH_TOKEN` does not match the config's `APIKEY` | Make the two strings identical |
| `401` on the Step 2 smoke test | Wrong or inactive Sakana key | Re-copy the key from console.sakana.ai into `.env` |
| Empty reply / `stop_reason: max_tokens` on tiny test calls | Fugu Ultra spends tokens thinking before answering | Give it a real budget; Claude Code does this by default, so only tiny manual curl tests hit it |
| `ccr: command not found` | npm global bin not on PATH | Add npm's global bin to PATH, or run `ccr` by full path |

## How it fits together (one-look reference)

```
.env (your Sakana key)
   |
   v   read once, pasted into:
~/.claude-code-router/config.json   <- the translator's brain (real key + which models)
   |
   v   ccr start  ->  listens at http://127.0.0.1:8080  (speaks Anthropic, forwards OpenAI)
   |
project/.claude/settings.local.json  <- tells Claude Code to use the translator
   |
   v
claude   ->   Fugu Ultra
```

**Sources:** Sakana API docs (console.sakana.ai/get-started) · claude-code-router (github.com/musistudio/claude-code-router)
