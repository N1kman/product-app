from typing import Annotated

from fastapi import Depends

from src.domain.entities import Product
from src.domain.interfaces import IUseCase
from src.domain.request import RequestModel
from src.domain.response import ResponseModel, ResponseSuccess, ResponseFailure
from src.infrastructure.repositories import EnDBRepository


class AddProduct(IUseCase):
    class Request(RequestModel):
        product: Product

    class Response(ResponseModel):
        id: int

    def __init__(
            self, repository: Annotated[EnDBRepository, Depends(EnDBRepository)]
    ):
        self.repository = repository

    async def execute(self, request: Request):
        try:
            product = Product(**request.product.model_dump())
            async with self.repository as repository:
                id = await repository.add_product(product)
            return ResponseSuccess.build(
                payload=id,
                status=ResponseSuccess.ResponseStatus.SUCCESS
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
