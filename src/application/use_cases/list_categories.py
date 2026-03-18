from src.domain.repositories.knowledge_repository import KnowledgeRepositoryBase


class ListCategoriesUseCase:
    def __init__(self, knowledge_repo: KnowledgeRepositoryBase) -> None:
        self._knowledge_repo = knowledge_repo

    async def execute(self) -> list[str]:
        return await self._knowledge_repo.list_categories()
