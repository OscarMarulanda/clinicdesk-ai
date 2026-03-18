-- ClinicDesk AI — Initial Schema
-- Migration 001: Create all tables, indexes, and triggers

-- Users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'staff',
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Knowledge Articles
CREATE TABLE IF NOT EXISTS knowledge_articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    slug VARCHAR(500) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    search_vector TSVECTOR,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_articles_search_vector
    ON knowledge_articles USING GIN (search_vector);

CREATE INDEX IF NOT EXISTS idx_articles_category
    ON knowledge_articles (category);

-- Auto-update search_vector on insert/update
CREATE OR REPLACE FUNCTION update_search_vector() RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.content, '')), 'B');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_articles_search_vector ON knowledge_articles;
CREATE TRIGGER trg_articles_search_vector
    BEFORE INSERT OR UPDATE OF title, content ON knowledge_articles
    FOR EACH ROW EXECUTE FUNCTION update_search_vector();

-- Sessions
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    channel VARCHAR(20) NOT NULL DEFAULT 'chat',
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    context JSONB NOT NULL DEFAULT '{}',
    messages JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions (user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions (status);
CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON sessions (created_at);

-- Escalations
CREATE TABLE IF NOT EXISTS escalations (
    id SERIAL PRIMARY KEY,
    session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    reason VARCHAR(100) NOT NULL,
    summary TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    assigned_to VARCHAR(255),
    calendar_event_id VARCHAR(255),
    email_sent_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_escalations_session_id ON escalations (session_id);
CREATE INDEX IF NOT EXISTS idx_escalations_status ON escalations (status);

-- Providers (support reps for escalation routing)
CREATE TABLE IF NOT EXISTS providers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    calendar_id VARCHAR(255),
    is_available BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
