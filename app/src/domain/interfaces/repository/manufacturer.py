from abc import abstractmethod

from src.domain.entities import Manufacturer, ManufacturerReadWithTranslations, ManufacturerRead
from src.domain.interfaces import IRepository
from src.domain.language import LanguageEnum


class IManufacturerRepository(IRepository):
    @abstractmethod
    async def add(
            self,
            manufacturers: list[Manufacturer],
            available_languages: list[LanguageEnum],
    ) -> ManufacturerReadWithTranslations:
        """
        :param manufacturers:
        manufacturer with translations
        :param available_languages:
        list of languages for translations
        :return:
        created manufacturer with translations
        """
        pass

    @abstractmethod
    async def delete(
            self,
            id: int,
    ) -> None:
        """
        :param id:
        id of deleted manufacturer
        :return:
        None
        """
        pass

    @abstractmethod
    async def update(
            self,
            manufacturers: list[Manufacturer],
            available_languages: list[LanguageEnum],
    ) -> ManufacturerReadWithTranslations:
        """
        :param manufacturers:
        manufacturer with translations
        :param available_languages:
        list of languages for translations
        :return:
        updated manufacturer with translations
        """
        pass

    @abstractmethod
    async def get(
            self,
            id: int,
            language: LanguageEnum,
    ) -> ManufacturerRead:
        """
        :param id:
        id of manufacturer
        :param language:
        language of manufacturer
        :return:
        manufacturer in target language
        """
        pass

    @abstractmethod
    async def get_all(
            self,
            language: LanguageEnum,
    ) -> list[ManufacturerRead]:
        """
        :param language:
        language of manufacturers
        :return:
        list of manufacturers in target language
        """
        pass
