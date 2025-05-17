from typing import List

from fastapi import APIRouter
from models.user import User

router = APIRouter()


@router.get("/user")
async def root():
    return {"Hello": "World"}
