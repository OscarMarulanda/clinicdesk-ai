# ClinicDesk AI — Agent Design Document

## Overview

The agent is a single Claude-powered conversational AI with tool calling capabilities. It helps clinic staff navigate practice management software by searching a knowledge base, walking users through procedures step-by-step, and escalating to human support when needed.

## Architecture Decision

**Single agent with tools** (not multi-agent). Rationale:
- Simpler — no routing logic, no inter-agent communication
- Sufficient for current scope — one domain (practice management software support)
- All behavior controlled via system prompt and tool availability
- Multi-agent would make sense at scale when billing, scheduling, and clinical triage need separate guardrails

## Model

- **Primary**: `claude-sonnet-4-20250514` (Claude Sonnet 4)
- **Upgrade path**: Can swap to Sonnet 4.5/4.6 by changing model ID — no code changes needed
- Tool calling is built-in to all Claude 4 models

## System Prompt

```
You are a customer support agent for ClinicDesk, a practice management software used by dental and medical clinics.

Your users are clinic staff: office managers, front desk coordinators, billing coordinators, and clinic owners. They are busy professionals in the middle of their workday who need quick, accurate help.

## Your capabilities
- Search the knowledge base to answer questions about ClinicDesk features and workflows
- Walk users through multi-step procedures one step at a time
- Escalate to a human support representative when needed
- Schedule callbacks and send notifications to the support team

## How to behave
- Be warm but efficient — friendly, not chatty
- Be concise and practical — these people don't have time for long explanations
- Always search the knowledge base before saying you don't know something
- For multi-step procedures, walk through one step at a time — confirm the user completed each step before moving on
- Use specific menu paths and button names when giving instructions (e.g., "Go to Patient → Insurance → Plan Details")
- If you find relevant information but aren't fully confident, say what you found and offer to escalate

## When to escalate
You MUST escalate to a human when:
- The knowledge base doesn't cover the user's question and you can't answer confidently
- The user expresses frustration or explicitly asks to speak with someone
- The question is about clinical/medical advice, legal matters, or compliance
- The issue involves billing disputes, refunds, or overcharges
- The user wants to change their plan (upgrade, downgrade, cancel)

When escalating:
1. Acknowledge the situation empathetically
2. Briefly explain why you're escalating
3. Ask the user if they'd prefer a scheduled callback or an email to the support team
4. Collect the necessary information (email, preferred time)
5. Use the appropriate tools to create the escalation

## What you must NOT do
- Never give medical, legal, or financial advice
- Never guess at procedures you're not sure about — escalate instead
- Never share information about other users or clinics
- Never make promises about pricing, refunds, or policy changes
- Never try to handle account cancellations yourself — always escalate
```

## Tools

### 1. search_knowledge_base

Searches the knowledge base using full-text search.

```json
{
  "name": "search_knowledge_base",
  "description": "Search the ClinicDesk knowledge base for articles matching the user's question. Always use this before saying you don't have information on a topic.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search query — use keywords from the user's question"
      },
      "category": {
        "type": "string",
        "enum": ["scheduling", "billing_coding", "insurance_claims", "patient_records", "reporting_analytics", "technical_troubleshooting", "account_plans"],
        "description": "Optional category filter to narrow results"
      }
    },
    "required": ["query"]
  }
}
```

### 2. get_article

Retrieves the full content of a specific article.

```json
{
  "name": "get_article",
  "description": "Get the full content of a knowledge base article by ID. Use this when search results show a relevant article and you need the complete details.",
  "input_schema": {
    "type": "object",
    "properties": {
      "article_id": {
        "type": "integer",
        "description": "The article ID from search results"
      }
    },
    "required": ["article_id"]
  }
}
```

### 3. escalate_to_human

Creates an escalation record and initiates handoff.

```json
{
  "name": "escalate_to_human",
  "description": "Escalate the conversation to a human support representative. Use this when you cannot confidently resolve the issue, the user is frustrated, or the issue is out of scope.",
  "input_schema": {
    "type": "object",
    "properties": {
      "reason": {
        "type": "string",
        "enum": ["knowledge_gap", "user_frustration", "out_of_scope", "billing_dispute", "account_change"],
        "description": "Why this conversation needs human intervention"
      },
      "summary": {
        "type": "string",
        "description": "A concise summary of the issue and what has been attempted so far"
      },
      "preferred_action": {
        "type": "string",
        "enum": ["calendar", "email", "both"],
        "description": "How to notify the support team — based on user preference"
      }
    },
    "required": ["reason", "summary", "preferred_action"]
  }
}
```

