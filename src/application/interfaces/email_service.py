from abc import ABC, abstractmethod


class EmailServiceInterface(ABC):
    @abstractmethod
    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
    ) -> bool:
        """Send an email. Returns True if successful."""
        ...
