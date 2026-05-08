import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import diary_router
from app.core.exceptions import LLMTimeoutException
from app.core.logger import get_logger

app = FastAPI(title = "Health Diary NLP API")

logger = get_logger("API_GATEWAY")

# API

app.include_router(diary_router.router, prefix="/v1/api")

# exceptions

@app.exception_handler(LLMTimeoutException)
async def llm_timeout_handler(request: Request, exc: LLMTimeoutException):
    return JSONResponse(
        status_code=504,
        content={
            "message" : "LLM 요청 처리 중 타임아웃 발생. 잠시 후 다시 시도해주세요."
        }
    )

# middlewares

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()

    response  = await call_next(request)

    process_time = time.perf_counter() - start_time
    logger.info(
        f"Method: {request.method} | "
        f"Path: {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Latency: {process_time:.2f}s"
    )

    return response