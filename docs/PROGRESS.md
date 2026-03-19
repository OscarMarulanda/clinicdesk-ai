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

---

## 2026-03-18 — Phase 6.4 Complete: Admin Dashboard Frontend

**Completed:**
- Admin dashboard SPA: login, sidebar nav, 4 tabs
- Knowledge Base tab: article list with search/filter by category, create/edit/delete via modal
- Sessions tab: session list with status badges, click-to-view detail with full transcript, token counts, cost breakdown, tool call log, per-turn breakdown table
- Escalations tab: list with reason/status badges, click-to-view detail with conversation transcript, escalation info, status update controls, link to full session
- Analytics tab: 6 metric cards, top categories, escalation reasons, period selector (7d/30d/90d)
- Design follows reference-design style: dark sidebar, white cards with rounded-xl borders, Inter font, OKLch-inspired color palette, color-coded badges

---

## 2026-03-18 — Bug Fixes & Improvements

**Bugs fixed:**
- Session detail API crash: `tool_calls` field stored as `list[str]` but DTO declared `list[dict]` — fixed DTO to `list[str]`
- Password hash mismatch in seed data — regenerated bcrypt hash for 'demo123'
- Chat widget session persistence: page refresh showed blank chat despite having a stored session — added `/api/sessions/{id}/messages` public endpoint and widget now loads previous messages on reconnect
- Google Calendar 403 error: service accounts can't invite attendees without Domain-Wide Delegation — removed attendees from event, put user email in description instead
- Calendar events created at wrong time: parser used UTC, events showed 5 hours off — switched to local time with `America/Bogota` timezone in Calendar API
- Escalations not always created: agent skipped `escalate_to_human` and called `schedule_callback`/`send_escalation_email` directly

**Improvements:**
- **Fused escalation tools**: Merged `schedule_callback` and `send_escalation_email` into `escalate_to_human`. Now a single tool call creates the DB record AND handles calendar + email based on `preferred_action`. Reduced from 8 tools to 6. Eliminates risk of agent skipping the escalation record.
- **Chat widget — FAB draggable**: bubble is now draggable (click still opens chat, drag moves it)
- **Chat widget — resizable**: top-left resize handle on chat window
- **Escalation detail view**: click escalation row in admin dashboard to see full transcript + escalation info + status controls
- **Calendar time parser improved**: handles more patterns (3:30pm, after 4, asap, morning, afternoon, evening)

**Next:** Tests, README, write-up.

---

## 2026-03-18 — Phase 8 Complete: Tests, README, Write-up

**Completed:**
- 72 tests across 4 layers (domain, application, infrastructure, presentation)
- pytest + pytest-asyncio with session-scoped event loop for DB integration tests
- README with quick start, architecture overview, feature list, embed instructions
- Write-up covering problem, solution, design decisions, future enhancements

---

## 2026-03-18 — Phase 9 Partial: Integrations & Notifications

**Completed:**
- **SendGrid live**: API key configured, emails sending to both admin and user on escalation
- **Real users**: Oscar Marulanda as admin (unal.edu.co) and staff (gmail)
- **Admin notifications**: bell icon with red unread badge, dropdown with notification list, click navigates to escalation detail
- **Real-time push**: Admin WebSocket (`/ws/admin`) broadcasts notifications instantly — no polling delay
- **Email structure**: clean subject line, structured body, user gets confirmation email with reference number
- **Email always sent**: regardless of user's preferred_action (calendar/email/both)

**Bugs fixed:**
- Empty chat bubble: agent text was lost across tool loop rounds — now accumulates all text parts
- `reason_label` undefined in email code — moved definition above email section
- Email subject contained full summary — cleaned up to short label only

**Deviations:**
- Originally planned identify form in chat widget for auth — decided against adding friction, agent collects email naturally during escalation instead
- Notifications use WebSocket push instead of polling (user requested instant updates)

**Next:** Deployment, desktop embedding research, session management, prompt caching.
