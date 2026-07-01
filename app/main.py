from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from app.routers.todos import router as todos_router

app = FastAPI(title="FastAPI Example", version="0.1.0")

app.include_router(todos_router, prefix="/api/v1")


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict) and "code" in exc.detail:
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": "ERROR", "message": str(exc.detail)},
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
