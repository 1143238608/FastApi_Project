from fastapi import APIRouter
from api.api_v1 import main, items,parasePdf,chat

router = APIRouter()
router.include_router(items.router, prefix="/items", tags=["items"])
router.include_router(main.router, prefix="/main", tags=["main"])
router.include_router(parasePdf.router, prefix="/pdf", tags=["pdf"])
router.include_router(chat.router, prefix="/chat", tags=["chat"])
