---
name: email-reply
description: Draft a reply to an email in my voice, for the right brand. Use when I ask to reply to, answer or draft a response to an email, or when the email agent automation (AUT-001) runs. Saves drafts only and never sends.
---

# Email reply

## 1. Pick the brand

- Sender domain `contoso.com` means **org-contoso**.
- Sender is a main contact in a `clients/*.md` file means that **client**.
- Anything else means **personal**.
- Still unclear: ask me in an interactive session. In an automation run, skip the email and log `skipped: brand unclear`.

## 2. Load only that brand's context

- `context/voice.md` (always)
- The brand's `CLAUDE.md`, or the client's pointer file
- For an org ticket email: `brands/org-contoso/projects/ticket-resolution/kb/` for a known fix

Don't open another brand's files. Don't open client deliverables.

## 3. Draft

Follow `context/voice.md`: answer first, under 120 words, numbered steps, one clear ask. If a fact is missing (a run ID, a workspace name), ask for it in the draft instead of guessing.

## 4. Save and log

1. Save the reply as a draft in the mail client. Never send.
2. Append one line to `brands/<brand>/data/email-log/drafts.jsonl`:
   `{"date": "...", "conversation_id": "...", "to": "...", "subject": "...", "draft": "..."}`

The `email-coach` skill reads this log to compare each draft with what I sent.
