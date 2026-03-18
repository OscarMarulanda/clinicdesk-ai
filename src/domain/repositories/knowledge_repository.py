from abc import ABC, abstractmethod

from src.domain.entities.article import Article, ArticleCategory, ArticleSearchResult


class KnowledgeRepositoryBase(ABC):
    @abstractmethod
    async def search(
        self, query: str, category: ArticleCategory | None = None, limit: int = 5
    ) -> list[ArticleSearchResult]:
        ...

    @abstractmethod
    async def get_by_id(self, article_id: int) -> Article | None:
        ...

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Article | None:
        ...

    @abstractmethod
    async def list_all(
        self,
        category: ArticleCategory | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Article], int]:
        ...

    @abstractmethod
    async def create(
        self,
        title: str,
        slug: str,
        category: ArticleCategory,
        content: str,
        created_by: int | None = None,
    ) -> Article:
        ...

    @abstractmethod
    async def update(
        self,
        article_id: int,
        title: str | None = None,
        category: ArticleCategory | None = None,
        content: str | None = None,
    ) -> Article | None:
        ...

    @abstractmethod
    async def delete(self, article_id: int) -> bool:
        ...

    @abstractmethod
    async def list_categories(self) -> list[str]:
        ...
