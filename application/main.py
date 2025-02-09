from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post, user

models.Base.metadata.create_all(engine)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
