# ADR-004: Single Agent with Tools Over Multi-Agent

## Status
Accepted

## Context
Need to decide the AI agent architecture. Options considered:
1. **Single agent** with multiple tools — one Claude instance handles all support topics
2. **Multi-agent** with router — specialized agents for billing, scheduling, technical issues, etc.

## Decision
Use a single agent with tool calling.

## Rationale
- **Simplicity**: No routing logic, no inter-agent communication, no context passing between agents
- **Sufficient scope**: All support topics are within the same domain (practice management software) — one system prompt can cover the behavioral guidelines
- **Tool-based specialization**: Different tools (search KB, escalate, schedule) provide the specialization without separate agents
- **Lower latency**: One API call per turn instead of router + specialist
- **Lower cost**: No routing overhead

## Trade-offs
- System prompt gets longer as capabilities grow — manageable at current scope
- Can't have different guardrails per topic area (e.g., stricter rules for billing vs scheduling) — mitigated by escalation triggers
- Single context window for everything — not a problem at article/conversation scale

## Upgrade Path
Multi-agent makes sense when:
- Billing, scheduling, and clinical triage need different safety guardrails
- The knowledge base grows large enough that specialized agents with filtered search improve accuracy
- Different topics need different models (e.g., cheaper model for FAQ, stronger model for troubleshooting)
