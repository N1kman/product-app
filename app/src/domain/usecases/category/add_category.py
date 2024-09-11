from typing import Annotated

from fastapi import Depends

from src.domain import LanguageEnum
from src.domain.entities import Category, CategoryWithTranslations, CategoryReadWithTranslations
from src.domain.entities.language import Translation
from src.domain.interfaces import IUseCase
from src.domain.request import RequestModel
from src.domain.response import ResponseModel, ResponseSuccess, ResponseFailure
from src.infrastructure.repositories.db import DBCategoryRepository
from src.infrastructure.translator import MBartTranslator


class AddCategory(IUseCase):
    class Request(RequestModel):
        category: Category

    class Response(ResponseModel):
        category_read: CategoryReadWithTranslations

    def __init__(
            self,
            repository: Annotated[DBCategoryRepository, Depends(DBCategoryRepository)],
            translator: Annotated[MBartTranslator, Depends(MBartTranslator)],
    ):
        self.repository = repository
        self.translator = translator

    async def execute(self, request: Request):
        try:
            category_add = CategoryWithTranslations()

            for lang_abbr in LanguageEnum:
                name = Translation(
                    translated=self.translator.translate_str(
                        request.category.name,
                        LanguageEnum(lang_abbr),
                    ),
                    lang_abbr=lang_abbr,
                )
                category_add.name.append(name)

            async with self.repository as repository:
                category_read = await repository.add(category_add)

            return ResponseSuccess.build(
                payload=AddCategory.Response.construct(category_read=category_read),
                status=ResponseSuccess.ResponseStatus.SUCCESS
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
