from abc import ABC, abstractmethod

from src.domain.request import RequestModel


class IUseCase(ABC):
    @abstractmethod
    async def execute(self, request: RequestModel):
        pass
