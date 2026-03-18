TOOL_DEFINITIONS = [
    {
        "name": "search_knowledge_base",
        "description": (
            "Search the ClinicDesk knowledge base for articles matching the user's question. "
            "Always use this before saying you don't have information on a topic."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query — use keywords from the user's question",
                },
                "category": {
                    "type": "string",
                    "enum": [
                        "scheduling",
                        "billing_coding",
                        "insurance_claims",
                        "patient_records",
                        "reporting_analytics",
                        "technical_troubleshooting",
                        "account_plans",
                    ],
                    "description": "Optional category filter to narrow results",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_article",
        "description": (
            "Get the full content of a knowledge base article by ID. "
            "Use this when search results show a relevant article and you need the complete details."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "article_id": {
                    "type": "integer",
                    "description": "The article ID from search results",
                },
            },
            "required": ["article_id"],
        },
    },
    {
        "name": "escalate_to_human",
        "description": (
            "Escalate the conversation to a human support representative. "
            "Use this when you cannot confidently resolve the issue, the user is frustrated, "
            "or the issue is out of scope."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "reason": {
                    "type": "string",
                    "enum": [
                        "knowledge_gap",
                        "user_frustration",
                        "out_of_scope",
                        "billing_dispute",
                        "account_change",
                    ],
                    "description": "Why this conversation needs human intervention",
                },
                "summary": {
                    "type": "string",
                    "description": "A concise summary of the issue and what has been attempted so far",
                },
                "preferred_action": {
                    "type": "string",
                    "enum": ["calendar", "email", "both"],
                    "description": "How to notify the support team — based on user preference",
                },
            },
            "required": ["reason", "summary", "preferred_action"],
        },
    },
    {
        "name": "schedule_callback",
        "description": (
            "Schedule a callback meeting between the user and a support representative "
            "via Google Calendar."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "user_email": {
                    "type": "string",
                    "description": "The user's email address for the calendar invite",
                },
                "preferred_time": {
                    "type": "string",
                    "description": "The user's preferred callback time (e.g., 'today after 2pm', 'tomorrow morning')",
                },
                "issue_summary": {
                    "type": "string",
                    "description": "Brief description of the issue for the calendar event description",
                },
            },
            "required": ["user_email", "preferred_time", "issue_summary"],
        },
    },
    {
        "name": "send_escalation_email",
        "description": (
            "Send an email to the support team with a summary of the conversation and the user's issue."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "to_email": {
                    "type": "string",
                    "description": "Support team email address",
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject line",
                },
                "conversation_summary": {
                    "type": "string",
                    "description": "Summary of the conversation including what was discussed and what the user needs",
                },
            },
            "required": ["to_email", "subject", "conversation_summary"],
        },
    },
    {
        "name": "update_session_notes",
        "description": (
            "Update your internal notes about this conversation. Use this to track what has been "
            "discussed, what was resolved, and any important context for follow-up."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "notes": {
                    "type": "string",
                    "description": "Updated notes about the conversation",
                },
            },
            "required": ["notes"],
        },
    },
    {
        "name": "get_user_info",
        "description": (
            "Get the user's profile and subscription plan information. "
            "Use this to personalize support and check what features are available on their plan."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's ID",
                },
            },
            "required": ["user_id"],
        },
    },
    {
        "name": "list_categories",
        "description": (
            "List all available knowledge base categories. "
            "Use this when the user wants to browse topics or when you want to suggest related categories."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]
