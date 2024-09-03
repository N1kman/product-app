from typing import Annotated

from fastapi import Depends

from src.domain.entities import Order
from src.domain.interfaces import IUseCase
from src.domain.request import RequestModel
from src.domain.response import ResponseModel, ResponseSuccess, ResponseFailure
from src.infrastructure.configs import kafka_config
from src.infrastructure.kafka import KafkaProducer
from src.infrastructure.repositories import EnDBRepository


class AddOrder(IUseCase):
    class Request(RequestModel):
        order: Order

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
                    request.order, Order.__name__,
                    EnDBRepository.add_order.__name__
                )
            async with self.repository as repository:
                id = await repository.add_order(request.order)
            return ResponseSuccess.build(
                payload=id,
                status=ResponseSuccess.ResponseStatus.SUCCESS
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
