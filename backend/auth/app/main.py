import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.logging_config import setup_logging
from app.core.config import settings
from starlette.middleware.cors import CORSMiddleware
import sentry_sdk
from app.api.v1.api import api_router
from app.db.base import Base
from app.db.session import create_tables, engine
from app.utils.logging_middleware import LoggingMiddleware
from loguru import logger

# Base.metadata.create_all(bind=engine)

setup_logging()

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await create_tables()


# if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
#     sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(LoggingMiddleware)

app.include_router(api_router, prefix=settings.API_V1_STR)


# format all errors
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"Error {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            # "success": False,
            "message": exc.detail,
        },
    )


# Format error 422  (validate input error)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = [
        {
            "field": ".".join(str(x) for x in err["loc"][1:]),  # bỏ "body"
            "message": err["msg"],
        }
        for err in exc.errors()
    ]

    logger.error(f"Error 422: {str(formatted_errors)}")
    return JSONResponse(
        status_code=422,
        content={
            # "success": False,
            "message": "Validation error",
            "errors": formatted_errors,
        },
    )
