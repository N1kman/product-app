from typing import Annotated

from fastapi import Header, Depends, HTTPException

from src.domain.entities import Customer
from src.domain.response import ResponseFailure
from src.domain.usecases import GetPaymentOptions
from src.domain.usecases.add_customer import AddCustomer
from src.domain.usecases.get_customer_by_id import GetCustomerById
from src.domain.usecases.get_customers import GetCustomers
from src.infrastructure.api.utils import APIRouter, get_db_imple, check_language

router = APIRouter(prefix="/customer", tags=["Customers"])


def get_usecase_get_payment_options(accept_language: str = Header("en")):
    return GetPaymentOptions(get_db_imple(check_language(accept_language)))


@router.get("/payment_options")
async def get_payment_options(
        use_case: Annotated[GetPaymentOptions, Depends(get_usecase_get_payment_options)],
):
    response = await use_case.execute(
        request=GetPaymentOptions.Request()
    )
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response


@router.post("/")
async def add_customer(
        customer: Customer,
        use_case: Annotated[AddCustomer, Depends(AddCustomer)],
):
    response = await use_case.execute(
        request=AddCustomer.Request(customer=customer)
    )
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response


def get_usecase_get_customers(accept_language: str = Header("en")):
    return GetCustomers(get_db_imple(check_language(accept_language)))


@router.get("/")
async def get_customers(
        use_case: Annotated[GetCustomers, Depends(get_usecase_get_customers)],
):
    response = await use_case.execute(
        request=GetCustomers.Request()
    )
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response


def get_usecase_get_customer_by_id(accept_language: str = Header("en")):
    return GetCustomerById(get_db_imple(check_language(accept_language)))


@router.get("/{customer_id}")
async def get_customer_by_id(
        customer_id: int,
        use_case: Annotated[GetCustomerById, Depends(get_usecase_get_customer_by_id)],
):
    response = await use_case.execute(
        request=GetCustomerById.Request(id=customer_id)
    )
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response
