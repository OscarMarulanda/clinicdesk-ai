# ClinicDesk AI — Write-Up

## Problem

Small dental and medical clinics don't have IT departments. When the office manager can't figure out how to submit an insurance pre-authorization, or the billing coordinator doesn't know how to handle a denied claim, they either call support (long hold times), search through outdated documentation, or figure it out wrong. An AI agent with the full knowledge base at its fingertips — one that can walk them through multi-step workflows in real time — is transformative.

## Solution

ClinicDesk AI is a conversational support agent that sits inside the practice management software as an embeddable chat widget. It searches a structured knowledge base of 67 articles across 7 categories (scheduling, billing, insurance, patient records, reporting, troubleshooting, account management) and walks clinic staff through procedures step by step. When it can't answer confidently — or when the user is frustrated, asking about billing disputes, or requesting account changes — it escalates to a human: it checks the support team's Google Calendar for availability, lets the user pick a slot, books the callback, and sends confirmation emails to both the user and the admin via SendGrid. The entire escalation flow — record creation, calendar booking, and email notifications — happens atomically in a single tool call.

## Key Design Decisions

**Clean Architecture** — The backend follows strict Clean Architecture with dependency inversion. The domain layer (entities, repository interfaces) has zero knowledge of FastAPI, asyncpg, or the Claude API. This means we can swap any infrastructure component (database driver, LLM provider, email service) without touching business logic. It also makes the codebase highly testable: 72 tests across domain, application, infrastructure, and presentation layers run in 1 second.

**Single agent with fused tools** — Rather than a multi-agent system with routing overhead, we use a single Claude agent with 7 tools. The most critical design iteration was fusing the escalation tools: originally, `escalate_to_human`, `schedule_callback`, and `send_escalation_email` were separate tools. During testing, the agent would sometimes call `schedule_callback` without first creating the escalation record, making escalations invisible in the admin dashboard. We fused all three into a single `escalate_to_human` tool that atomically creates the record and triggers the callback/email. This eliminated the reliability issue entirely.

**Defensive calendar booking** — During live testing, we discovered the agent would sometimes skip the availability check and book callbacks on already-occupied slots. We fixed this with three layers of defense: the system prompt enforces a mandatory check → confirm → book flow; the backend rejects booking attempts if no availability check was performed (validated via session state); and `create_event` re-verifies the slot is free with a real-time calendar query before inserting. Even if the LLM skips a step, the backend won't allow a double booking.

**PostgreSQL full-text search** — For a structured knowledge base with well-titled, categorized articles, PostgreSQL's built-in `tsvector`/`tsquery` with weighted ranking (title weight A, content weight B) provides fast, relevant search with no external dependencies. This is sufficient for the current scale; vector embeddings (pgvector) would be the next step for unstructured documents like PDFs and manuals.

**Admin → Knowledge → Agent feedback loop** — This is the system's key differentiator. When the agent can't answer a question, it escalates. The admin sees the gap in the escalation log, creates a new knowledge article through the dashboard, and the next user who asks the same question gets an answer. The system improves over time without code changes.

## Tradeoffs

- **Vanilla JS over React** — The chat widget and admin dashboard use plain HTML/CSS/JS with no build step. This made the widget trivially embeddable (single `<script>` tag, Shadow DOM isolation) and eliminated framework overhead. The tradeoff is that the admin dashboard code is less structured than it would be with components, but at this scale it's manageable.
- **Raw SQL (asyncpg) over ORM** — Direct SQL gives full control over PostgreSQL-specific features like `tsvector`, `ts_rank`, and GIN indexes. An ORM would have added abstraction overhead without helping, since the queries are tuned for full-text search performance.
- **Single agent over multi-agent** — A router + specialized agents would add latency and complexity. For a support agent with a bounded knowledge base, one agent with well-scoped tools is simpler and equally capable. Multi-agent becomes worthwhile when domains diverge enough to need separate system prompts and safety guardrails.

## What I'd Build Next

- **Prompt caching**: The system prompt and knowledge base context are identical across turns — caching would cut input token costs significantly at scale
- **Knowledge gap analytics**: Auto-detect which topics trigger the most escalations and surface them to admins as content priorities, closing the feedback loop faster
- **Vector search**: pgvector for ingesting unstructured documents (PDFs, product manuals) alongside the structured knowledge base
