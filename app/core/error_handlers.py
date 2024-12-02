from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse


def register_error_handlers(app: FastAPI):
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred."},
        )
