from fastapi import APIRouter, Depends, HTTPException, Query

from src.application.dto.article import (
    ArticleCreate,
    ArticleListResponse,
    ArticleResponse,
    ArticleUpdate,
)
from src.application.use_cases.manage_articles import ManageArticlesUseCase
from src.domain.exceptions import EntityNotFoundError
from src.presentation.dependencies import get_manage_articles_use_case
from src.presentation.middleware.auth import require_admin

router = APIRouter(prefix="/api/admin/articles", tags=["articles"])


@router.get("", response_model=ArticleListResponse)
async def list_articles(
    category: str | None = None,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    use_case: ManageArticlesUseCase = Depends(get_manage_articles_use_case),
    _admin: dict = Depends(require_admin),
):
    articles, total = await use_case.list_articles(
        category=category, page=page, per_page=per_page
    )
    return ArticleListResponse(
        articles=[
            ArticleResponse(
                id=a.id,
                title=a.title,
                slug=a.slug,
                category=a.category.value,
                content=a.content,
                created_by=a.created_by,
                updated_at=a.updated_at,
                created_at=a.created_at,
            )
            for a in articles
        ],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.post("", response_model=ArticleResponse, status_code=201)
async def create_article(
    body: ArticleCreate,
    use_case: ManageArticlesUseCase = Depends(get_manage_articles_use_case),
    admin: dict = Depends(require_admin),
):
    article = await use_case.create_article(
        title=body.title,
        category=body.category,
        content=body.content,
        created_by=admin.get("user_id"),
    )
    return ArticleResponse(
        id=article.id,
        title=article.title,
        slug=article.slug,
        category=article.category.value,
        content=article.content,
        created_by=article.created_by,
        updated_at=article.updated_at,
        created_at=article.created_at,
    )


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: int,
    use_case: ManageArticlesUseCase = Depends(get_manage_articles_use_case),
    _admin: dict = Depends(require_admin),
):
    try:
        article = await use_case.get_article(article_id)
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleResponse(
        id=article.id,
        title=article.title,
        slug=article.slug,
        category=article.category.value,
        content=article.content,
        created_by=article.created_by,
        updated_at=article.updated_at,
        created_at=article.created_at,
    )


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: int,
    body: ArticleUpdate,
    use_case: ManageArticlesUseCase = Depends(get_manage_articles_use_case),
    _admin: dict = Depends(require_admin),
):
    try:
        article = await use_case.update_article(
            article_id,
            title=body.title,
            category=body.category,
            content=body.content,
        )
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleResponse(
        id=article.id,
        title=article.title,
        slug=article.slug,
        category=article.category.value,
        content=article.content,
        created_by=article.created_by,
        updated_at=article.updated_at,
        created_at=article.created_at,
    )


@router.delete("/{article_id}", status_code=204)
async def delete_article(
    article_id: int,
    use_case: ManageArticlesUseCase = Depends(get_manage_articles_use_case),
    _admin: dict = Depends(require_admin),
):
    try:
        await use_case.delete_article(article_id)
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Article not found")
