# ClinicDesk AI — Write-Up

## Problem

Small dental and medical clinics don't have IT departments. When the office manager can't figure out how to submit an insurance pre-authorization, or the billing coordinator doesn't know how to handle a denied claim, they either call support (long hold times), search through outdated documentation, or figure it out wrong. An AI agent with the full knowledge base at its fingertips — one that can walk them through multi-step workflows in real time — is transformative.

## Solution

ClinicDesk AI is a conversational support agent that sits inside the practice management software as an embeddable chat widget. It searches a structured knowledge base of 67 articles across 7 categories (scheduling, billing, insurance, patient records, reporting, troubleshooting, account management) and walks clinic staff through procedures step by step. When it can't answer confidently — or when the user is frustrated, asking about billing disputes, or requesting account changes — it escalates to a human by scheduling a Google Calendar callback and notifying the support team.

## Key Design Decisions

**Clean Architecture** — The backend follows strict Clean Architecture with dependency inversion. The domain layer (entities, repository interfaces) has zero knowledge of FastAPI, asyncpg, or the Claude API. This means we can swap any infrastructure component (database driver, LLM provider, email service) without touching business logic. It also makes the codebase highly testable: 72 tests across domain, application, infrastructure, and presentation layers run in 1 second.

**Single agent with fused tools** — Rather than a multi-agent system with routing overhead, we use a single Claude agent with 6 tools. The most critical design iteration was fusing the escalation tools: originally, `escalate_to_human`, `schedule_callback`, and `send_escalation_email` were separate tools. During testing, the agent would sometimes call `schedule_callback` without first creating the escalation record, making escalations invisible in the admin dashboard. We fused all three into a single `escalate_to_human` tool that atomically creates the record and triggers the callback/email. This eliminated the reliability issue entirely.

**PostgreSQL full-text search** — For a structured knowledge base with well-titled, categorized articles, PostgreSQL's built-in `tsvector`/`tsquery` with weighted ranking (title weight A, content weight B) provides fast, relevant search with no external dependencies. This is sufficient for the current scale; vector embeddings (pgvector) would be the next step for unstructured documents like PDFs and manuals.

**Admin → Knowledge → Agent feedback loop** — This is the system's key differentiator. When the agent can't answer a question, it escalates. The admin sees the gap in the escalation log, creates a new knowledge article through the dashboard, and the next user who asks the same question gets an answer. The system improves over time without code changes.

## What I'd Build Next

- **Multi-agent architecture**: Separate billing, scheduling, and technical agents with a router, each with tailored prompts and safety guardrails
- **Prompt caching**: The system prompt is identical across turns — caching would reduce costs significantly at scale
- **Vector search**: For ingesting unstructured documents (PDFs, product manuals) alongside the structured knowledge base
- **Voice channel**: Twilio + Deepgram + TTS for phone-based support
- **Knowledge gap analytics**: Auto-detect which topics trigger the most escalations and surface them to admins as content priorities
- **HIPAA compliance path**: Encryption at rest, comprehensive audit logging, BAA with cloud providers
