from pydantic import BaseModel


class CategoryCount(BaseModel):
    category: str
    count: int


class ReasonCount(BaseModel):
    reason: str
    count: int


class AnalyticsResponse(BaseModel):
    total_sessions: int
    active_sessions: int
    total_escalations: int
    escalation_rate: float
    resolved_escalations: int
    resolution_rate: float
    avg_messages_per_session: float
    total_cost_usd: float
    avg_cost_per_session: float
    total_input_tokens: int
    total_output_tokens: int
    avg_tokens_per_session: float
    top_categories: list[CategoryCount]
    escalation_reasons: list[ReasonCount]
    period_days: int
