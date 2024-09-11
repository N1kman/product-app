from typing import Annotated

from fastapi import Header, Depends, HTTPException

from src.domain.entities import Customer
from src.domain.response import ResponseFailure
from src.domain.usecases import GetPaymentOptions
from src.domain.usecases import AddCustomer
from src.domain.usecases import GetCustomerById
from src.domain.usecases import GetCustomers
from src.infrastructure.api.utils import APIRouter, get_db_imple, check_language

router = APIRouter(prefix="/customer", tags=["Customers"])


@router.get("/payment_options")
async def get_payment_options(
        use_case: Annotated[GetPaymentOptions, Depends(GetPaymentOptions)],
        accept_language: str = Header("en"),
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


@router.get("/")
async def get_customers(
        use_case: Annotated[GetCustomers, Depends(GetCustomers)],
):
    response = await use_case.execute(
        request=GetCustomers.Request()
    )
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response


@router.get("/{customer_id}")
async def get_customer_by_id(
        customer_id: int,
        use_case: Annotated[GetCustomerById, Depends(GetCustomerById)],
):
    response = await use_case.execute(
        request=GetCustomerById.Request(id=customer_id)
    )
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response
