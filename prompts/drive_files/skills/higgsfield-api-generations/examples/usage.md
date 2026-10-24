# Usage examples

Commands below assume a Claude Code project install. For Codex, replace `.claude/skills` with `.agents/skills`.

## List the live catalog

```bash
python .claude/skills/higgsfield-api-generations/scripts/higgsfield_api.py models
python .claude/skills/higgsfield-api-generations/scripts/higgsfield_api.py models --output video --operation text2video
```

## Estimate the default video without spending

```bash
python .claude/skills/higgsfield-api-generations/scripts/higgsfield_api.py generate video \
  --prompt "A tiny robot waters plants in a sunlit apartment"
```

Without `--yes`, the helper performs the estimate and stops.

## Generate the default Seedance 2.5 video

```bash
python .claude/skills/higgsfield-api-generations/scripts/higgsfield_api.py generate video \
  --prompt "A tiny robot waters plants in a sunlit apartment" \
  --duration 5 \
  --resolution 720p \
  --aspect-ratio 16:9 \
  --no-audio \
  --yes
```

## Generate with a different video model

```bash
python .claude/skills/higgsfield-api-generations/scripts/higgsfield_api.py generate video \
  --model wan/v2.7/text-to-video \
  --prompt "A slow tracking shot through a moonlit greenhouse" \
  --params-json '{"duration":5,"resolution":"720p","aspect_ratio":"16:9","prompt_extend":false}' \
  --yes
```

On PowerShell, place JSON in a file to avoid quoting problems:

```powershell
python .claude/skills/higgsfield-api-generations/scripts/higgsfield_api.py generate video `
  --model wan/v2.7/text-to-video `
  --prompt "A slow tracking shot through a moonlit greenhouse" `
  --params-file .\wan-settings.json `
  --yes
```

## Generate an image

```bash
python .claude/skills/higgsfield-api-generations/scripts/higgsfield_api.py generate image \
  --prompt "Editorial product photograph of a translucent blue coffee cup" \
  --yes
```

## Use a public input image

```bash
python .claude/skills/higgsfield-api-generations/scripts/higgsfield_api.py generate video \
  --prompt "A smooth cinematic push-in with natural cloth and hair movement" \
  --image-url "https://example.com/reference.jpg" \
  --yes
```

## Use a local input image

```bash
python .claude/skills/higgsfield-api-generations/scripts/higgsfield_api.py generate video \
  --prompt "A smooth cinematic push-in with natural cloth and hair movement" \
  --image-file "./reference.jpg" \
  --yes
```

For another media type, upload it first and put the returned `public_url` into a model-specific params file:

```bash
python .claude/skills/higgsfield-api-generations/scripts/higgsfield_api.py upload "./reference.mp4"
```

## Resume an interrupted generation

```bash
python .claude/skills/higgsfield-api-generations/scripts/higgsfield_api.py resume \
  projects/higgsfield-api-generations/outputs/20260917-120000-video/run.json
```

## Return format

The helper’s final JSON contains:

- `status`
- `request_id`
- `model`
- `payload`
- `estimate`
- `cost_report`
- `downloaded_files`
- `run_file`

The agent should turn this into a concise response with inline media, a clickable file path, and the cost basis.
