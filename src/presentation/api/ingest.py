import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from src.application.use_cases.ingest_document import IngestDocumentUseCase
from src.presentation.dependencies import get_ingest_document_use_case
from src.presentation.middleware.auth import require_admin

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin/ingest", tags=["ingest"])

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("")
async def ingest_document(
    file: UploadFile = File(...),
    use_case: IngestDocumentUseCase = Depends(get_ingest_document_use_case),
    _admin: dict = Depends(require_admin),
):
    # Validate extension
    filename = file.filename or "unknown"
    ext = ("." + filename.rsplit(".", 1)[-1]).lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Allowed: PDF, DOCX, TXT",
        )

    # Read and validate size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum 10MB.")

    try:
        result = await use_case.execute(content, filename)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    return result
