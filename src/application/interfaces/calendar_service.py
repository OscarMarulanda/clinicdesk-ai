from abc import ABC, abstractmethod


class CalendarServiceInterface(ABC):
    @abstractmethod
    async def check_availability(
        self,
        preferred_time: str,
        duration_minutes: int = 30,
        num_options: int = 3,
    ) -> list[dict[str, str]]:
        """Check calendar availability around the preferred time.

        Returns a list of available slots, each with:
            - start: str (ISO format)
            - end: str (ISO format)
        """
        ...

    @abstractmethod
    async def create_event(
        self,
        summary: str,
        description: str,
        attendee_email: str,
        start_time: str,
        duration_minutes: int = 30,
    ) -> dict[str, str]:
        """Create a calendar event at a specific time (already confirmed available).

        Returns dict with:
            - event_id: str
            - scheduled_time: str (ISO format)
        """
        ...
