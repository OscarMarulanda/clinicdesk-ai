import io
import logging

from src.application.interfaces.document_extractor import DocumentExtractorInterface

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_TEXT_LENGTH = 50_000  # ~50k chars to stay within Claude's context


class DocumentExtractor(DocumentExtractorInterface):
    async def extract_text(self, file_content: bytes, filename: str) -> str:
        ext = self._get_extension(filename)

        if ext == ".pdf":
            text = self._extract_pdf(file_content)
        elif ext == ".docx":
            text = self._extract_docx(file_content)
        elif ext == ".txt":
            text = self._extract_txt(file_content)
        else:
            raise ValueError(
                f"Unsupported file type: {ext}. Supported: {', '.join(SUPPORTED_EXTENSIONS)}"
            )

        if not text.strip():
            raise ValueError(
                "Could not extract any text from the document. "
                "It may be a scanned image or empty file."
            )

        if len(text) > MAX_TEXT_LENGTH:
            logger.warning(
                f"Document text truncated from {len(text)} to {MAX_TEXT_LENGTH} chars"
            )
            text = text[:MAX_TEXT_LENGTH] + "\n\n[Content truncated — document too long]"

        return text

    @staticmethod
    def _get_extension(filename: str) -> str:
        name = filename.lower().strip()
        for ext in SUPPORTED_EXTENSIONS:
            if name.endswith(ext):
                return ext
        return "." + name.rsplit(".", 1)[-1] if "." in name else ""

    @staticmethod
    def _extract_pdf(content: bytes) -> str:
        import fitz  # pymupdf

        doc = fitz.open(stream=content, filetype="pdf")
        pages = []
        for page in doc:
            pages.append(page.get_text())
        doc.close()
        return "\n\n".join(pages)

    @staticmethod
    def _extract_docx(content: bytes) -> str:
        from docx import Document

        doc = Document(io.BytesIO(content))
        return "\n\n".join(p.text for p in doc.paragraphs if p.text.strip())

    @staticmethod
    def _extract_txt(content: bytes) -> str:
        for encoding in ("utf-8", "latin-1"):
            try:
                return content.decode(encoding)
            except UnicodeDecodeError:
                continue
        raise ValueError("Could not decode text file")
