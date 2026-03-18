from abc import ABC, abstractmethod


class CalendarServiceInterface(ABC):
    @abstractmethod
    async def create_event(
        self,
        summary: str,
        description: str,
        attendee_email: str,
        preferred_time: str,
        duration_minutes: int = 30,
    ) -> str:
        """Create a calendar event and return the event ID."""
        ...
