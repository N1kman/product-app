from typing import Annotated, Union

from fastapi import Depends

from src.domain.entities.product import ProductRead
from src.domain.interfaces import IUseCase
from src.domain.request import RequestModel
from src.domain.response import ResponseModel, ResponseFailure, ResponseSuccess
from src.infrastructure.repositories.db import DBRepository


class GetProductById(IUseCase):
    class Request(RequestModel):
        id: int

    class Response(ResponseModel):
        product: ProductRead

    def __init__(
            self, repository: Annotated[DBRepository, Depends(DBRepository)]
    ):
        self.repository = repository

    async def execute(self, request: Request) -> Union[ResponseSuccess, ResponseFailure]:
        try:
            async with self.repository as repository:
                product = await repository.get_product_by_id(request.id)
            return ResponseSuccess.build(
                payload=product,
                status=ResponseSuccess.ResponseStatus.SUCCESS
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
