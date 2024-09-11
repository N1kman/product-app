from typing import Annotated

from fastapi import Header, Depends, HTTPException

from src.domain import LanguageEnum
from src.domain.entities import Category
from src.domain.response import ResponseFailure
from src.domain.usecases import GetCategory, AddCategory
from src.infrastructure.api.utils import APIRouter, convert_header_lang

router = APIRouter(prefix="/category", tags=["Categories"])


@router.get("/")
async def get_category(
        id: int,
        use_case: Annotated[GetCategory, Depends(GetCategory)],
        accept_language: str = Header("en"),
):
    accept_language = LanguageEnum(convert_header_lang(accept_language))
    response = await use_case.execute(
        request=GetCategory.Request(
            id=id,
            language=accept_language
        )
    )
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response


@router.post("/")
async def add_category(
        category: Category,
        use_case: Annotated[AddCategory, Depends(AddCategory)],
):
    response = await use_case.execute(
        request=AddCategory.Request(category=category)
    )
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response
