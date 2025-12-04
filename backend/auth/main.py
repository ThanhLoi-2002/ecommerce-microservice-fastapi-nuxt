from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from app.modules.auth.authController import authRouter
from fastapi.responses import JSONResponse
from app.common.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

from app.common.utils.logger import setup_logger

logger = setup_logger(__name__)

app.include_router(authRouter)


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
    except Exception as e:
        # Ghi lại lỗi
        logger.error(f"Error 500: {str(e)}")
        # Trả về thông báo lỗi với mã 500
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error", "error": str(e)},
        )
    return response
