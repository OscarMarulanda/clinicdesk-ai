# ClinicDesk AI — Progress Log

## How to use this document

Each entry records: date, what was completed, any deviations from the plan, and what's next. Updated after each implementation milestone.

---

## 2026-03-17 — Project Documentation & Planning

**Completed:**
- Created project documentation structure (`docs/`)
- Created `/update-docs` custom skill for documentation maintenance reminders
- Saved memory: always update docs after implementation work
- Saved memory: always check latest stable dependency versions
- Saved memory: use Clean Architecture for backend
- Designed Clean Architecture backend structure (domain → application → infrastructure → presentation)
- Verified latest stable versions of all dependencies
- Created all foundational docs: ARCHITECTURE, CHECKLIST, DATABASE, API_SPEC, AGENT_DESIGN, SETUP, PROGRESS
- Created initial ADRs: Clean Architecture, asyncpg, full-text search, single agent, Shadow DOM widget

**Deviations from original spec:**
- Original spec described a layered architecture (routes → services → repositories). Changed to Clean Architecture at user's request. This adds more files and abstractions but provides better testability and framework independence.
- Upgraded Python from 3.12 (in spec) to 3.13 based on version check — 3.13.12 is latest stable.

**Dependency versions verified:**
| Package | Version |
|---------|---------|
| Python | 3.13.x |
| FastAPI | 0.135.1 |
| Uvicorn | 0.42.0 |
| asyncpg | 0.31.0 |
| Pydantic | 2.12.5 |
| anthropic | ~0.85.0 |
| SendGrid | 6.x |

**Next:** Phase 1 — project setup, database schema, domain layer, repository implementations.

---

## 2026-03-17 — Phase 1 Complete: Project Foundation

**Completed:**
- Full Clean Architecture directory structure
- Python 3.13.12 venv, all dependencies installed and pinned
- PostgreSQL 17 — database `clinicdesk` created, all 5 tables, indexes, tsvector trigger
- 5 domain entities, 5 repository ABCs, 5 Postgres repo implementations
- 3 application service interfaces (AI, Calendar, Email)
- Migration runner, seed data (3 users, 3 providers)
- FastAPI app boots with health endpoint

**Deviations:** Using local PostgreSQL 17 instead of Docker (Docker not installed).

---

## 2026-03-17 — Phase 2 Complete: Agent Core

**Completed:**
- ClaudeAIService with tool calling and tool result continuation
- System prompt and 8 tool definitions
- ProcessChatMessage use case — full agent loop with up to 10 tool rounds
- 11 total use cases (process chat, manage articles, sessions, escalations, analytics, auth, etc.)
- 5 DTO modules
- WebSocket chat handler, 5 REST route files, JWT auth + RBAC middleware
- GoogleCalendarService and SendGridEmailService (with stub fallbacks)
- Composition root (main.py) wiring all dependencies
- All routes verified working: login, auth-protected endpoints, analytics

---

## 2026-03-17 — Phase 3 Complete: Knowledge Base Seed Data

**Completed:**
- 67 articles across 7 categories generated in parallel (7 agents)
- All articles inserted via migrations/002_seed_knowledge_base.sql
- Full-text search verified working with weighted ranking (title=A, content=B)

---

## 2026-03-17 — Phase 4 Complete: Chat Widget + Session Metrics

**Completed:**
- Embeddable chat widget: Shadow DOM, single `<script>` tag embed
- Draggable (mouse + touch drag via header)
- Refresh button for new conversations
- Markdown rendering (headers, bold, italic, code, lists, tables)
- Typing indicator, auto-reconnect, session persistence
- Mobile responsive (full-screen on small devices)
- Demo page at /static/widget/demo.html
- Enhanced session metadata: per-turn token counts, cost calculation, tool call log, aggregate tool counts
- Cost calculation uses Sonnet 4 pricing ($3/M input, $15/M output)

**Deviations:** Added draggable + refresh features (user request). Added per-turn metrics tracking beyond original spec.

**Next:** Phase 6.4 — Admin Dashboard frontend (the backend APIs are all done). Then Phase 8 — testing and polish.
