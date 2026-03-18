# ClinicDesk AI — Implementation Checklist

## Phase 1: Project Foundation

### 1.1 Project Setup
- [x] Initialize git repository
- [x] Create Clean Architecture directory structure (`src/domain`, `application`, `infrastructure`, `presentation`)
- [x] Set up `requirements.txt` with pinned dependency versions
- [x] Create `.env.example` with all required environment variables
- [x] Create `Makefile` for common operations (run, migrate, seed)
- [x] Set up `.gitignore`

### 1.2 Database Setup
- [x] Docker Compose for local PostgreSQL (using local PostgreSQL 17 instead)
- [x] Migration runner script
- [x] `migrations/001_initial.sql` — users, knowledge_articles, sessions, escalations, providers
- [x] GIN index on `knowledge_articles.search_vector`
- [x] Index on `knowledge_articles.category`
- [x] Verify migrations are idempotent (`IF NOT EXISTS`)

### 1.3 Domain Layer
- [x] `Article` entity
- [x] `Session` entity
- [x] `Escalation` entity
- [x] `User` entity
- [x] `Provider` entity
- [x] `KnowledgeRepositoryBase` (ABC)
- [x] `SessionRepositoryBase` (ABC)
- [x] `EscalationRepositoryBase` (ABC)
- [x] `UserRepositoryBase` (ABC)
- [x] `ProviderRepositoryBase` (ABC)
- [x] Domain exceptions

### 1.4 Infrastructure — Database Repositories
- [x] asyncpg connection pool setup
- [x] `PostgresKnowledgeRepository` — CRUD + full-text search
- [x] `PostgresSessionRepository` — create, update, get, list
- [x] `PostgresEscalationRepository` — create, update status, list
- [x] `PostgresUserRepository` — create, get by email, authenticate
- [x] `PostgresProviderRepository` — list available, get by ID

---

## Phase 2: Agent Core

### 2.1 Application Layer — Service Interfaces
- [x] `AIServiceInterface` (ABC) — process message with tools
- [x] `CalendarServiceInterface` (ABC) — create calendar events
- [x] `EmailServiceInterface` (ABC) — send emails

### 2.2 Infrastructure — Claude AI Service
- [x] `ClaudeAIService` implementing `AIServiceInterface`
- [x] System prompt definition
- [x] Tool schema definitions (6 tools — escalation tools fused into one)
- [x] Tool execution dispatcher
- [x] Conversation loop: message → Claude → tool calls → response
- [x] Token usage tracking

### 2.3 Application Layer — Use Cases
- [x] `SearchKnowledgeBase` use case
- [x] `GetArticle` use case
- [x] `ProcessChatMessage` use case (orchestrates agent + tools)
- [x] `CreateEscalation` use case (fused — now handles calendar + email internally)
- [x] `UpdateSessionNotes` use case
- [x] `GetUserInfo` use case
- [x] `ListCategories` use case

### 2.4 DTOs
- [x] `ChatInput` / `ChatOutput`
- [x] `ArticleCreate` / `ArticleUpdate` / `ArticleResponse`
- [x] `EscalationCreate` / `EscalationResponse`
- [x] `SessionResponse` / `SessionDetail`
- [x] `AnalyticsResponse`

---

## Phase 3: Knowledge Base Seed Data

- [x] Scheduling articles (10 articles)
- [x] Billing & Coding articles (12 articles)
- [x] Insurance & Claims articles (10 articles)
- [x] Patient Records articles (9 articles)
- [x] Reporting & Analytics articles (8 articles)
- [x] Technical / Troubleshooting articles (9 articles)
- [x] Account & Plans articles (9 articles)
- [x] `migrations/002_seed_knowledge_base.sql`
- [x] Verify full-text search returns relevant results

---

## Phase 4: Chat Interface

### 4.1 Presentation — WebSocket
- [x] FastAPI WebSocket route `/ws/chat`
- [x] Session creation on connect
- [x] Message → `ProcessChatMessage` use case → response
- [x] Session context persistence between messages
- [x] Graceful disconnect handling

### 4.2 Chat Widget (Frontend)
- [x] HTML/CSS/JS widget with Shadow DOM
- [x] Configurable via data attributes
- [x] WebSocket connection + auto-reconnect
- [x] Markdown rendering for agent messages
- [x] Typing indicator
- [x] Session persistence (`sessionStorage`)
- [x] Mobile responsive
- [x] Embeddable via single `<script>` tag
- [x] Auto-reconnect on connection loss
- [x] Draggable (header drag handle, mouse + touch)
- [x] Refresh button (new conversation)

### 4.3 Session Metrics Tracking
- [x] Per-turn token counts (input/output)
- [x] Per-turn cost calculation (Sonnet 4 pricing)
- [x] Cumulative session cost
- [x] Per-turn tool call log
- [x] Aggregate tool call counts per session
- [x] Tool round counts per turn

---

## Phase 5: Escalation System

### 5.1 Infrastructure — Google Calendar
- [x] `GoogleCalendarService` implementing `CalendarServiceInterface`
- [x] Create events with summary, attendees, description
- [x] Error handling for API failures
- [x] Stub fallback when credentials not configured

### 5.2 Infrastructure — SendGrid
- [x] `SendGridEmailService` implementing `EmailServiceInterface`
- [x] Escalation email sending
- [x] Error handling for API failures
- [x] Stub fallback when API key not configured

### 5.3 Escalation Workflow (end-to-end)
- [x] Agent detects escalation triggers in conversation
- [x] Agent collects user preferences (time, email)
- [x] Single `escalate_to_human` tool creates DB record + calendar event + email
- [x] Agent confirms to user with details
- [x] Google Calendar integration verified working (service account)
- [x] SendGrid email integration (stub — awaiting API key)

