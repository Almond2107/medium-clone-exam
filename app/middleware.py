import time

from fastapi.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware


class SimplePrintLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print("Before request")
        response = await call_next(request)
        print("After request")

        return response


class ProcessTimeLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        return response


# CORS middleware

origins = [
    "http://localhost:3000",
]