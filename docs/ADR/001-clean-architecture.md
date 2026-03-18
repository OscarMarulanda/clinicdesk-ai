# ADR-001: Clean Architecture for Backend

## Status
Accepted

## Context
Need to choose a backend architecture pattern for the ClinicDesk AI support agent. Options considered:
1. **Layered architecture** (routes → services → repositories) — simpler, fewer files
2. **Clean Architecture** (domain → application → infrastructure → presentation) — more abstractions, dependency inversion

## Decision
Use Clean Architecture with strict dependency inversion.

## Rationale
- **Testability**: Domain and use cases can be tested without any infrastructure (no DB, no API calls)
- **Framework independence**: Domain layer has zero knowledge of FastAPI, asyncpg, or Claude SDK — we could swap any of these without touching business logic
- **Swappable infrastructure**: Repository and service interfaces allow easy substitution (e.g., swap asyncpg for SQLAlchemy, or Claude for another LLM provider)
- **Explicit boundaries**: Each layer has a clear responsibility, making the codebase navigable for any developer familiar with the pattern

## Trade-offs
- More files and abstractions than a simple layered approach
- Slightly more boilerplate (ABC definitions, dependency injection wiring)
- Overkill for a throwaway prototype, but appropriate for a demo that should demonstrate architectural thinking

## Structure
```
src/
├── domain/          # Entities, repository ABCs, exceptions — no external deps
├── application/     # Use cases, DTOs, service interface ABCs
├── infrastructure/  # Concrete implementations (asyncpg, Claude, SendGrid, Google Calendar)
├── presentation/    # FastAPI routes, WebSocket handlers, middleware
└── main.py          # Composition root
```
