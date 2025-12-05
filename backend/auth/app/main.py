from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.exceptions import RequestValidationError
from app.core.db import Base, engine
from app.modules.auth.authController import authRouter
from app.modules.user.userController import userRouter
from fastapi.responses import JSONResponse
from app.common.utils.authHandler import AuthHandler
from app.common.utils.logger import setup_logger
from app.core.config import settings
from starlette.middleware.cors import CORSMiddleware
import sentry_sdk

Base.metadata.create_all(bind=engine)

app = FastAPI()

if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

logger = setup_logger(__name__)

app.include_router(authRouter)
app.include_router(userRouter)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"Error {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
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
            "success": False,
            "message": "Validation error",
            "errors": formatted_errors,
        },
    )


# format error 500
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        # Check if the response code indicates an error
        # if response.status_code >= 400:
        #     logger.error(f"Error {response.status_code}: {response.body.decode()}")
    except Exception as e:
        # Log the full stack trace for debugging
        logger.error(f"Error 500: {str(e)}", exc_info=True)
        # Return a more informative error response
        return JSONResponse(
            status_code=500,
            content={
                "status": False,
                "message": str(e),
            },
        )
    return response
