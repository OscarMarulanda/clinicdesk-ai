# ClinicDesk AI — Customer Support Agent

AI-powered customer support agent for clinic staff who use practice management software. Built with Clean Architecture, Claude API with tool calling, PostgreSQL full-text search, and real-time WebSocket chat.

## What It Does

Clinic staff (office managers, front desk, billing coordinators) get instant help with software questions, billing workflows, insurance claims, and troubleshooting — without waiting on hold for a support rep.

- **Conversational AI agent** that searches a 67-article knowledge base and walks users through multi-step procedures
- **Human escalation system** with Google Calendar callback scheduling and email notifications
- **Admin dashboard** for knowledge base management, session viewing with full metrics, and escalation tracking
- **Embeddable chat widget** with Shadow DOM isolation, drag-to-move, and session persistence

## Quick Start

### Prerequisites

- Python 3.13+
- PostgreSQL 16+
- Anthropic API key

### Setup

```bash
# Clone and enter the project
git clone <repo-url> && cd supportAgent

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

### Access

| Page | URL |
|------|-----|
| Chat widget demo | http://localhost:8000/static/widget/demo.html |
| Admin dashboard | http://localhost:8000/static/admin/index.html |
| API docs (auto-generated) | http://localhost:8000/docs |

**Admin login:** `admin@clinicdesk.com` / `demo123`

## Architecture

Clean Architecture with strict dependency inversion:

```
src/
├── domain/           # Entities, repository ABCs, exceptions (no external deps)
├── application/      # Use cases, DTOs, service interfaces
├── infrastructure/   # asyncpg repos, Claude API, Google Calendar, SendGrid
├── presentation/     # FastAPI routes, WebSocket handler, auth middleware
└── main.py           # Composition root
```

Dependencies always point inward: Presentation → Application → Domain ← Infrastructure.

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.13, FastAPI 0.135.1, Uvicorn |
| Database | PostgreSQL 17, asyncpg (raw SQL, no ORM) |
| AI | Claude Sonnet 4 via Anthropic SDK with tool calling |
| Search | PostgreSQL tsvector/tsquery with GIN index |
| Chat | WebSocket (real-time), Shadow DOM widget |
| Escalation | Google Calendar API, SendGrid |
| Auth | JWT + bcrypt, role-based (staff/admin) |

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
| `escalate_to_human` | Create escalation + schedule callback + send email (fused) |
| `update_session_notes` | Agent scratchpad for context |
| `get_user_info` | User profile and plan info |
| `list_categories` | Browse knowledge base categories |

### Admin Dashboard
- **Knowledge Base**: CRUD with search/filter by category
- **Sessions**: Transcript viewer with per-turn token counts, cost breakdown, tool call log
- **Escalations**: Detail view with linked conversation, status management
- **Analytics**: Session counts, escalation rate, resolution rate, top categories

### Session Metrics
Every conversation tracks:
- Input/output tokens per turn
- Cost calculation (Sonnet 4 pricing: $3/M in, $15/M out)
- Tool calls made with counts
- Cumulative session cost

## External Integrations

### Google Calendar (callback scheduling)
Requires a Google Cloud service account with Calendar API enabled. See `docs/SETUP.md` for setup steps.

### SendGrid (escalation emails)
Requires a SendGrid API key. Free tier supports 100 emails/day.

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

## Project Documentation

| Document | Description |
|----------|-------------|
| `docs/ARCHITECTURE.md` | System design, component breakdown, data flows |
| `docs/AGENT_DESIGN.md` | System prompt, tool schemas, conversation patterns |
| `docs/API_SPEC.md` | All REST and WebSocket endpoints |
| `docs/DATABASE.md` | Schema, indexes, full-text search strategy |
| `docs/CHECKLIST.md` | Implementation checklist with status |
| `docs/PROGRESS.md` | Development log with decisions and deviations |
| `docs/ADR/` | Architecture Decision Records (6) |
| `docs/SETUP.md` | Detailed setup and configuration guide |

## Embed the Widget

Add this to any website:

```html
<script src="https://your-server.com/static/widget/chat-widget.js"
        data-server="ws://your-server.com"
        data-color="#2563eb"
        data-title="Support"
        data-greeting="Hi! How can I help you today?">
</script>
```
