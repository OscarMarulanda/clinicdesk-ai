# ADR-002: asyncpg Over ORM (SQLAlchemy)

## Status
Accepted

## Context
Need a database access strategy for PostgreSQL. Options considered:
1. **SQLAlchemy** (async) — full ORM with query builder, migrations (Alembic), model definitions
2. **asyncpg** (raw) — direct async PostgreSQL driver, raw SQL queries

## Decision
Use asyncpg with raw SQL queries behind repository interfaces.

## Rationale
- **Performance**: asyncpg is the fastest Python PostgreSQL driver — purpose-built for async
- **Simplicity**: No ORM model definitions to maintain alongside domain entities (avoids duplication in Clean Architecture)
- **Control**: Full control over SQL, especially for PostgreSQL-specific features (tsvector, JSONB, triggers)
- **Clean Architecture fit**: Repository implementations are already abstracted behind interfaces — the ORM's abstraction layer would be redundant
- **Less dependency surface**: asyncpg is a single, focused library vs SQLAlchemy's large dependency tree

## Trade-offs
- Must write SQL manually (acceptable — queries are straightforward CRUD + full-text search)
- No auto-generated migrations (using numbered SQL files instead)
- Must handle connection pooling manually (asyncpg provides pool API)

## Migration Strategy
Numbered SQL files in `migrations/` directory, executed by a simple runner script. Each migration is idempotent.
