# ClinicDesk AI — Architecture Document

## Overview

ClinicDesk AI is an AI-powered customer support agent for clinic staff (office managers, front desk, billing coordinators, clinic owners) who use practice management software. The system provides instant, contextual help by searching a structured knowledge base and walking users through multi-step workflows.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend                           │
│  ┌──────────────┐  ┌──────────────────────────────────┐ │
│  │ Chat Widget   │  │ Admin Dashboard                  │ │
│  │ (embeddable)  │  │ - Knowledge management           │ │
│  │               │  │ - Escalation log                 │ │
│  │               │  │ - Session viewer                 │ │
│  │               │  │ - Analytics                      │ │
│  └──────┬───────┘  └──────────────┬───────────────────┘ │
└─────────┼──────────────────────────┼────────────────────┘
          │ WebSocket                │ REST API
┌─────────┼──────────────────────────┼────────────────────┐
│         ▼                          ▼       Backend      │
│                                                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │              Presentation Layer                     │ │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────┐  │ │
│  │  │ WS Handlers  │  │ REST Routes   │  │ Middleware│  │ │
│  │  │ (chat)       │  │ (admin API)   │  │ (auth)   │  │ │
│  │  └──────┬───────┘  └──────┬───────┘  └──────────┘  │ │
│  └─────────┼─────────────────┼────────────────────────┘ │
│            │ depends on      │                          │
│            ▼                 ▼                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │              Application Layer                      │ │
│  │  ┌────────────────────────────────────────────────┐ │ │
│  │  │ Use Cases (one per operation)                   │ │ │
│  │  │ - SearchKnowledgeBase                           │ │ │
│  │  │ - ProcessChatMessage                            │ │ │
│  │  │ - CreateEscalation                              │ │ │
│  │  │ - ManageArticles (CRUD)                         │ │ │
│  │  │ - GetAnalytics                                  │ │ │
│  │  │ - ScheduleCallback                              │ │ │
│  │  │ - ...                                           │ │ │
│  │  └────────────────────────────────────────────────┘ │ │
│  │  ┌────────────────────────────────────────────────┐ │ │
│  │  │ DTOs (input/output data contracts)              │ │ │
│  │  └────────────────────────────────────────────────┘ │ │
│  │  ┌────────────────────────────────────────────────┐ │ │
│  │  │ External Service Interfaces (ABCs)              │ │ │
│  │  │ - AIServiceInterface                            │ │ │
│  │  │ - CalendarServiceInterface                      │ │ │
│  │  │ - EmailServiceInterface                         │ │ │
│  │  └────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────┘ │
│            │ depends on                                 │
│            ▼                                            │
│  ┌────────────────────────────────────────────────────┐ │
│  │              Domain Layer (innermost)                │ │
│  │  ┌──────────────┐  ┌────────────────────────────┐  │ │
│  │  │ Entities      │  │ Repository Interfaces (ABCs)│  │ │
│  │  │ - Article     │  │ - KnowledgeRepositoryBase   │  │ │
│  │  │ - Session     │  │ - SessionRepositoryBase     │  │ │
│  │  │ - Escalation  │  │ - EscalationRepositoryBase  │  │ │
│  │  │ - User        │  │ - UserRepositoryBase        │  │ │
│  │  │ - Provider    │  │ - ProviderRepositoryBase    │  │ │
│  │  └──────────────┘  └────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │ Domain Exceptions                             │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────┘ │
│            ▲ implements                                  │
│            │                                            │
│  ┌────────────────────────────────────────────────────┐ │
│  │              Infrastructure Layer                   │ │
│  │  ┌──────────────┐  ┌────────────────────────────┐  │ │
│  │  │ PostgreSQL    │  │ External Services           │  │ │
│  │  │ Repositories  │  │ - ClaudeAIService           │  │ │
│  │  │ (asyncpg)     │  │ - GoogleCalendarService     │  │ │
│  │  │               │  │ - SendGridEmailService      │  │ │
│  │  └──────────────┘  └────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │ Config / Settings                             │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────┘ │
│                                                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Composition Root (main.py)                         │ │
│  │  - Wires all dependencies together                  │ │
│  │  - FastAPI dependency injection                     │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## The Dependency Rule

**Dependencies always point inward.** No inner layer knows about any outer layer.

```
Presentation → Application → Domain ← Infrastructure
```

- **Domain** depends on nothing. Pure Python, no imports from FastAPI, asyncpg, or anthropic.
- **Application** depends only on Domain. Defines use cases that orchestrate entities and call repository/service interfaces defined in Domain and Application.
- **Infrastructure** depends on Domain + Application. Implements the abstract interfaces with concrete technology (asyncpg, Claude SDK, SendGrid, Google Calendar).
- **Presentation** depends on Application. Calls use cases, never touches repositories or infrastructure directly.

## Project Structure

