from abc import abstractmethod

from src.domain.entities import Category, CategoryReadWithTranslations, CategoryRead
from src.domain.interfaces import IRepository
from src.domain.language import LanguageEnum


class ICategoryRepository(IRepository):
    @abstractmethod
    async def add(
            self,
            categories: list[Category],
            available_languages: list[LanguageEnum],
    ) -> CategoryReadWithTranslations:
        """
        :param categories:
        category with translations
        :param available_languages:
        list of languages for translations
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
            categories: list[Category],
            available_languages: list[LanguageEnum],
    ) -> CategoryReadWithTranslations:
        """
        :param categories:
        category with translations
        :param available_languages:
        list of languages for translations
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
