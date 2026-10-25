# Ticket resolution

- **Goal:** first response within 4 working hours, and a known fix for the top 10 ticket types.
- **Status:** active
- **Source of tickets:** Jira project PLAT. Tickets stay in Jira; nothing is copied here.

## Files

- `kb/<category>.md`: known fixes per category (symptom, cause, fix, verified on). The `ticket-triage` skill reads these.
- `metrics.md`: monthly counts by category and time to first response

## Next actions

1. Write kb entries for the 5 most common access tickets.
2. Pilot AUT-005 (webhook triage) on new PLAT tickets for 2 weeks, then compare the drafts with the final replies.
