# ClinicDesk AI — Customer Support Agent

AI-powered customer support agent for clinic staff who use practice management software. Built with Clean Architecture, Claude Sonnet 4.6 with tool calling, PostgreSQL full-text search, and real-time WebSocket chat.

## Live Demo

| Page | URL |
|------|-----|
| Chat widget | https://clinicdesk-ai.fly.dev/static/widget/demo.html |
| Admin dashboard | https://clinicdesk-ai.fly.dev/static/admin/ |
| API docs | https://clinicdesk-ai.fly.dev/docs |

**Admin login:** create an account via Sign Up, or use `clinicdeskai@gmail.com` / `odmb7750`

See `docs/DEMO_SCRIPT.md` for a guided walkthrough of all features.

## What It Does

Clinic staff (office managers, front desk, billing coordinators) get instant help with software questions, billing workflows, insurance claims, and troubleshooting — without waiting on hold for a support rep.

- **Conversational AI agent** that searches a 67-article knowledge base and walks users through multi-step procedures
- **Human escalation system** with calendar availability checking, Google Calendar callback scheduling, and email notifications to all admin users via SendGrid
- **Admin dashboard** for knowledge base management, session viewing with cost/token metrics, escalation tracking, and analytics
- **Drag-and-drop document ingestion** — drop a PDF, DOCX, or TXT onto the admin dashboard and the AI structures it as a KB article for review
- **Embeddable chat widget** with Shadow DOM isolation, drag-to-move, and session persistence
- **Knowledge feedback loop** — when the agent can't answer, admins see the gap and add articles; the agent immediately starts answering

## Quick Start (Local Development)

### Prerequisites

- Python 3.13+
- PostgreSQL 17+
- Anthropic API key

### Setup

```bash
# Clone and enter the project
git clone https://github.com/OscarMarulanda/clinicdesk-ai.git && cd clinicdesk-ai

# Create virtual environment and install dependencies
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Create database and run migrations
createdb clinicdesk
python -m src.infrastructure.database.migrate --seed

# Start the server
uvicorn src.main:app --reload --port 8000
```

### Local Access

| Page | URL |
|------|-----|
| Chat widget demo | http://localhost:8000/static/widget/demo.html |
| Admin dashboard | http://localhost:8000/static/admin/ |
| API docs | http://localhost:8000/docs |

## Architecture

Clean Architecture with strict dependency inversion:

```
src/
├── domain/           # Entities, repository ABCs, exceptions (no external deps)
├── application/      # Use cases, DTOs, service interfaces
├── infrastructure/   # asyncpg repos, Claude API, Google Calendar, SendGrid, document extraction
├── presentation/     # FastAPI routes, WebSocket handlers, auth middleware
└── main.py           # Composition root
```

Dependencies always point inward: Presentation → Application → Domain ← Infrastructure.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.13, FastAPI 0.135.1, Uvicorn |
| Database | PostgreSQL 17, asyncpg (raw SQL, no ORM) |
| AI | Claude Sonnet 4.6 via Anthropic SDK with tool calling |
| Search | PostgreSQL tsvector/tsquery with GIN index |
| Chat | WebSocket (real-time), Shadow DOM widget |
| Escalation | Google Calendar API, SendGrid |
| Auth | JWT + bcrypt, role-based (staff/admin) |
| Document ingestion | pymupdf (PDF), python-docx (DOCX) |
| Deployment | Fly.io (sjc) + Supabase PostgreSQL |

## Features

### Chat Widget
- Embeddable via single `<script>` tag
- Shadow DOM for CSS isolation
- Draggable bubble and resizable window
- Markdown rendering (headers, bold, code, lists, tables)
- Session persistence across page reloads
- Auto-reconnect on connection loss

### Agent Tools (6)
| Tool | Purpose |
|------|---------|
| `search_knowledge_base` | Full-text search across 67 articles |
| `get_article` | Retrieve full article content |
| `check_availability` | Check calendar for open callback slots (read-only) |
| `escalate_to_human` | Create escalation + book callback + send emails (fused) |
| `update_session_notes` | Agent scratchpad for context |
| `list_categories` | Browse knowledge base categories |

### Defensive Calendar Booking
- System prompt enforces mandatory check → confirm → book flow
- Backend rejects bookings if availability wasn't checked first (validated via session state)
- `create_event` re-verifies the slot is free before inserting
- Timezone-safe comparisons via `zoneinfo`

### Admin Dashboard
- **Knowledge Base**: CRUD with search/filter by category
- **Document Ingestion**: Drag-and-drop PDF/DOCX/TXT → AI structures as KB article → review modal
- **Sessions**: Transcript viewer with per-turn token counts, cost breakdown, tool call log
- **Escalations**: Detail view with linked conversation, status management
- **Analytics**: Session counts, escalation rate, resolution rate, cost/token metrics, top categories
- **Notifications**: Real-time push via WebSocket when escalations are created
- **Admin Registration**: Sign up from login screen, all admins receive escalation emails

### Session Metrics
Every conversation tracks:
- Input/output tokens per turn
- Cost calculation (Sonnet 4.6 pricing: $3/M in, $15/M out)
- Tool calls made with counts
- Cumulative session cost

## External Integrations

### Google Calendar (callback scheduling)
Requires a Google Cloud service account with Calendar API enabled. See `docs/SETUP.md` for setup steps.

### SendGrid (escalation emails)
Requires a SendGrid API key. Escalation emails are sent to all admin users and the requesting user.

Both integrations run in stub mode when credentials are not configured — the system logs actions to console instead.

## Testing

```bash
source .venv/bin/activate
python -m pytest tests/ -v
```

72 tests across 4 layers:
- **Domain** (21): entity creation, business logic, exceptions
- **Application** (15): use cases with mocked repositories
- **Infrastructure** (22): repositories against real PostgreSQL
- **Presentation** (14): REST API endpoints via httpx

## Deployment

Deployed on Fly.io (San Jose) with Supabase PostgreSQL (us-west-2). See `docs/SETUP.md` for deployment instructions.

```bash
fly deploy
```

## Project Documentation

| Document | Description |
|----------|-------------|
| `docs/WRITEUP.md` | Problem, solution, design decisions, tradeoffs, what's next |
| `docs/DEMO_SCRIPT.md` | Guided demo walkthrough with 5 scenarios |
| `docs/ARCHITECTURE.md` | System design, component breakdown, data flows |
| `docs/AGENT_DESIGN.md` | System prompt, tool schemas, conversation patterns |
| `docs/API_SPEC.md` | All REST and WebSocket endpoints |
| `docs/DATABASE.md` | Schema, indexes, full-text search strategy |
| `docs/CHECKLIST.md` | Implementation checklist with status |
| `docs/PROGRESS.md` | Development log with decisions and deviations |
| `docs/ADR/` | Architecture Decision Records (6) |
| `docs/SETUP.md` | Detailed setup, configuration, and deployment guide |

## Embed the Widget

Add this to any website:

```html
<script src="https://clinicdesk-ai.fly.dev/static/widget/chat-widget.js"
        data-server="wss://clinicdesk-ai.fly.dev"
        data-color="#2563eb"
        data-title="Support"
        data-greeting="Hi! How can I help you today?">
</script>
```
