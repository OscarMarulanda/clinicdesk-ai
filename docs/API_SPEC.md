# ClinicDesk AI — API Specification

## Base URL

```
http://localhost:8000
```

## Authentication

Simple auth via API key header or session token (for demo purposes):

```
Authorization: Bearer <token>
```

---

## WebSocket — Chat

### `WS /ws/chat`

Bidirectional WebSocket for real-time chat with the AI agent.

**Query params:**
- `session_id` (optional) — resume existing session
- `user_id` (optional) — associate with authenticated user

**Client → Server message:**
```json
{
  "type": "message",
  "content": "How do I submit a pre-authorization?"
}
```

**Server → Client messages:**

*Typing indicator:*
```json
{
  "type": "typing",
  "status": true
}
```

*Agent response:*
```json
{
  "type": "message",
  "content": "To submit a pre-authorization, follow these steps...",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

*Error:*
```json
{
  "type": "error",
  "message": "Something went wrong. Please try again."
}
```

---

## REST API — Admin

All admin endpoints require `Authorization` header and `admin` role.

### Knowledge Base Articles

#### `GET /api/admin/articles`

List articles with optional search and category filter.

**Query params:**
- `q` (string, optional) — full-text search query
- `category` (string, optional) — filter by category
- `page` (int, default 1) — pagination
- `per_page` (int, default 20) — items per page

**Response: `200 OK`**
```json
{
  "articles": [
    {
      "id": 1,
      "title": "How to Book a New Appointment",
      "slug": "how-to-book-new-appointment",
      "category": "scheduling",
      "updated_at": "2026-03-17T10:00:00Z",
      "created_at": "2026-03-17T10:00:00Z"
    }
  ],
  "total": 67,
  "page": 1,
  "per_page": 20
}
```

#### `POST /api/admin/articles`

Create a new article.

**Request body:**
```json
{
  "title": "How to Set Up Telehealth",
  "category": "technical_troubleshooting",
  "content": "## Overview\n\nTo set up the telehealth module..."
}
```

**Response: `201 Created`**
```json
{
  "id": 68,
  "title": "How to Set Up Telehealth",
  "slug": "how-to-set-up-telehealth",
  "category": "technical_troubleshooting",
  "content": "## Overview\n\nTo set up the telehealth module...",
  "created_by": 1,
  "updated_at": "2026-03-17T14:30:00Z",
  "created_at": "2026-03-17T14:30:00Z"
}
```

#### `GET /api/admin/articles/{id}`

Get full article by ID.

**Response: `200 OK`** — full article object (same shape as create response)

#### `PUT /api/admin/articles/{id}`

Update an article.

**Request body:**
```json
{
  "title": "Updated Title",
  "category": "scheduling",
  "content": "Updated content..."
}
```

**Response: `200 OK`** — updated article object

#### `DELETE /api/admin/articles/{id}`

Delete an article.

**Response: `204 No Content`**

---

### Sessions

#### `GET /api/admin/sessions`

List all chat sessions.

**Query params:**
- `status` (string, optional) — `active` or `closed`
- `page` (int, default 1)
- `per_page` (int, default 20)

**Response: `200 OK`**
```json
{
  "sessions": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "user_id": 1,
      "user_name": "Maria Garcia",
      "status": "closed",
      "message_count": 12,
      "created_at": "2026-03-17T09:00:00Z",
      "updated_at": "2026-03-17T09:15:00Z"
    }
  ],
  "total": 45,
  "page": 1,
  "per_page": 20
}
```

#### `GET /api/admin/sessions/{id}`

Get session with full message transcript.

**Response: `200 OK`**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": 1,
  "user_name": "Maria Garcia",
  "status": "closed",
  "context": { "notes": "Resolved CDT code mismatch" },
  "messages": [
    {
      "role": "user",
      "content": "How do I submit a pre-authorization?",
      "timestamp": "2026-03-17T09:00:00Z"
    },
    {
      "role": "assistant",
      "content": "I can help with that...",
      "timestamp": "2026-03-17T09:00:05Z"
    }
  ],
  "metadata": {
    "total_input_tokens": 2100,
    "total_output_tokens": 450,
    "total_cost_usd": 0.013050,
    "tool_call_counts": {
      "search_knowledge_base": 2,
      "get_article": 1
    },
    "turns": [
      {
        "turn": 1,
        "input_tokens": 2100,
        "output_tokens": 450,
        "cost_usd": 0.013050,
        "tool_calls": ["search_knowledge_base", "get_article"],
        "tool_rounds": 1
      }
    ]
  },
  "created_at": "2026-03-17T09:00:00Z",
  "updated_at": "2026-03-17T09:15:00Z"
}
```

