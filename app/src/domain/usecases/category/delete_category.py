from typing import Annotated

from fastapi import Depends

from src.domain.entities import CategoryRead
from src.domain.interfaces import IUseCase
from src.domain.request import RequestModel
from src.domain.response import ResponseModel, ResponseSuccess, ResponseFailure
from src.infrastructure.repositories.db import DBCategoryRepository


class DeleteCategory(IUseCase):
    class Request(RequestModel):
        id: int

    class Response(ResponseModel):
        pass

    def __init__(
            self,
            repository: Annotated[DBCategoryRepository, Depends(DBCategoryRepository)],
    ):
        self.repository = repository

    async def execute(self, request: Request):
        try:
            async with self.repository as repository:
                await repository.delete(request.id)
        except Exception as exc:
            return ResponseFailure.build(exc)
