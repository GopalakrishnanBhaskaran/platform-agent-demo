# Decision log

Append-only. One row per decision that changes how the OS works. Project decisions stay in the project's README.

| Date | Decision | Why | Revisit when |
|---|---|---|---|
| 2026-10-18 | Brand-only skills nest inside the brand | The Contoso setup must be able to hand over intact | A second brand needs the skill |
| 2026-10-18 | Client work stays outside the OS; `clients/` holds pointers only | The OS syncs to my personal GitHub, and client files are confidential | Never |
| 2026-10-20 | Brand automations start in the brand folder in `dontAsk` mode | Headless runs can't read outside their working directory, so the folder is the silo | Claude Code adds per-folder settings |
| 2026-10-25 | Connections get their own registry | Connectors aren't scoped by folder, and I can't guard what isn't listed | Never |
