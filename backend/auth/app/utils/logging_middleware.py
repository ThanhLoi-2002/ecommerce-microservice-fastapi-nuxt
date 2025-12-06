from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from loguru import logger
import time
import json


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Log request nhận vào
        start_time = time.perf_counter()

        # Lấy thông tin cơ bản
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path
        query_params = str(request.url.query) if request.url.query else None

        # Đọc body (cẩn thận với stream)
        body = await request.body()
        body_str = body.decode("utf-8", errors="ignore") if body else None

        if body_str:
            try:
                body_json = json.loads(body_str)
                body_preview = json.dumps(body_json, ensure_ascii=False, indent=2)[:500]
            except json.JSONDecodeError:
                body_preview = body_str[:500]
        else:
            body_preview = None

        # Log request (chi tiết nhưng an toàn)
        logger.info(
            f"HTTP Request → {method} {path} | IP: {client_ip} | Query: {query_params}"
        )
        if body_preview:
            logger.info(f"\nRequest body: {body_preview}")

        # Gọi handler tiếp theo
        try:
            response = await call_next(request)
        except Exception as exc:
            # Log lỗi nếu handler crash
            duration = (time.perf_counter() - start_time) * 1000
            logger.exception(
                f"Request failed with exception | {method} {path} | Duration: {duration:.2f}ms"
            )
            raise

        # 2. Log response
        duration = (time.perf_counter() - start_time) * 1000
        status_code = response.status_code

        logger.info(
            f"HTTP Response ← {method} {path} | Status: {status_code} | {duration:.2f}ms | IP: {client_ip}"
        )

        return response
