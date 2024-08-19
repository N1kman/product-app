from typing import Annotated, Any

from fastapi import Depends, HTTPException

from src.domain.entities.product import ProductRead, Product
from src.domain.response import ResponseFailure
from src.domain.usecases import GetProductById
from src.domain.usecases.add_product import AddProduct
from src.infrastructure.api.utils import APIRouter

router = APIRouter(prefix="/poducts", tags=["Products"])


@router.get("/{product_id}")
async def get_product(
        product_id: int,
        use_case: Annotated[GetProductById, Depends(GetProductById)]
):
    response = await use_case.execute(
        GetProductById.Request(id=product_id)
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
