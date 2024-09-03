from typing import Annotated

from fastapi import HTTPException, Depends

from src.domain.entities import Order
from src.domain.response import ResponseFailure
from src.domain.usecases.add_order import AddOrder
from src.infrastructure.api.utils import APIRouter

router = APIRouter(prefix="/order", tags=["Orders"])


@router.post("/")
async def add_order(
        order: Order,
        use_case: Annotated[AddOrder, Depends(AddOrder)],
):
    response = await use_case.execute(
        request=AddOrder.Request(order=order)
    )
    if isinstance(response, ResponseFailure):
        raise HTTPException(status_code=response.status.value, detail=response.err_msg)
    return response
