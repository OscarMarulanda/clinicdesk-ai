# ClinicDesk AI — Database Schema

## Overview

PostgreSQL database accessed exclusively through the repository layer via asyncpg. No ORM — all queries are raw SQL for performance and control.

## Tables

### users

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | SERIAL | PRIMARY KEY | |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Login identifier |
| name | VARCHAR(255) | NOT NULL | Display name |
| role | VARCHAR(20) | NOT NULL, DEFAULT 'staff' | 'staff' or 'admin' |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt or argon2 |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

### knowledge_articles

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | SERIAL | PRIMARY KEY | |
| title | VARCHAR(500) | NOT NULL | Article title |
| slug | VARCHAR(500) | UNIQUE, NOT NULL | URL-friendly identifier |
| category | VARCHAR(50) | NOT NULL | See category enum below |
| content | TEXT | NOT NULL | Markdown content |
| search_vector | TSVECTOR | | Auto-updated from title + content |
| created_by | INTEGER | FK → users(id), NULL | Author (nullable for seed data) |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

**Indexes:**
- `idx_articles_search_vector` — GIN index on `search_vector` (full-text search)
- `idx_articles_category` — B-tree on `category` (filter queries)
- `idx_articles_slug` — unique index on `slug`

**Trigger:** Auto-update `search_vector` on INSERT/UPDATE using `to_tsvector('english', title || ' ' || content)`

**Categories (enforced at application level):**
- `scheduling`
- `billing_coding`
- `insurance_claims`
- `patient_records`
- `reporting_analytics`
- `technical_troubleshooting`
- `account_plans`

### sessions

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Externally-facing ID |
| user_id | INTEGER | FK → users(id), NULL | Nullable for anonymous widget users |
| channel | VARCHAR(20) | NOT NULL, DEFAULT 'chat' | 'chat' (extensible) |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'active' | 'active' or 'closed' |
| context | JSONB | DEFAULT '{}' | Agent notepad / scratchpad |
| messages | JSONB | DEFAULT '[]' | Array of message objects |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| metadata | JSONB | DEFAULT '{}' | Token counts, timing, etc. |

**Indexes:**
- `idx_sessions_user_id` — B-tree on `user_id`
- `idx_sessions_status` — B-tree on `status`
- `idx_sessions_created_at` — B-tree on `created_at` (for listing/sorting)

**Message object shape (in JSONB array):**
```json
{
  "role": "user" | "assistant",
  "content": "message text",
  "timestamp": "2026-03-17T10:30:00Z",
  "tool_calls": [...] | null,
  "token_count": 150
}
```

### escalations

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | SERIAL | PRIMARY KEY | |
| session_id | UUID | FK → sessions(id), NOT NULL | Which conversation triggered this |
| reason | VARCHAR(100) | NOT NULL | Category of escalation trigger |
| summary | TEXT | NOT NULL | Agent-generated issue summary |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | 'pending', 'in_progress', 'resolved' |
| assigned_to | VARCHAR(255) | NULL | Support rep email |
| calendar_event_id | VARCHAR(255) | NULL | Google Calendar event ID |
| email_sent_at | TIMESTAMPTZ | NULL | When notification was sent |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |
| resolved_at | TIMESTAMPTZ | NULL | When marked resolved |

**Indexes:**
- `idx_escalations_session_id` — B-tree on `session_id`
- `idx_escalations_status` — B-tree on `status`

**Escalation reasons:**
- `knowledge_gap` — question not covered in KB
- `user_frustration` — user expressing frustration
- `out_of_scope` — clinical/medical/legal question
- `billing_dispute` — refunds, overcharges, financial disagreements
- `account_change` — plan upgrades, downgrades, cancellations

### providers

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | SERIAL | PRIMARY KEY | |
| name | VARCHAR(255) | NOT NULL | Support rep name |
| email | VARCHAR(255) | UNIQUE, NOT NULL | For calendar invites and assignments |
| calendar_id | VARCHAR(255) | NULL | Google Calendar ID |
| is_available | BOOLEAN | NOT NULL, DEFAULT true | Availability for routing |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

### notifications

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | SERIAL | PRIMARY KEY | |
| type | VARCHAR(50) | NOT NULL, DEFAULT 'escalation' | Notification type |
| title | VARCHAR(500) | NOT NULL | Short title |
| message | TEXT | NOT NULL | Notification body |
| reference_id | INTEGER | NULL | ID of referenced entity |
| reference_type | VARCHAR(50) | NULL | Entity type ('escalation') |
| is_read | BOOLEAN | NOT NULL, DEFAULT false | Read status |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | |

**Indexes:**
- `idx_notifications_is_read` — B-tree on `is_read`
- `idx_notifications_created_at` — B-tree on `created_at`

## Migrations

Located in `migrations/` directory. Numbered sequentially.

| File | Purpose |
|------|---------|
| `001_initial.sql` | Create all tables, indexes, triggers |
| `002_seed_knowledge_base.sql` | Insert all knowledge base articles |
| `003_seed_users_providers.sql` | Insert demo users and providers |
| `004_real_users.sql` | Real user accounts |
| `005_notifications.sql` | Notifications table for admin dashboard |

All migrations must be idempotent — use `CREATE TABLE IF NOT EXISTS`, `CREATE INDEX IF NOT EXISTS`, `INSERT ... ON CONFLICT DO NOTHING` where appropriate.

## Full-Text Search

Knowledge base search uses PostgreSQL's built-in full-text search:

```sql
-- Search query
SELECT id, title, category, content,
       ts_rank(search_vector, query) AS rank
FROM knowledge_articles, plainto_tsquery('english', $1) query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 5;
```

Optional category filter:
```sql
AND category = $2
```

The `search_vector` column is automatically maintained by a trigger that concatenates `title` (weight A) and `content` (weight B):

```sql
CREATE FUNCTION update_search_vector() RETURNS TRIGGER AS $$
BEGIN
  NEW.search_vector :=
    setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
    setweight(to_tsvector('english', COALESCE(NEW.content, '')), 'B');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

## Entity Relationship Diagram

```
users 1──────────────────┐
  │                      │
  │ 1:N                  │ 1:N (created_by)
  │                      │
  ▼                      ▼
sessions            knowledge_articles
  │
  │ 1:N
  │
  ▼
escalations ──── notifications (reference_id → escalation.id)

providers (standalone — used for escalation routing)
```
