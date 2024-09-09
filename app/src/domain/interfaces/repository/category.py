from abc import abstractmethod

from src.domain.entities import Category, CategoryReadWithTranslations, CategoryRead, CategoryWithTranslations
from src.domain.interfaces.repository import IRepository
from src.domain.language import LanguageEnum


class ICategoryRepository(IRepository):
    @abstractmethod
    async def add(
            self,
            category: CategoryWithTranslations,
    ) -> CategoryReadWithTranslations:
        """
        :param category:
        category with translations
        :return:
        created category with translations
        """
        pass

    @abstractmethod
    async def delete(
            self,
            id: int,
    ) -> None:
        """
        :param id:
        id of deleted category
        :return:
        None
        """
        pass

    @abstractmethod
    async def update(
            self,
            id: int,
            category: CategoryWithTranslations,
    ) -> CategoryReadWithTranslations:
        """
        :param id:
        id of category
        :param category:
        category with translations
        :return:
        updated category with translations
        """
        pass

    @abstractmethod
    async def get(
            self,
            id: int,
            language: LanguageEnum,
    ) -> CategoryRead:
        """
        :param id:
        id of category
        :param language:
        language of manufacturer
        :return:
        category in target language
        """
        pass

    @abstractmethod
    async def get_all(
            self,
            language: LanguageEnum,
    ) -> list[CategoryRead]:
        """
        :param language:
        language of categories
        :return:
        list of categories in target language
        """
        pass
