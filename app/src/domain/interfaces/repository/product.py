from abc import abstractmethod

from src.domain.entities import Product, ProductReadWithTranslations, ProductRead
from src.domain.interfaces import IRepository
from src.domain.language import LanguageEnum


class IProductRepository(IRepository):

    @abstractmethod
    async def add(
            self,
            products: list[Product],
            available_languages: list[LanguageEnum],
    ) -> ProductReadWithTranslations:
        """
        :param products:
        product with translations
        :param available_languages:
        list of languages for translations
        :return:
        created product with translations
        """
        pass

    @abstractmethod
    async def delete(
            self,
            id: int
    ) -> None:
        """
        :param id:
        id of deleted product
        :return:
        None
        """
        pass

    @abstractmethod
    async def update(
            self,
            products: list[Product],
            available_languages: list[LanguageEnum],
    ) -> ProductReadWithTranslations:
        """
        :param products:
        product with translations
        :param available_languages:
        list of languages for translations
        :return:
        updated product with translations
        """
        pass

    @abstractmethod
    async def get(
            self,
            id: int,
            language: LanguageEnum,
    ) -> ProductRead:
        """
        :param id:
        id of product
        :param language:
        language of product
        :return:
        product in target language
        """
        pass

    @abstractmethod
    async def get_all(
            self,
            language: LanguageEnum,
    ) -> list[ProductRead]:
        """
        :param language:
        language of products
        :return:
        list of products in target language
        """
        pass
