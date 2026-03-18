from src.application.interfaces.calendar_service import CalendarServiceInterface


class ScheduleCallbackUseCase:
    def __init__(self, calendar_service: CalendarServiceInterface) -> None:
        self._calendar_service = calendar_service

    async def execute(
        self,
        user_email: str,
        preferred_time: str,
        issue_summary: str,
    ) -> str:
        """Schedule a callback and return the calendar event ID."""
        event_id = await self._calendar_service.create_event(
            summary=f"ClinicDesk Support Callback",
            description=f"Support callback requested.\n\nIssue: {issue_summary}",
            attendee_email=user_email,
            preferred_time=preferred_time,
        )
        return event_id
