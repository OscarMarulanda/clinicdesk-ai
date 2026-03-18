from src.domain.entities.article import Article
from src.domain.exceptions import EntityNotFoundError
from src.domain.repositories.knowledge_repository import KnowledgeRepositoryBase


class GetArticleUseCase:
    def __init__(self, knowledge_repo: KnowledgeRepositoryBase) -> None:
        self._knowledge_repo = knowledge_repo

    async def execute(self, article_id: int) -> Article:
        article = await self._knowledge_repo.get_by_id(article_id)
        if article is None:
            raise EntityNotFoundError("Article", article_id)
        return article
