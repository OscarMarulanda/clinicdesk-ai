from src.application.interfaces.calendar_service import CalendarServiceInterface


class ScheduleCallbackUseCase:
    def __init__(self, calendar_service: CalendarServiceInterface) -> None:
        self._calendar_service = calendar_service

    async def execute(
        self,
        user_email: str,
        preferred_time: str,
        issue_summary: str,
    ) -> dict[str, str]:
        """Schedule a callback and return event_id + scheduled_time."""
        return await self._calendar_service.create_event(
            summary="ClinicDesk Support Callback",
            description=f"Support callback requested.\n\nIssue: {issue_summary}",
            attendee_email=user_email,
            preferred_time=preferred_time,
        )
