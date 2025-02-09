from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, utils, oauth2
from ..database import get_db

router = APIRouter(tags=["auth"])


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # Verify user
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    utils.verify(user_credentials.password, user.password)

    # verify password
    verify_password = utils.verify(user_credentials.password, user.password)
    if not verify_password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    # implement access token
    token = oauth2.create_access_token(data={"user_id": user.id})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
