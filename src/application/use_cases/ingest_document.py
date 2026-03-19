from src.application.interfaces.ai_service import AIServiceInterface
from src.application.interfaces.document_extractor import DocumentExtractorInterface


class IngestDocumentUseCase:
    def __init__(
        self,
        document_extractor: DocumentExtractorInterface,
        ai_service: AIServiceInterface,
    ) -> None:
        self._extractor = document_extractor
        self._ai = ai_service

    async def execute(self, file_content: bytes, filename: str) -> dict[str, str]:
        """Extract text from a document and structure it as a KB article.

        Returns dict with title, category, content for admin review.
        Does NOT save — the admin reviews and saves via the existing article API.
        """
        raw_text = await self._extractor.extract_text(file_content, filename)
        return await self._ai.structure_document(raw_text, filename)