---

### Escalations

#### `GET /api/admin/escalations`

List all escalations.

**Query params:**
- `status` (string, optional) — `pending`, `in_progress`, `resolved`
- `page` (int, default 1)
- `per_page` (int, default 20)

**Response: `200 OK`**
```json
{
  "escalations": [
    {
      "id": 1,
      "session_id": "550e8400-e29b-41d4-a716-446655440000",
      "reason": "billing_dispute",
      "summary": "Patient double-charged, refund pending 3 days",
      "status": "pending",
      "assigned_to": "support@clinicdesk.com",
      "calendar_event_id": "abc123",
      "email_sent_at": "2026-03-17T10:00:00Z",
      "created_at": "2026-03-17T10:00:00Z",
      "resolved_at": null
    }
  ],
  "total": 8,
  "page": 1,
  "per_page": 20
}
```

#### `PUT /api/admin/escalations/{id}`

Update escalation status.

**Request body:**
```json
{
  "status": "resolved",
  "assigned_to": "sarah@clinicdesk.com"
}
```

**Response: `200 OK`** — updated escalation object

---

### Analytics

#### `GET /api/admin/analytics`

Get aggregated analytics.

**Query params:**
- `days` (int, default 30) — look-back period

**Response: `200 OK`**
```json
{
  "total_sessions": 245,
  "active_sessions": 3,
  "total_escalations": 18,
  "escalation_rate": 0.073,
  "resolved_escalations": 15,
  "resolution_rate": 0.833,
  "avg_session_duration_seconds": 420,
  "avg_messages_per_session": 8.5,
  "top_categories": [
    { "category": "insurance_claims", "count": 67 },
    { "category": "billing_coding", "count": 52 },
    { "category": "scheduling", "count": 45 }
  ],
  "escalation_reasons": [
    { "reason": "knowledge_gap", "count": 8 },
    { "reason": "billing_dispute", "count": 5 },
    { "reason": "user_frustration", "count": 3 }
  ],
  "period_days": 30
}
```

---

### Auth

#### `POST /api/auth/login`

Simple login for demo.

**Request body:**
```json
{
  "email": "admin@clinicdesk.com",
  "password": "demo123"
}
```

**Response: `200 OK`**
```json
{
  "token": "eyJhbGciOi...",
  "user": {
    "id": 1,
    "email": "admin@clinicdesk.com",
    "name": "Admin User",
    "role": "admin"
  }
}
```

---

## Staff-Accessible Endpoints

These require auth but allow `staff` or `admin` role:

#### `GET /api/sessions/me`

List current user's own sessions. Same shape as admin sessions list but filtered to `user_id`.

#### `GET /api/sessions/me/{id}`

Get own session detail. Same shape as admin session detail, 404 if not owned by user.

---

## Public Endpoints

These require no authentication — used by the chat widget.

#### `GET /api/sessions/{session_id}/messages`

Get messages for a session. Used by the widget to restore conversation history on page reload.

**Response: `200 OK`**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "How do I submit a pre-authorization?",
      "timestamp": "2026-03-17T09:00:00Z"
    },
    {
      "role": "assistant",
      "content": "I can help with that...",
      "timestamp": "2026-03-17T09:00:05Z"
    }
  ]
}
```

---

## Error Responses

All errors follow this shape:

```json
{
  "detail": "Description of what went wrong"
}
```

| Status | Meaning |
|--------|---------|
| 400 | Bad request — invalid input |
| 401 | Unauthorized — missing or invalid auth |
| 403 | Forbidden — insufficient role |
| 404 | Not found |
| 422 | Validation error (Pydantic) |
| 500 | Internal server error |
