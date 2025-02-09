from .. import models, schemas
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from ..database import get_db
from .. import utils
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def add_user(user: schemas.User, db: Session = Depends(get_db)):

    user_exists = db.query(models.User).filter(models.User.email == user.email).first()
    if user_exists:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User already exists")
    # Hash password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"User with {user_id} not found")
    return user
