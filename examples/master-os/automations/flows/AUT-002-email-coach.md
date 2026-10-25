# AUT-002 Email coach (org-contoso)

Compares each draft from AUT-001 with what I actually sent, and proposes changes to my voice rules.

```mermaid
flowchart LR
  T([Schedule<br/>daily 18:00, Mon-Fri]) --> A[(data/email-log/<br/>drafts.jsonl)]
  T --> B[Fetch today's<br/>Sent Items]
  A --> M[Match draft to sent<br/>by conversation id]
  B --> M
  M --> C[email-coach skill<br/>score and find patterns]
  C --> R[(coach-YYYY-MM-DD.md)]
  C --> P[Proposed voice.md diff]
  P -.->|I approve| V[(context/voice.md)]
```

## Run command

```bash
cd ~/master-os/brands/org-contoso && claude -p "/email-coach brand=org-contoso" \
  --add-dir ../../context \
  --permission-mode dontAsk --permission-prompts none \
  --allowedTools "Edit(./data/email-log/**),<outlook read tools>"
```

`context/voice.md` isn't in the edit list, so the coach can only propose changes. Applying them is my call.
