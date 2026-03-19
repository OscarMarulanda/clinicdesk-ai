# ClinicDesk AI — Setup & Development Guide

## Prerequisites

- Python 3.13+
- PostgreSQL 16+
- A Google Cloud project with Calendar API enabled (for escalation callbacks)
- A SendGrid account (for escalation emails)
- An Anthropic API key (for Claude AI agent)

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.135.1 | Web framework |
| uvicorn | 0.42.0 | ASGI server |
| asyncpg | 0.31.0 | PostgreSQL async driver |
| pydantic | 2.12.5 | Data validation |
| pydantic-settings | 2.13.1 | Settings management |
| anthropic | 0.85.0 | Claude API SDK |
| sendgrid | 6.12.5 | Email sending |
| google-api-python-client | >= 2.160.0 | Google Calendar API |
| google-auth-oauthlib | >= 1.2.1 | Google OAuth |
| google-auth-httplib2 | >= 0.2.0 | Google auth transport |
| python-dotenv | >= 1.1.0 | Environment variable loading |
| python-multipart | >= 0.0.20 | File upload support |
| bcrypt | 5.0.0 | Password hashing |
| PyJWT | 2.12.1 | JWT tokens |
| pymupdf | >= 1.25.0 | PDF text extraction |
| python-docx | >= 1.1.0 | DOCX text extraction |

## Environment Variables

Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Required variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/clinicdesk

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# SendGrid
SENDGRID_API_KEY=SG....
SENDGRID_FROM_EMAIL=support@clinicdesk.com

# Google Calendar
GOOGLE_CREDENTIALS_PATH=./credentials.json
GOOGLE_CALENDAR_ID=primary

# App
APP_SECRET_KEY=your-secret-key-here
APP_ENV=development
APP_PORT=8000
```

## Local Setup

### 1. Database

**Option A: Docker Compose (recommended)**
```bash
docker-compose up -d postgres
```

**Option B: Local PostgreSQL**
```bash
createdb clinicdesk
```

### 2. Run Migrations

```bash
make migrate
```

Or manually:
```bash
psql $DATABASE_URL -f migrations/001_initial.sql
psql $DATABASE_URL -f migrations/002_seed_knowledge_base.sql
psql $DATABASE_URL -f migrations/003_seed_users_providers.sql
```

### 3. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the Server

```bash
make run
```

Or:
```bash
uvicorn src.main:app --reload --port 8000
```

### 5. Access

- **Chat widget demo**: http://localhost:8000/static/widget/demo.html
- **Admin dashboard**: http://localhost:8000/static/admin/index.html
- **API docs (auto-generated)**: http://localhost:8000/docs

## Google Calendar Setup

1. Create a Google Cloud project
2. Enable the Google Calendar API
3. Create a service account (or OAuth credentials for demo)
4. Download `credentials.json` and place in project root
5. Share your Google Calendar with the service account email

## SendGrid Setup

1. Create a SendGrid account
2. Create an API key with Mail Send permissions
3. Verify a sender identity (email address)
4. Set the API key and sender email in `.env`

## Makefile Commands

_Will be documented as commands are created._

```makefile
make run        # Start development server
make migrate    # Run all migrations
make seed       # Seed knowledge base and demo data
make test       # Run tests
```

## Deployment (Fly.io + Supabase)

### Production Setup

1. Install Fly CLI: `brew install flyctl`
2. Authenticate: `fly auth login`
3. Create app: `fly launch --no-deploy --name clinicdesk-ai --region sjc`
4. Set secrets:
```bash
fly secrets set \
  DATABASE_URL="postgresql://postgres.PROJECT_REF:PASSWORD@aws-0-REGION.pooler.supabase.com:5432/postgres" \
  ANTHROPIC_API_KEY="sk-ant-..." \
  SENDGRID_API_KEY="SG...." \
  APP_SECRET_KEY="$(openssl rand -hex 32)" \
  GOOGLE_CREDENTIALS_JSON="$(cat credentials.json)"
```
5. Deploy: `fly deploy`

### Notes
- The Dockerfile writes `GOOGLE_CREDENTIALS_JSON` to a file at startup
- Migrations run automatically on each deploy
- SSL is enabled for database connections in production (`APP_ENV=production`)
- Supabase Session Pooler requires `statement_cache_size=0` (configured automatically)