```
src/
├── domain/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── article.py          # Article entity
│   │   ├── session.py          # Session entity
│   │   ├── escalation.py       # Escalation entity
│   │   ├── user.py             # User entity
│   │   └── provider.py         # Provider entity
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── knowledge_repository.py   # ABC
│   │   ├── session_repository.py     # ABC
│   │   ├── escalation_repository.py  # ABC
│   │   ├── user_repository.py        # ABC
│   │   └── provider_repository.py    # ABC
│   └── exceptions.py           # Domain-specific exceptions
│
├── application/
│   ├── __init__.py
│   ├── use_cases/
│   │   ├── __init__.py
│   │   ├── search_knowledge_base.py
│   │   ├── get_article.py
│   │   ├── process_chat_message.py
│   │   ├── create_escalation.py
│   │   ├── schedule_callback.py
│   │   ├── send_escalation_email.py
│   │   ├── manage_articles.py      # CRUD use cases
│   │   ├── get_sessions.py
│   │   ├── manage_escalations.py
│   │   ├── get_analytics.py
│   │   ├── authenticate_user.py
│   │   └── update_session_notes.py
│   ├── dto/
│   │   ├── __init__.py
│   │   ├── chat.py              # ChatInput, ChatOutput
│   │   ├── article.py           # ArticleCreate, ArticleUpdate, ArticleResponse
│   │   ├── escalation.py        # EscalationCreate, EscalationResponse
│   │   ├── session.py           # SessionResponse, SessionDetail
│   │   └── analytics.py         # AnalyticsResponse
│   └── interfaces/
│       ├── __init__.py
│       ├── ai_service.py        # ABC for AI/LLM interaction
│       ├── calendar_service.py  # ABC for calendar integration
│       └── email_service.py     # ABC for email sending
│
├── infrastructure/
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py        # asyncpg pool management
│   │   ├── knowledge_repository.py   # implements ABC
│   │   ├── session_repository.py     # implements ABC
│   │   ├── escalation_repository.py  # implements ABC
│   │   ├── user_repository.py        # implements ABC
│   │   └── provider_repository.py    # implements ABC
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── claude_service.py    # implements AIServiceInterface
│   │   ├── system_prompt.py     # prompt template
│   │   └── tools.py             # tool definitions and execution
│   ├── calendar/
│   │   ├── __init__.py
│   │   └── google_calendar_service.py  # implements CalendarServiceInterface
│   ├── email/
│   │   ├── __init__.py
│   │   └── sendgrid_service.py  # implements EmailServiceInterface
│   └── config.py                # Settings, env var loading
│
├── presentation/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── articles.py          # Knowledge base CRUD routes
│   │   ├── sessions.py          # Session listing/detail routes
│   │   ├── escalations.py       # Escalation management routes
│   │   ├── analytics.py         # Analytics routes
│   │   └── auth.py              # Login/auth routes
│   ├── ws/
│   │   ├── __init__.py
│   │   └── chat.py              # WebSocket chat handler
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py              # Auth + RBAC middleware
│   └── dependencies.py          # FastAPI dependency injection setup
│
├── main.py                      # Composition root — wires everything
│
migrations/
├── 001_initial.sql
├── 002_seed_knowledge_base.sql
│
frontend/
├── widget/
│   ├── chat-widget.js
│   ├── chat-widget.css
│   └── demo.html
├── admin/
│   ├── index.html
│   ├── app.js
│   └── styles.css
```

## Data Flow

### Chat Flow
```
User types message in widget
  → WebSocket sends to presentation/ws/chat.py
    → Calls ProcessChatMessage use case
      → Use case loads session via SessionRepositoryBase
      → Use case calls AIServiceInterface.process(message, context, tools)
        → Infrastructure: ClaudeService calls Claude API
          → Claude may call tools → use case executes them via repository/service interfaces
          → Claude generates response
      → Use case saves updated session via SessionRepositoryBase
      → Returns ChatOutput DTO
    → WebSocket sends response to widget
  → Widget renders markdown response
```

### Escalation Flow
```
Agent detects escalation trigger
  → Agent calls escalate_to_human tool (single fused tool)
    → ProcessChatMessage creates Escalation via EscalationRepositoryBase
    → If preferred_action includes calendar: calls CalendarServiceInterface.create_event()
    → If preferred_action includes email: calls EmailServiceInterface.send()
    → Updates escalation record with calendar_event_id / email_sent_at
  → Returns confirmation to agent → user
```

### Knowledge Feedback Loop
```
Agent can't answer → escalates → admin sees gap
  → Admin creates article via ManageArticles use case
    → Saved via KnowledgeRepositoryBase (with tsvector)
  → Next user asks same question
    → SearchKnowledgeBase use case finds new article → agent answers
```

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Language | Python | 3.13.x |
| Backend framework | FastAPI | 0.135.1 |
| ASGI server | Uvicorn | 0.42.0 |
| Database driver | asyncpg | 0.31.0 |
| Database | PostgreSQL | 16+ |
| Validation | Pydantic | 2.12.5 |
| AI SDK | anthropic | ~0.85.0 |
| AI Model | Claude Sonnet 4 | claude-sonnet-4-20250514 |
| Email | SendGrid | 6.x |
| Calendar | google-api-python-client | latest |
| Frontend widget | Vanilla HTML/CSS/JS | — |
| Frontend admin | Tailwind CSS + vanilla JS | — |

> **Note on AI model**: The spec targets `claude-sonnet-4-20250514`. Newer models (Sonnet 4.5, Sonnet 4.6) are available with improved tool calling. We can upgrade the model string with no code changes.

## Key Architectural Decisions

See `docs/ADR/` for detailed records. Summary:

1. **ADR-001**: Clean Architecture over layered — domain independence, testability, swappable infrastructure
2. **ADR-002**: asyncpg over SQLAlchemy — direct SQL control, async-native, less abstraction overhead
3. **ADR-003**: PostgreSQL full-text search over vector embeddings — sufficient for structured articles, no external dependencies
4. **ADR-004**: Single agent with tools over multi-agent — simpler routing, sufficient for current scope
5. **ADR-005**: Shadow DOM chat widget — style isolation for embedding in any site
6. **ADR-006**: Fused escalation tool — single tool creates record + calendar + email, preventing agent from skipping the DB record
