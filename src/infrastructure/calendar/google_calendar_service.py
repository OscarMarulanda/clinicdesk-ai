import logging
import os
import re
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from src.application.interfaces.calendar_service import CalendarServiceInterface
from src.infrastructure.config import settings

LOCAL_TZ = ZoneInfo("America/Bogota")

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

    async def check_availability(
        self,
        preferred_time: str,
        duration_minutes: int = 30,
        num_options: int = 3,
    ) -> list[dict[str, str]]:
        start = self._parse_preferred_time(preferred_time)

        if self._service is None:
            # Stub: return fake options around the preferred time
            options = []
            candidate = start
            for _ in range(num_options):
                candidate = self._next_business_slot(candidate)
                options.append({
                    "start": candidate.isoformat(),
                    "end": (candidate + timedelta(minutes=duration_minutes)).isoformat(),
                })
                candidate = candidate + timedelta(minutes=60)
            return options

        # Get all events for the target day so we can find gaps
        start = self._next_business_slot(start)
        day_start = start.replace(hour=8, minute=0, second=0, microsecond=0)
        day_end = start.replace(hour=18, minute=0, second=0, microsecond=0)

        try:
            events_result = self._service.events().list(
                calendarId=self._calendar_id,
                timeMin=day_start.isoformat() + "-05:00",
                timeMax=day_end.isoformat() + "-05:00",
                singleEvents=True,
                orderBy="startTime",
            ).execute()
        except Exception as e:
            logger.error(f"Calendar availability check failed: {e}")
            return []

        # Collect busy times — convert to naive local time regardless of source timezone
        busy = []
        for event in events_result.get("items", []):
            evt_start = event.get("start", {}).get("dateTime", "")
            evt_end = event.get("end", {}).get("dateTime", "")
            if evt_start and evt_end:
                bs = datetime.fromisoformat(evt_start)
                be = datetime.fromisoformat(evt_end)
                # Convert to local timezone first, then strip tzinfo for naive comparison
                if bs.tzinfo is not None:
                    bs = bs.astimezone(LOCAL_TZ).replace(tzinfo=None)
                if be.tzinfo is not None:
                    be = be.astimezone(LOCAL_TZ).replace(tzinfo=None)
                busy.append((bs, be))

        # Scan the day in 30-min increments, find free slots, prefer ones closest to requested time
        options = []
        candidate = day_start
        while candidate + timedelta(minutes=duration_minutes) <= day_end:
            candidate_end = candidate + timedelta(minutes=duration_minutes)
            conflict = any(
                not (candidate_end <= bs or candidate >= be)
                for bs, be in busy
            )
            if not conflict and candidate >= datetime.now():
                options.append({
                    "start": candidate.isoformat(),
                    "end": candidate_end.isoformat(),
                })
            candidate = candidate + timedelta(minutes=30)

        # Sort by proximity to the preferred time, then take top N
        options.sort(key=lambda s: abs(datetime.fromisoformat(s["start"]) - start))
        options = options[:num_options]
        # Re-sort chronologically for display
        options.sort(key=lambda s: s["start"])

        return options

    async def create_event(
        self,
        summary: str,
        description: str,
        attendee_email: str,
        start_time: str,
        duration_minutes: int = 30,
    ) -> dict[str, str]:
        # Parse the confirmed start time
        try:
            parsed_start = datetime.fromisoformat(start_time)
        except ValueError:
            parsed_start = self._parse_preferred_time(start_time)

        # Safety: fix wrong year (agent sometimes hallucinates past years)
        now = datetime.now()
        if parsed_start.year < now.year:
            parsed_start = parsed_start.replace(year=now.year)
            logger.warning(f"Fixed wrong year in calendar event: {start_time} → {parsed_start.isoformat()}")

        end_time = parsed_start + timedelta(minutes=duration_minutes)

        if self._service is None:
            logger.info(
                f"Calendar stub: would create event '{summary}' for {attendee_email} at {parsed_start.isoformat()}"
            )
            return {
                "event_id": f"stub-event-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
                "scheduled_time": parsed_start.isoformat(),
                "meet_link": "",
            }

        # Verify the slot is actually free before booking
        try:
            events_result = self._service.events().list(
                calendarId=self._calendar_id,
                timeMin=parsed_start.isoformat() + "-05:00",
                timeMax=end_time.isoformat() + "-05:00",
                singleEvents=True,
            ).execute()
            if events_result.get("items"):
                logger.warning(
                    f"Slot conflict: {parsed_start.isoformat()} already has "
                    f"{len(events_result['items'])} event(s)"
                )
                raise ValueError(
                    f"The slot at {parsed_start.strftime('%I:%M %p')} is already booked. "
                    f"Please call check_availability to find a free slot."
                )
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Could not verify slot availability: {e}")

        import uuid

        event = {
            "summary": summary,
            "description": f"{description}\n\nCallback requested by: {attendee_email}",
            "start": {
                "dateTime": parsed_start.isoformat(),
                "timeZone": "America/Bogota",
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "America/Bogota",
            },
            "conferenceData": {
                "createRequest": {
                    "requestId": uuid.uuid4().hex,
                    "conferenceSolutionKey": {"type": "hangoutsMeet"},
                },
            },
        }

        if attendee_email:
            event["attendees"] = [{"email": attendee_email}]

        # Try progressively simpler inserts — service accounts on personal
        # Gmail can't add attendees or create Meet conferences.
        result = None
        attempts = [
            {"conferenceDataVersion": 1, "sendUpdates": "all"},  # full: attendees + Meet
            {"conferenceDataVersion": 1},                         # no attendees
            {},                                                   # no attendees, no Meet
        ]
        for i, kwargs in enumerate(attempts):
            try:
                result = self._service.events().insert(
                    calendarId=self._calendar_id, body=event, **kwargs,
                ).execute()
                break
            except Exception as e:
                err = str(e)
                if "forbiddenForServiceAccounts" in err or "invalid conference" in err.lower():
                    logger.warning(f"Calendar insert attempt {i + 1} failed: {e}")
                    # Strip features the service account can't use
                    event.pop("attendees", None)
                    event.pop("conferenceData", None)
                else:
                    raise

        if result is None:
            raise RuntimeError("All calendar insert attempts failed")

        meet_link = result.get("hangoutLink", "")
        logger.info(
            f"Calendar event created: {result.get('id')} at {parsed_start.isoformat()}"
            f"{f' | Meet: {meet_link}' if meet_link else ''}"
        )
        return {
            "event_id": result.get("id", "unknown"),
            "scheduled_time": parsed_start.isoformat(),
            "meet_link": meet_link,
        }

    @staticmethod
    def _next_business_slot(dt: datetime) -> datetime:
        """Adjust a datetime to fall within business hours (8am-6pm, Mon-Fri)."""
        now = datetime.now()
        if dt < now:
            dt = now + timedelta(minutes=15)
            dt = dt.replace(minute=(dt.minute // 15) * 15, second=0, microsecond=0)

        if dt.hour < 8:
            dt = dt.replace(hour=8, minute=0, second=0, microsecond=0)
        elif dt.hour >= 18:
            dt = dt + timedelta(days=1)
            dt = dt.replace(hour=8, minute=0, second=0, microsecond=0)

        # Skip weekends
        while dt.weekday() >= 5:
            dt = dt + timedelta(days=1)
            dt = dt.replace(hour=8, minute=0, second=0, microsecond=0)

        return dt

    @staticmethod
    def _parse_preferred_time(preferred_time: str) -> datetime:
        """Parse natural language time preferences into naive datetime (local time)."""
        now = datetime.now()

        lower = preferred_time.lower()
        if "tomorrow" in lower:
            base = now + timedelta(days=1)
        else:
            base = now

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

        after_match = re.search(r'after\s+(\d{1,2})', lower)
        if after_match:
            hour = int(after_match.group(1))
            if hour < 7:
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
            return now + timedelta(hours=1)
