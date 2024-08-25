from abc import ABC, abstractmethod
from enum import Enum


class Language(str, Enum):
    en = "en_XX"
    ru = "ru_RU"
    de = "de_DE"


class IAsyncTranslator(ABC):
    @abstractmethod
    async def async_translate_obj(self, obj: object, src_lang: Language, target_lang: Language):
        pass


class ITranslator(ABC):
    @abstractmethod
    def translate_obj(self, obj: object, src_lang: Language, target_lang: Language):
        pass
