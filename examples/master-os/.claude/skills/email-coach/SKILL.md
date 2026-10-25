---
name: email-coach
description: Compare each email draft the email agent wrote with what I actually sent, find the patterns in my edits, and propose changes to context/voice.md. Use when I say "coach me", "how did the drafts do", or when the coach automation (AUT-002) runs.
---

# Email coach

## Steps

1. Read the day's entries from `brands/<brand>/data/email-log/drafts.jsonl`. Default to today and all brands, one brand at a time.
2. For each draft, find my sent message in the same conversation (Sent Items, matched by `conversation_id`).
3. Score each draft:
   - **As-is:** sent with no real change
   - **Light edit:** wording or length only
   - **Heavy edit:** facts, structure or tone changed
   - **Not used:** no sent reply, or I wrote a fresh one
4. For the edited ones, note what I cut, added or rewrote. Quote short fragments only.
5. Find the top 3 patterns, for example "always removes the opening line" or "adds the ticket ID".

## Output

Write `brands/<brand>/data/email-log/coach-YYYY-MM-DD.md` with:

- A score table: as-is, light, heavy, not used (counts and %)
- The top 3 patterns, each with one example
- The proposed edits to `context/voice.md`, as a diff

**Never edit `voice.md` directly.** In an interactive session, show the diff and ask me. In an automation run, leave the diff in the report.

Track the trend: if "as-is + light edit" isn't rising week on week, say so at the top of the report.
