import logging
import os
from datetime import datetime, timedelta, timezone

from src.application.interfaces.calendar_service import CalendarServiceInterface
from src.infrastructure.config import settings

logger = logging.getLogger(__name__)


class GoogleCalendarService(CalendarServiceInterface):
    def __init__(self) -> None:
        self._service = None
        self._calendar_id = settings.google_calendar_id
        self._init_service()

    def _init_service(self) -> None:
        try:
            if not os.path.exists(settings.google_credentials_path):
                logger.warning(
                    "Google credentials file not found. Calendar integration disabled."
                )
                return

            from google.oauth2 import service_account
            from googleapiclient.discovery import build

            credentials = service_account.Credentials.from_service_account_file(
                settings.google_credentials_path,
                scopes=["https://www.googleapis.com/auth/calendar"],
            )
            self._service = build("calendar", "v3", credentials=credentials)
        except Exception as e:
            logger.warning(f"Could not initialize Google Calendar: {e}")

    async def create_event(
        self,
        summary: str,
        description: str,
        attendee_email: str,
        preferred_time: str,
        duration_minutes: int = 30,
    ) -> str:
        if self._service is None:
            logger.info(
                f"Calendar stub: would create event '{summary}' for {attendee_email} at {preferred_time}"
            )
            return f"stub-event-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

        # Parse preferred time — simplified for demo
        start_time = self._parse_preferred_time(preferred_time)
        end_time = start_time + timedelta(minutes=duration_minutes)

        event = {
            "summary": summary,
            "description": f"{description}\n\nCallback requested by: {attendee_email}",
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": "America/Bogota",
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "America/Bogota",
            },
        }

        result = self._service.events().insert(
            calendarId=self._calendar_id, body=event,
        ).execute()

        return result.get("id", "unknown")

    @staticmethod
    def _parse_preferred_time(preferred_time: str) -> datetime:
        """Parse natural language time preferences into naive datetime (local time)."""
        import re
        now = datetime.now()  # local time, no timezone — Calendar API uses timeZone field

        lower = preferred_time.lower()
        if "tomorrow" in lower:
            base = now + timedelta(days=1)
        else:
            base = now

        # Try to extract specific hour like "2pm", "3:30 pm", "after 4"
        hour_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(?:pm|p\.m\.)', lower)
        if hour_match:
            hour = int(hour_match.group(1))
            minute = int(hour_match.group(2) or 0)
            if hour < 12:
                hour += 12
            return base.replace(hour=hour, minute=minute, second=0, microsecond=0)

        hour_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(?:am|a\.m\.)', lower)
        if hour_match:
            hour = int(hour_match.group(1))
            minute = int(hour_match.group(2) or 0)
            if hour == 12:
                hour = 0
            return base.replace(hour=hour, minute=minute, second=0, microsecond=0)

        # "after X" pattern
        after_match = re.search(r'after\s+(\d{1,2})', lower)
        if after_match:
            hour = int(after_match.group(1))
            if hour < 7:  # assume PM for small numbers
                hour += 12
            return base.replace(hour=hour, minute=0, second=0, microsecond=0)

        if "morning" in lower:
            return base.replace(hour=10, minute=0, second=0, microsecond=0)
        elif "afternoon" in lower:
            return base.replace(hour=14, minute=0, second=0, microsecond=0)
        elif "evening" in lower:
            return base.replace(hour=17, minute=0, second=0, microsecond=0)
        elif "soon" in lower or "asap" in lower or "now" in lower:
            return now + timedelta(minutes=30)
        else:
            # Default to 1 hour from now
            return now + timedelta(hours=1)
