from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import socketio
from app.core.logging_config import setup_logging
from app.core.config import settings
from starlette.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.db.session import create_tables
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.socketio.server import sio

setup_logging()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await create_tables()


# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# app.add_middleware(LoggingMiddleware)

app.include_router(api_router, prefix=settings.API_V1_STR)

socket_app = socketio.ASGIApp(
    sio
)

# Mount Socket.IO application
app.mount("/", socket_app)


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


# Handle Starlette 401/403/404 from security dependencies
@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(
    request: Request, exc: StarletteHTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
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

