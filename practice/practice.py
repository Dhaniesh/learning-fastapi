from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Protected route
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}