from fastapi import Depends, HTTPException, status
import jwt
from jwt import PyJWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from . import schemas, models
from .database import get_db

from sqlalchemy.orm import Session
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "gYWS5Tk1qPhIAhsjZWHlqQA3AIrua6kO"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_access_token(token, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if not user_id:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except PyJWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: schemas.TokenData = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token(token, credentials_exception)

    current_user = db.query(models.User).filter(models.User.id == token.id).first()
    return current_user
