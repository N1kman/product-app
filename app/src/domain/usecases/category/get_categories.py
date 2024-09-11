from typing import Annotated

from fastapi import Depends

from src.domain import LanguageEnum
from src.domain.entities import CategoryRead
from src.domain.interfaces import IUseCase
from src.domain.request import RequestModel
from src.domain.response import ResponseModel, ResponseSuccess, ResponseFailure
from src.infrastructure.repositories.db import DBCategoryRepository


class GetCategories(IUseCase):
    class Request(RequestModel):
        language: LanguageEnum

    class Response(ResponseModel):
        category_read: list[CategoryRead]

    def __init__(
            self,
            repository: Annotated[DBCategoryRepository, Depends(DBCategoryRepository)],
    ):
        self.repository = repository

    async def execute(self, request: Request):
        try:
            async with self.repository as repository:
                categories_read = await repository.get_all(request.language)
            return ResponseSuccess.build(
                payload=GetCategories.Response.construct(category_read=categories_read),
                status=ResponseSuccess.ResponseStatus.SUCCESS
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
