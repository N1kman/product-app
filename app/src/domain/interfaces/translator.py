from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.domain import LanguageEnum


class IAsyncTranslator(ABC):
    @abstractmethod
    async def async_translate_obj(
            self,
            obj: BaseModel,
            src_lang: LanguageEnum,
            target_lang: LanguageEnum
    ) -> BaseModel:
        """
        :param obj:
        BaseModel for translation
        :param src_lang:
        source language
        :param target_lang:
        target language
        :return:
        translated BaseModel
        """
        pass

    @abstractmethod
    async def async_translate_str(
            self,
            string: str,
            src_lang: LanguageEnum,
            target_lang: LanguageEnum
    ) -> str:
        """
        :param string:
        string for translation
        :param src_lang:
        source language
        :param target_lang:
        target language
        :return:
        translated string
        """
        pass
