from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()
