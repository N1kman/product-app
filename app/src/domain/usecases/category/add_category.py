from typing import Annotated

from fastapi import Depends

from src.domain.entities import Category
from src.domain.interfaces import IUseCase
from src.domain.request import RequestModel
from src.domain.response import ResponseModel, ResponseSuccess, ResponseFailure
from src.infrastructure.repositories import DBRepository


class AddCategory(IUseCase):
    class Request(RequestModel):
        category: Category

    class Response(ResponseModel):
        id: int

    def __init__(
            self,
            repository: Annotated[DBRepository, Depends(DBRepository)],
    ):
        self.repository = repository

    async def execute(self, request: Request):
        try:
            async with self.repository as repository:
                id = await repository.add_customer(request.customer)
            return ResponseSuccess.build(
                payload=id,
                status=ResponseSuccess.ResponseStatus.SUCCESS
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
