from fastapi import APIRouter
from api.api_v1 import items, main

router = APIRouter()
router.include_router(items.router, prefix="/items", tags=["items"])
router.include_router(main.router, prefix="/main", tags=["main"])
