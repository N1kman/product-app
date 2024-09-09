from abc import abstractmethod

from src.domain.entities import Manufacturer, ManufacturerReadWithTranslations, ManufacturerRead, \
    ManufacturerWithTranslations
from src.domain.interfaces import IRepository
from src.domain.language import LanguageEnum


class IManufacturerRepository(IRepository):
    @abstractmethod
    async def add(
            self,
            manufacturer: ManufacturerWithTranslations,
    ) -> ManufacturerReadWithTranslations:
        """
        :param manufacturer:
        manufacturer with translations
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
            id: int,
            manufacturer: ManufacturerWithTranslations,
    ) -> ManufacturerReadWithTranslations:
        """
        :param id:
        id of manufacturer
        :param manufacturer:
        manufacturer with translations
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
