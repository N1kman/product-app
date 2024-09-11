from src.infrastructure.api.utils import APIRouter
from .category import router as category_router

router = APIRouter(prefix="/api/v1")

router.include_router(
    category_router
)
