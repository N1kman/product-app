from typing import Annotated, Union

from fastapi import Depends

from src.domain.entities.product import ProductRead
from src.domain.interfaces import IUseCase
from src.domain.request import RequestModel
from src.domain.response import ResponseModel, ResponseSuccess, ResponseFailure
from src.infrastructure.repositories import EnDBRepository
from src.infrastructure.repositories.db import DBRepository


class GetProducts(IUseCase):
    class Request(RequestModel):
        pass

    class Response(ResponseModel):
        products: list[ProductRead]

    def __init__(
            self, repository: DBRepository
    ):
        self.repository = repository

    async def execute(self, request: Request) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            async with self.repository as repository:
                products = await repository.get_products()
            return ResponseSuccess.build(
                payload=products,
                status=ResponseSuccess.ResponseStatus.SUCCESS
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
