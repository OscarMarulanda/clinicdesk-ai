# ADR-007: Hybrid Agent + Workflow Architecture

## Status
Proposed

## Context
The current system (ADR-004) uses a pure agent pattern: a single Claude instance in a tool loop makes all decisions autonomously. This works well for open-ended conversations (KB search, follow-up questions), but some sub-tasks — particularly callback booking and escalation — are deterministic multi-step sequences that the agent must execute in a strict order.

Today we enforce ordering through two mechanisms:
1. **System prompt instructions** — a mandatory step-by-step sequence for callback booking
2. **Backend validation** — `escalate_to_human` rejects if `check_availability` wasn't called first

This is a workflow encoded as prompt engineering. It works, but it's fragile: the LLM can still attempt steps out of order, and the backend must catch and reject those attempts. Every guardrail we add is compensating for giving the LLM control over a flow it shouldn't control.

Anthropic's [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) guide distinguishes:
- **Workflows**: LLMs and tools orchestrated through predefined code paths — predictable, consistent
- **Agents**: LLMs dynamically direct their own processes and tool usage — flexible, open-ended

Their recommendation: use agents for open-ended problems, workflows for well-defined tasks. Most real systems benefit from combining both.

## Decision (Proposed)
Evolve from a pure agent to a **hybrid architecture**: agent at the outer conversational layer, with workflow sub-routines for deterministic flows.

## Design

### Current Architecture (Pure Agent)
```
User message → Claude (tool loop, up to 10 rounds) → Response
                  ↕
            All 6 tools available
            Claude decides everything
```

### Proposed Architecture (Hybrid)
```
User message
    ↓
┌─ Agent (outer loop, conversational) ──────────────────┐
│                                                        │
│  Claude decides what to do:                            │
│    • Answer from KB     → stays in agent loop          │
│    • Callback requested → hands off to CALLBACK        │
│                           WORKFLOW (code-controlled)    │
│    • Needs escalation   → hands off to ESCALATION      │
│                           WORKFLOW (code-controlled)    │
│    • Simple reply        → responds directly            │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Component 1: Intent-Aware Agent Loop

The agent loop remains the primary interface. Claude still decides *what* to do, but for certain intents it signals a handoff rather than executing the flow itself. This can be implemented two ways:

**Option A — Tool-based handoff**: Add a `start_callback_flow` tool that the agent calls instead of directly calling `check_availability`. This triggers the workflow, which takes over the conversation until complete.

**Option B — Detection in code**: After each agent response, inspect tool calls. If `check_availability` is called, transition into the callback workflow for subsequent turns. No new tools needed.

Option B is simpler and backward-compatible.

### Component 2: Callback Booking Workflow (Prompt Chaining)

A deterministic, code-controlled sequence:

```
Step 1: Agent calls check_availability(preferred_time)
        → Code detects this, enters workflow mode

Step 2: Code formats available slots, sends to user
        → No LLM call needed (template response)

Step 3: User picks a slot
        → Code validates selection against pending_slots
        → No LLM call needed

Step 4: Code calls escalate_to_human(confirmed_time=chosen_slot)
        → Deterministic, no LLM decision

Step 5: Code generates confirmation message
        → Single LLM call to write a natural confirmation
        → Exits workflow mode, returns to agent loop
```

**What this eliminates:**
- System prompt's mandatory sequence instructions (the code enforces it)
- Backend validation of `pending_slots` existence (the code guarantees ordering)
- Risk of the agent calling tools out of order
- 2-3 unnecessary LLM round-trips per booking (currently: check → present → confirm → escalate → respond = up to 5 agent loop iterations; proposed: 2 LLM calls max)

### Component 3: Escalation Workflow (Simpler Case)

For non-callback escalations (no calendar booking), the flow is already mostly atomic thanks to the fused `escalate_to_human` tool (ADR-006). The improvement here is minor:

```
Agent decides to escalate
    → Code calls escalate_to_human with collected context
    → Single LLM call to write empathetic handoff message
```

This is close to what happens today, so the ROI of formalizing it as a workflow is lower.

### Optional: Routing Layer

A lightweight classifier before the agent loop:

```python
async def classify_intent(message: str, history: list) -> str:
    """Fast classification — could use haiku for cost savings."""
    # Returns: "faq", "callback", "escalation", "chitchat"
```

**Benefits:**
- Skip tool loop entirely for greetings/chitchat (save ~$0.003/turn)
- Pre-load relevant KB articles for FAQ intent (reduce tool rounds)
- Enter callback workflow directly if intent is clear

**Tradeoff:** Adds latency for an extra LLM call on every message. May not be worth it unless the volume justifies cost savings. A simpler alternative: keyword/pattern detection for obvious cases ("schedule a callback", "book a call"), LLM classification only when ambiguous.

## Impact on Current Codebase

### Files to Modify
- `src/application/use_cases/process_chat_message.py` — Add workflow state machine alongside agent loop
- `src/infrastructure/ai/system_prompt.py` — Remove mandatory callback sequence instructions (code handles it)
- `src/infrastructure/ai/tools.py` — Possibly add `start_callback_flow` tool (Option A only)

### Files Unchanged
- `src/infrastructure/calendar/google_calendar_service.py` — Same service, called by workflow instead of agent
- `src/infrastructure/email/sendgrid_service.py` — Same
- `src/presentation/ws/chat.py` — Same WebSocket interface
- All domain entities and repository interfaces — Same

### Migration Path
1. Add workflow mode flag to session context (`workflow: null | "callback" | "escalation"`)
2. In the agent loop, detect `check_availability` tool call → set `workflow: "callback"`
3. On subsequent messages, if `workflow == "callback"`, run workflow steps instead of agent loop
4. On workflow completion or timeout, clear workflow flag → return to agent mode

This is backward-compatible: if no workflow is triggered, behavior is identical to today.

## Rationale

| Aspect | Pure Agent (current) | Hybrid (proposed) |
|---|---|---|
| KB search/Q&A | Agent decides (good) | Agent decides (same) |
| Callback booking | Agent decides, prompt + code guard ordering (fragile) | Code controls ordering (reliable) |
| Escalation | Agent decides, fused tool (good) | Workflow formalizes it (marginal gain) |
| Cost per callback | ~5 LLM rounds | ~2 LLM calls |
| Guardrail complexity | System prompt rules + backend validation | Code enforces sequence |
| Flexibility | Maximum | Slightly less for workflow flows |
| Testability | Must test LLM behavior | Workflow steps are unit-testable |

## Trade-offs
- **Added complexity**: Workflow state machine adds code paths to `process_chat_message`
- **Reduced flexibility**: Callback flow can't adapt if user changes their mind mid-workflow (needs explicit "cancel" handling)
- **Two mental models**: Developers must understand both the agent loop and workflow mode
- **Marginal gain for escalation**: The fused tool already handles non-callback escalations well

## When to Implement
This becomes worthwhile when:
- Callback booking volume is high enough that reliability and cost matter
- New deterministic flows are added (e.g., account setup wizard, guided troubleshooting)
- The system prompt is getting too long with behavioral rules that should be code

For a demo/interview context, the current pure agent architecture is clean and defensible. The value is in being able to articulate *why* you'd make this change and *when*.
