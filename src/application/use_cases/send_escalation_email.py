from src.application.interfaces.email_service import EmailServiceInterface


class SendEscalationEmailUseCase:
    def __init__(self, email_service: EmailServiceInterface) -> None:
        self._email_service = email_service

    async def execute(
        self,
        to_email: str,
        subject: str,
        conversation_summary: str,
    ) -> bool:
        return await self._email_service.send_email(
            to_email=to_email,
            subject=subject,
            body=conversation_summary,
        )
