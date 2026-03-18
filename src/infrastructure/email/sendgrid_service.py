import logging

from src.application.interfaces.email_service import EmailServiceInterface
from src.infrastructure.config import settings

logger = logging.getLogger(__name__)


class SendGridEmailService(EmailServiceInterface):
    def __init__(self) -> None:
        self._client = None
        self._from_email = settings.sendgrid_from_email

        if settings.sendgrid_api_key and settings.sendgrid_api_key != "SG....":
            try:
                from sendgrid import SendGridAPIClient

                self._client = SendGridAPIClient(settings.sendgrid_api_key)
            except Exception as e:
                logger.warning(f"Could not initialize SendGrid: {e}")
        else:
            logger.warning("SendGrid API key not configured. Email integration disabled.")

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
    ) -> bool:
        if self._client is None:
            logger.info(
                f"Email stub: would send '{subject}' to {to_email}\nBody: {body[:200]}..."
            )
            return True

        try:
            from sendgrid.helpers.mail import Content, Email, Mail, To

            message = Mail(
                from_email=Email(self._from_email),
                to_emails=To(to_email),
                subject=subject,
                plain_text_content=Content("text/plain", body),
            )

            response = self._client.send(message)
            logger.info(f"Email sent to {to_email}: status={response.status_code}")
            return response.status_code in (200, 201, 202)

        except Exception as e:
            logger.error(f"SendGrid error: {e}")
            return False
