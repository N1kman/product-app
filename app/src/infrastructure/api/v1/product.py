from typing import Annotated, Any

from fastapi import Depends, HTTPException, Header

from src.domain.entities.product import ProductRead, Product
from src.domain.response import ResponseFailure
from src.domain.usecases import GetProductById
from src.domain.usecases import AddProduct
from src.domain.usecases import GetProducts
from src.domain.usecases.get_product_with_customers_by_id import GetProductWithCustomersById
from src.domain.usecases.get_products_with_customers import GetProductsWithCustomers
from src.infrastructure.api.utils import APIRouter, check_language, get_db_imple

router = APIRouter(prefix="/poducts", tags=["Products"])


def get_usecase_get_product_with_customers_by_id(accept_language: str = Header("en")):
    return GetProductWithCustomersById(get_db_imple(accept_language))


@router.get("/full/{product_id}")
async def get_product(
        product_id: int,
        use_case: Annotated[GetProductWithCustomersById, Depends(get_usecase_get_product_with_customers_by_id)],
):
    response = await use_case.execute(
        GetProductWithCustomersById.Request(id=product_id)
    )
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response


def get_usecase_get_products_with_customers(accept_language: str = Header("en")):
    return GetProductsWithCustomers(get_db_imple(check_language(accept_language)))


@router.get("/full")
async def get_products(
        use_case: Annotated[GetProductsWithCustomers, Depends(get_usecase_get_products_with_customers)],
):
    response = await use_case.execute(
        request=GetProductsWithCustomers.Request()
    )
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response


def get_usecase_get_product_by_id(accept_language: str = Header("en")):
    return GetProductById(get_db_imple(accept_language))


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


def get_usecase_get_products(accept_language: str = Header("en")):
    return GetProducts(get_db_imple(check_language(accept_language)))


@router.get("/")
async def get_products(
        use_case: Annotated[GetProducts, Depends(get_usecase_get_products)],
):
    response = await use_case.execute(
        request=GetProducts.Request()
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
