from src.domain.entities.article import ArticleCategory, ArticleSearchResult
from src.domain.repositories.knowledge_repository import KnowledgeRepositoryBase


class SearchKnowledgeBaseUseCase:
    def __init__(self, knowledge_repo: KnowledgeRepositoryBase) -> None:
        self._knowledge_repo = knowledge_repo

    async def execute(
        self, query: str, category: str | None = None, limit: int = 5
    ) -> list[ArticleSearchResult]:
        cat = ArticleCategory(category) if category else None
        return await self._knowledge_repo.search(query, category=cat, limit=limit)