### 4. schedule_callback

Creates a Google Calendar event for a support callback.

```json
{
  "name": "schedule_callback",
  "description": "Schedule a callback meeting between the user and a support representative via Google Calendar.",
  "input_schema": {
    "type": "object",
    "properties": {
      "user_email": {
        "type": "string",
        "description": "The user's email address for the calendar invite"
      },
      "preferred_time": {
        "type": "string",
        "description": "The user's preferred callback time (e.g., 'today after 2pm', 'tomorrow morning')"
      },
      "issue_summary": {
        "type": "string",
        "description": "Brief description of the issue for the calendar event description"
      }
    },
    "required": ["user_email", "preferred_time", "issue_summary"]
  }
}
```

### 5. send_escalation_email

Sends an email notification to the support team.

```json
{
  "name": "send_escalation_email",
  "description": "Send an email to the support team with a summary of the conversation and the user's issue.",
  "input_schema": {
    "type": "object",
    "properties": {
      "to_email": {
        "type": "string",
        "description": "Support team email address"
      },
      "subject": {
        "type": "string",
        "description": "Email subject line"
      },
      "conversation_summary": {
        "type": "string",
        "description": "Summary of the conversation including what was discussed and what the user needs"
      }
    },
    "required": ["to_email", "subject", "conversation_summary"]
  }
}
```

### 6. update_session_notes

Updates the agent's internal scratchpad for context tracking.

```json
{
  "name": "update_session_notes",
  "description": "Update your internal notes about this conversation. Use this to track what has been discussed, what was resolved, and any important context for follow-up.",
  "input_schema": {
    "type": "object",
    "properties": {
      "notes": {
        "type": "string",
        "description": "Updated notes about the conversation"
      }
    },
    "required": ["notes"]
  }
}
```

### 7. get_user_info

Returns user profile and plan information.

```json
{
  "name": "get_user_info",
  "description": "Get the user's profile and subscription plan information. Use this to personalize support and check what features are available on their plan.",
  "input_schema": {
    "type": "object",
    "properties": {
      "user_id": {
        "type": "string",
        "description": "The user's ID"
      }
    },
    "required": ["user_id"]
  }
}
```

### 8. list_categories

Returns available knowledge base categories.

```json
{
  "name": "list_categories",
  "description": "List all available knowledge base categories. Use this when the user wants to browse topics or when you want to suggest related categories.",
  "input_schema": {
    "type": "object",
    "properties": {},
    "required": []
  }
}
```

## Conversation Flow Patterns

### Pattern 1: Direct Answer
```
User asks question → search KB → find article → answer from article
```

### Pattern 2: Multi-Step Walkthrough
```
User asks how to do X → search KB → find procedure article
→ give step 1 → wait for confirmation
→ give step 2 → wait for confirmation
→ ... → completion → update session notes
```

### Pattern 3: Search + Navigate
```
User asks question → search KB → article references a screen
→ user doesn't know how to get there → search KB for navigation
→ guide to the screen → continue with original answer
```

### Pattern 4: Escalation
```
User has issue → search KB → no confident answer OR frustration detected
→ explain escalation → ask preference (callback/email)
→ collect info → schedule_callback and/or send_escalation_email
→ escalate_to_human → confirm to user
```

### Pattern 5: Out of Scope
```
User asks medical/legal/financial question
→ politely decline → explain it's outside scope
→ offer to escalate to appropriate team
```

## Escalation Triggers

| Trigger | Detection Method |
|---------|-----------------|
| Knowledge gap | Search returns no results or low-relevance results |
| User frustration | Repeated questions, "this isn't working", explicit ask for human |
| Out of scope | Medical/legal/financial advice requests |
| Billing dispute | Mentions of refunds, overcharges, disputed amounts |
| Account change | Mentions of upgrading, downgrading, cancelling |

## Prompt Iteration Notes

_This section will be updated as we test and tune the system prompt._

| Date | Change | Reason |
|------|--------|--------|
| — | Initial prompt | Baseline |
