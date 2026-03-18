# ADR-003: PostgreSQL Full-Text Search Over Vector Embeddings

## Status
Accepted

## Context
The knowledge base needs a search mechanism. Options considered:
1. **PostgreSQL tsvector/tsquery** — built-in full-text search with ranking
2. **Vector embeddings** (pgvector or external) — semantic search using embeddings
3. **External search service** (Elasticsearch, Meilisearch) — dedicated search infrastructure

## Decision
Use PostgreSQL's built-in full-text search with tsvector/tsquery and GIN index.

## Rationale
- **No external dependencies**: Everything runs in the same PostgreSQL instance
- **Sufficient for structured content**: Knowledge base articles are well-titled, categorized, and written in clear language — keyword-based search with ranking works well
- **Fast to implement**: GIN index + tsvector trigger is a few lines of SQL
- **Weighted search**: Can weight title matches higher than body matches using `setweight()`
- **Category filtering**: Combines naturally with SQL WHERE clauses

## Trade-offs
- Less semantic understanding than vector search (won't find "how do I bill someone" when the article says "submitting a claim") — mitigated by good article titles and the agent's ability to rephrase queries
- No fuzzy matching — mitigated by tsquery's stemming and the agent trying multiple search queries

## Upgrade Path
If search quality proves insufficient, add pgvector for semantic search alongside tsvector. Both can coexist — use tsvector for keyword matches and vector similarity for semantic fallback.
