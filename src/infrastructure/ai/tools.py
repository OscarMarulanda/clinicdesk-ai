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
        "name": "check_availability",
        "description": (
            "Check the support team's calendar for available callback slots. "
            "This only checks — it does NOT create anything. Use this when the user "
            "wants a callback so you can show them available times to choose from."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "preferred_time": {
                    "type": "string",
                    "description": "The user's preferred callback time (e.g., 'tomorrow at 4pm')",
                },
            },
            "required": ["preferred_time"],
        },
    },
    {
        "name": "escalate_to_human",
        "description": (
            "Create an escalation, book the callback, and send email notifications — all in one step. "
            "This is the ONLY tool that creates records and books calendar events. "
            "If the user wants a callback, you MUST have already called check_availability and "
            "gotten the user's slot choice BEFORE calling this tool. Pass the chosen slot's exact "
            "'start' value as confirmed_time."
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
                    "description": "A concise summary of the issue",
                },
                "preferred_action": {
                    "type": "string",
                    "enum": ["calendar", "email", "both"],
                    "description": "How to notify the support team",
                },
                "user_email": {
                    "type": "string",
                    "description": "The user's email address",
                },
                "confirmed_time": {
                    "type": "string",
                    "description": "The exact 'start' value from the slot the user chose from check_availability. Required when preferred_action is 'calendar' or 'both'.",
                },
            },
            "required": ["reason", "summary", "preferred_action"],
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
