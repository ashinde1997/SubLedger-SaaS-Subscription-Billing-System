from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import Base, engine
import app.models  # Register SQLAlchemy models with metadata
from app.api.v1.api import api_router
from app.exceptions import (
    EntityNotFoundError,
    BusinessRuleViolationError,
    DuplicateEntityError,
)

# Resolve Starlette 422 constant across versions
HTTP_422 = getattr(status, "HTTP_422_UNPROCESSABLE_CONTENT", 422)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-create database tables on application boot
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="SubLedger billing and subscription backend engine.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(EntityNotFoundError)
async def handle_not_found(request: Request, exc: EntityNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "Not Found", "detail": exc.message},
    )


@app.exception_handler(BusinessRuleViolationError)
async def handle_business_rule_violation(request: Request, exc: BusinessRuleViolationError):
    return JSONResponse(
        status_code=HTTP_422,
        content={"error": "Business Rule Violation", "detail": exc.message},
    )


@app.exception_handler(DuplicateEntityError)
async def handle_duplicate_entity(request: Request, exc: DuplicateEntityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": "Duplicate Entity", "detail": exc.message},
    )


@app.get("/", tags=["System"])
def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "healthy",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok"}


# Direct API routes (/plans, /customers, etc.)
app.include_router(api_router)

# Versioned routes (/api/v1/plans, etc.)
app.include_router(api_router, prefix=settings.API_V1_STR)
