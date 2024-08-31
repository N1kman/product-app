from typing import Annotated

from fastapi import Depends

from src.domain.entities import Product
from src.domain.interfaces import IUseCase
from src.domain.request import RequestModel
from src.domain.response import ResponseModel, ResponseSuccess, ResponseFailure
from src.infrastructure.configs import kafka_config
from src.infrastructure.kafka import KafkaProducer
from src.infrastructure.repositories import EnDBRepository


class AddProduct(IUseCase):
    class Request(RequestModel):
        product: Product

    class Response(ResponseModel):
        id: int

    def __init__(
            self,
            repository: Annotated[EnDBRepository, Depends(EnDBRepository)],
            broker: Annotated[KafkaProducer, Depends(KafkaProducer)]
    ):
        self.repository = repository
        self.broker = broker

    async def execute(self, request: Request):
        try:
            async with self.broker as producer:
                await producer.send_message(
                    kafka_config.KAFKA_TOPIC,
                    request.product, Product.__name__,
                    EnDBRepository.add_product.__name__
                )
            product = Product(**request.product.model_dump())
            async with self.repository as repository:
                id = await repository.add_product(product)
            return ResponseSuccess.build(
                payload=id,
                status=ResponseSuccess.ResponseStatus.SUCCESS
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
