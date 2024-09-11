from typing import Annotated

from fastapi import Depends

from src.domain import LanguageEnum
from src.domain.entities import CategoryRead
from src.domain.interfaces import IUseCase
from src.domain.request import RequestModel
from src.domain.response import ResponseModel, ResponseSuccess, ResponseFailure
from src.infrastructure.repositories.db import DBCategoryRepository


class GetCategory(IUseCase):
    class Request(RequestModel):
        id: int
        language: LanguageEnum

    class Response(ResponseModel):
        category_read: CategoryRead

    def __init__(
            self,
            repository: Annotated[DBCategoryRepository, Depends(DBCategoryRepository)],
    ):
        self.repository = repository

    async def execute(self, request: Request):
        try:
            async with self.repository as repository:
                category_read = await repository.get(request.id, request.language)
            return ResponseSuccess.build(
                payload=GetCategory.Response.construct(category_read=category_read),
                status=ResponseSuccess.ResponseStatus.SUCCESS
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
