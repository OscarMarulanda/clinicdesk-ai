from abc import ABC, abstractmethod

from src.domain.entities.provider import Provider


class ProviderRepositoryBase(ABC):
    @abstractmethod
    async def get_by_id(self, provider_id: int) -> Provider | None:
        ...

    @abstractmethod
    async def get_available(self) -> list[Provider]:
        ...

    @abstractmethod
    async def list_all(self) -> list[Provider]:
        ...