---

## Phase 6: Admin Dashboard

### 6.1 Application — Admin Use Cases
- [x] `ManageArticles` — create, update, delete
- [x] `GetSessions` — list all, get by ID with messages
- [x] `ManageEscalations` — list, update status
- [x] `GetAnalytics` — aggregate stats
- [x] `AuthenticateUser` — login, role check

### 6.2 Presentation — Admin REST API
- [x] `GET /api/admin/articles` — list (search/filter)
- [x] `POST /api/admin/articles` — create
- [x] `GET /api/admin/articles/:id` — get
- [x] `PUT /api/admin/articles/:id` — update
- [x] `DELETE /api/admin/articles/:id` — delete
- [x] `GET /api/admin/sessions` — list
- [x] `GET /api/admin/sessions/:id` — get with messages + metrics
- [x] `GET /api/admin/escalations` — list
- [x] `PUT /api/admin/escalations/:id` — update status
- [x] `GET /api/admin/analytics` — stats

### 6.3 Presentation — RBAC Middleware
- [x] Auth middleware (JWT)
- [x] Role check middleware (admin vs staff)
- [x] Protected admin routes
- [x] Staff routes (chat, own session history)

### 6.4 Admin Frontend
- [x] Dashboard layout with tab navigation (dark sidebar, reference-design style)
- [x] Knowledge Base tab: list + search/filter + create/edit/delete via modal
- [x] Sessions tab: list + transcript viewer + metrics (tools, tokens, cost, per-turn breakdown)
- [x] Escalations tab: list + detail view with transcript + status management
- [x] Analytics tab: metric cards + top categories + escalation reasons + period selector
- [ ] Responsive layout

### 6.5 Public API
- [x] `GET /api/sessions/:id/messages` — public endpoint for widget session restore

---

## Phase 7: Composition & Wiring

- [x] `main.py` composition root — wire all dependencies
- [x] FastAPI dependency injection for use cases
- [x] Startup: create DB pool, initialize services
- [x] Shutdown: close DB pool, cleanup
- [x] CORS configuration
- [x] Static file serving (widget, admin)

---

## Phase 8: Testing & Documentation

### 8.1 Testing
- [x] Unit tests — domain entities (21 tests)
- [x] Unit tests — use cases with mocked repos (15 tests)
- [x] Integration tests — repos against real PostgreSQL (22 tests)
- [x] Integration tests — REST endpoints via httpx (14 tests)
- [ ] E2E tests — multi-turn conversations, escalation flows

### 8.2 Documentation & Delivery
- [x] README with setup instructions
- [x] Write-up (half page to one page)
- [ ] Demo script tested end-to-end

---

## Phase 9: Integrations & User Setup

### 9.1 SendGrid Email Integration
- [ ] Create SendGrid account and get API key
- [ ] Verify sender email address
- [ ] Add `SENDGRID_API_KEY` and `SENDGRID_FROM_EMAIL` to `.env`
- [ ] Test escalation email sending (live)

### 9.2 Real Users
- [ ] Create real users with actual email addresses (migration or admin endpoint)
- [ ] Test login with real user accounts

### 9.3 Admin Dashboard Notifications
- [ ] Browser push notifications for new escalations
- [ ] Live badge counter on Escalations nav item (WebSocket or polling)
- [ ] Optional: notification sound on new escalation

---

## Phase 10: Production Readiness

### 10.1 Deployment
- [ ] Choose platform (Railway / Render / Fly.io)
- [ ] Managed PostgreSQL setup
- [ ] Environment variables configured (secrets, API keys)
- [ ] Google `credentials.json` → base64-encoded env var
- [ ] HTTPS / SSL
- [ ] Domain name (optional)

### 10.2 Desktop App Embedding
- [ ] Research how target macOS practice software handles plugins / help panels
- [ ] WKWebView approach: create stripped-down widget page for embedding
- [ ] Test WebSocket connection from WKWebView context
- [ ] Alternative: standalone Electron/Tauri wrapper if web view not available

### 10.3 Session Management
- [ ] Auto-close sessions after inactivity (30 min timeout)
- [ ] Session close cleanup (update status, finalize metadata)

### 10.4 Rate Limiting
- [ ] Rate limit WebSocket messages (per session, per IP)
- [ ] Rate limit REST API endpoints
- [ ] Graceful error messages when rate limited

### 10.5 Prompt Caching
- [ ] Enable Anthropic prompt caching for system prompt + tool definitions
- [ ] Measure cost reduction

---

## Phase 11: Future Enhancements

### 11.1 Search Quality
- [ ] Test edge case queries and measure recall
- [ ] Query expansion / fallback to broader search
- [ ] Consider pgvector for semantic search alongside tsvector

### 11.2 Multi-Language Support
- [ ] Agent responds in user's language (prompt instruction)
- [ ] Spanish knowledge base articles (priority for target market)
- [ ] Language detection and routing

### 11.3 Audit Log
- [ ] Log all article changes (who, when, what)
- [ ] Log all escalation status changes
- [ ] Log all user access to patient-related data
- [ ] Admin view for audit log

### 11.4 Multi-Agent Architecture
- [ ] Separate billing, scheduling, and technical agents
- [ ] Router agent for intent classification
- [ ] Per-agent guardrails and safety rules

### 11.5 Voice Channel
- [ ] Twilio integration for phone-based support
- [ ] Deepgram for speech-to-text
- [ ] TTS for agent responses

### 11.6 Analytics Improvements
- [ ] Knowledge gap detection (topics that trigger most escalations)
- [ ] Surface gap reports to admins as content priorities
- [ ] Cost tracking dashboard (daily/weekly/monthly spend)
- [ ] User satisfaction tracking (post-conversation rating)
