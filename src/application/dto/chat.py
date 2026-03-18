from pydantic import BaseModel


class ChatInput(BaseModel):
    message: str
    session_id: str | None = None
    user_id: int | None = None


class ChatOutput(BaseModel):
    message: str
    session_id: str
    tool_calls_made: list[str] | None = None
