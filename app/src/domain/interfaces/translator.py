from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.domain import LanguageEnum


class IAsyncTranslator(ABC):
    @abstractmethod
    def translate_obj(
            self,
            obj: BaseModel,
            target_lang: LanguageEnum
    ) -> BaseModel:
        """
        :param obj:
        BaseModel for translation
        :param target_lang:
        target language
        :return:
        translated BaseModel
        """
        pass

    @abstractmethod
    def translate_str(
            self,
            string: str,
            target_lang: LanguageEnum
    ) -> str:
        """
        :param string:
        string for translation
        :param target_lang:
        target language
        :return:
        translated string
        """
        pass
