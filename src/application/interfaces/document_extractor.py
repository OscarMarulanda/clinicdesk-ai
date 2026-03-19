from abc import ABC, abstractmethod


class DocumentExtractorInterface(ABC):
    @abstractmethod
    async def extract_text(self, file_content: bytes, filename: str) -> str:
        """Extract plain text from a document file (PDF, DOCX, TXT).

        Raises ValueError for unsupported file types or unreadable files.
        """
        ...
