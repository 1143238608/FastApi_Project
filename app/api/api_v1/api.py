from fastapi import APIRouter
from app.api.api_v1 import main, items

router = APIRouter()
router.include_router(items.router, prefix="/items", tags=["items"])
router.include_router(main.router, prefix="/main", tags=["main"])
