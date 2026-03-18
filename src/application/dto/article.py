from datetime import datetime

from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    category: str
    content: str


class ArticleUpdate(BaseModel):
    title: str | None = None
    category: str | None = None
    content: str | None = None


class ArticleResponse(BaseModel):
    id: int
    title: str
    slug: str
    category: str
    content: str
    created_by: int | None
    updated_at: datetime
    created_at: datetime


class ArticleListResponse(BaseModel):
    articles: list[ArticleResponse]
    total: int
    page: int
    per_page: int


class ArticleSearchResultResponse(BaseModel):
    id: int
    title: str
    category: str
    content: str
    rank: float
