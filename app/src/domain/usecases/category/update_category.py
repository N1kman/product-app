from typing import Annotated

from fastapi import Depends

from src.domain import LanguageEnum
from src.domain.entities import CategoryReadWithTranslations, CategoryUpdate, CategoryUpdateWithTranslations
from src.domain.entities.language import Translation
from src.domain.interfaces import IUseCase
from src.domain.request import RequestModel
from src.domain.response import ResponseModel, ResponseSuccess, ResponseFailure
from src.infrastructure.repositories.db import DBCategoryRepository
from src.infrastructure.translator import MBartTranslator


class UpdateCategory(IUseCase):
    class Request(RequestModel):
        id: int
        category: CategoryUpdate

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
            if request.category.name is None:
                raise Exception("name is not valid")

            category_update = CategoryUpdateWithTranslations()

            for lang_abbr in LanguageEnum:
                name = Translation(
                    translated=self.translator.translate_str(
                        request.category.name,
                        LanguageEnum(lang_abbr),
                    ),
                    lang_abbr=lang_abbr,
                )
                category_update.name.append(name)

            async with self.repository as repository:
                category_read = await repository.update(request.id, category_update)
            return ResponseSuccess.build(
                payload=UpdateCategory.Response.construct(category_read=category_read),
                status=ResponseSuccess.ResponseStatus.SUCCESS
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
