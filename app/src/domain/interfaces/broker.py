from abc import ABC, abstractmethod

from pydantic import BaseModel


class BrokerProducer(ABC):
    @abstractmethod
    async def send_message(self, topic: str, obj: BaseModel, model, method):
        pass
