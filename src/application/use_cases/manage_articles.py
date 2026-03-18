from src.domain.entities.article import Article, ArticleCategory
from src.domain.exceptions import EntityNotFoundError
from src.domain.repositories.knowledge_repository import KnowledgeRepositoryBase
from src.infrastructure.database.knowledge_repository import PostgresKnowledgeRepository


class ManageArticlesUseCase:
    def __init__(self, knowledge_repo: KnowledgeRepositoryBase) -> None:
        self._knowledge_repo = knowledge_repo

    async def list_articles(
        self,
        category: str | None = None,
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Article], int]:
        cat = ArticleCategory(category) if category else None
        return await self._knowledge_repo.list_all(category=cat, page=page, per_page=per_page)

    async def get_article(self, article_id: int) -> Article:
        article = await self._knowledge_repo.get_by_id(article_id)
        if article is None:
            raise EntityNotFoundError("Article", article_id)
        return article

    async def create_article(
        self,
        title: str,
        category: str,
        content: str,
        created_by: int | None = None,
    ) -> Article:
        slug = PostgresKnowledgeRepository.generate_slug(title)
        return await self._knowledge_repo.create(
            title=title,
            slug=slug,
            category=ArticleCategory(category),
            content=content,
            created_by=created_by,
        )

    async def update_article(
        self,
        article_id: int,
        title: str | None = None,
        category: str | None = None,
        content: str | None = None,
    ) -> Article:
        cat = ArticleCategory(category) if category else None
        article = await self._knowledge_repo.update(
            article_id, title=title, category=cat, content=content
        )
        if article is None:
            raise EntityNotFoundError("Article", article_id)
        return article

    async def delete_article(self, article_id: int) -> None:
        deleted = await self._knowledge_repo.delete(article_id)
        if not deleted:
            raise EntityNotFoundError("Article", article_id)
