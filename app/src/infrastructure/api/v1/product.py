from typing import Annotated, Any

from fastapi import Depends, HTTPException, Header

from src.domain.entities.product import ProductRead, Product
from src.domain.response import ResponseFailure
from src.domain.usecases import GetProductById
from src.domain.usecases.add_product import AddProduct
from src.domain.usecases.get_products import GetProducts
from src.infrastructure.api.utils import APIRouter, check_language, get_usecase_get_product_by_id, \
    get_usecase_get_products
from src.infrastructure.repositories import RuDBRepository, EnDBRepository, DeDBRepository

router = APIRouter(prefix="/poducts", tags=["Products"])


@router.get("/{product_id}")
async def get_product(
        product_id: int,
        use_case: Annotated[GetProductById, Depends(get_usecase_get_product_by_id)],
):
    response = await use_case.execute(
        GetProductById.Request(id=product_id)
    )
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response


@router.get("/")
async def get_products(
        use_case: Annotated[GetProducts, Depends(get_usecase_get_products)],
):
    response = await use_case.execute(
        use_case.execute(
            request=GetProducts.Request()
        )
    )
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response


@router.post("/")
async def add_product(
        product: Product,
        use_case: Annotated[AddProduct, Depends(AddProduct)]
):
    response = await use_case.execute(
        AddProduct.Request(product=product)
    )
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response
