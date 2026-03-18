# ADR-006: Fused Escalation Tool (Single Tool for Record + Calendar + Email)

## Status
Accepted

## Context
The agent originally had 3 separate tools for escalation:
1. `escalate_to_human` — create DB record
2. `schedule_callback` — create Google Calendar event
3. `send_escalation_email` — send SendGrid email

During testing, the agent would sometimes call `schedule_callback` or `send_escalation_email` without first calling `escalate_to_human`, resulting in calendar events or emails being sent with no corresponding escalation record in the database. This made escalations invisible in the admin dashboard.

An intermediate fix (adding instructions to the system prompt telling the agent to always call `escalate_to_human` first) was attempted but proved unreliable — the agent still skipped it in some conversations.

## Decision
Fuse all three tools into a single `escalate_to_human` tool. The tool accepts an optional `user_email` and `preferred_time`, and internally creates the DB record, then triggers calendar and/or email based on the `preferred_action` field.

## Rationale
- **Reliability**: A single tool call cannot be partially executed — the DB record is always created
- **Simpler for the agent**: One tool to learn, one call to make, fewer decisions to get wrong
- **No loss of flexibility**: The `preferred_action` field (calendar/email/both) still lets the user choose their preference
- **Cleaner code**: Escalation logic is in one place instead of spread across 3 tool handlers

## Trade-offs
- Slightly larger tool schema (more optional fields)
- Less granular tool call tracking in metrics (one `escalate_to_human` call instead of seeing separate `schedule_callback` + `send_escalation_email`)
- If only the calendar or email portion fails, the escalation record is still created (acceptable — better than the reverse)

## Tool count
Reduced from 8 tools to 6.
