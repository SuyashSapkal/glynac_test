from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

from app.api import api_router

# from app.core import JWTAuthMiddleware

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# CORS setup (optional, useful for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(JWTAuthMiddleware)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
