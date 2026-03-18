from fastapi import APIRouter, Depends, Query

from src.application.dto.analytics import AnalyticsResponse
from src.application.use_cases.get_analytics import GetAnalyticsUseCase
from src.presentation.dependencies import get_analytics_use_case
from src.presentation.middleware.auth import require_admin

router = APIRouter(prefix="/api/admin/analytics", tags=["analytics"])


@router.get("", response_model=AnalyticsResponse)
async def get_analytics(
    days: int = Query(default=30, ge=1, le=365),
    use_case: GetAnalyticsUseCase = Depends(get_analytics_use_case),
    _admin: dict = Depends(require_admin),
):
    return await use_case.execute(days=days)
