from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from application.routers import vote
from .database import engine
from . import models
from .routers import login, post, user

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS to allow Google domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.google.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,  # Cache preflight requests for 10 minutes
)

# Middleware to log incoming requests (for debugging)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request: {request.method} {request.url}")
    print(f"Origin: {request.headers.get('origin')}")
    response = await call_next(request)
    return response


@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(vote.router)
