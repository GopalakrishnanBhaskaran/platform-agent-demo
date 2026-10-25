# AUT-006 LinkedIn draft from cost tips (personal)

Every Friday, it turns the top idea into a post draft. I edit and post by hand.

```mermaid
flowchart LR
  T([Claude Code scheduled task<br/>Fri 09:00]) --> I[(linkedin-content/<br/>ideas.md)]
  I --> P[linkedin-post skill<br/>write generic post]
  P --> D[(linkedin-content/drafts/<br/>YYYY-MM-DD-slug.md)]
  P --> U[Mark idea drafted]
  D -.->|I review and post| L([LinkedIn])
```

## Details

- **Reads:** `brands/personal/**` only. It has no connector and no org or client access.
- **Writes:** `drafts/` and `ideas.md`. It commits to the repo, and I review the diff.
