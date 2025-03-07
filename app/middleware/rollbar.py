import rollbar
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def setup_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        level = "error"
        if exc.status_code < 500:
            level = "warning" if exc.status_code >= 400 else "info"

        request_data = {
            "url": str(request.url),
            "method": request.method,
            "headers": dict(request.headers),
            "client": request.client.host if request.client else None,
        }

        rollbar.report_message(
            f"HTTP {exc.status_code}: {exc.detail}",
            level=level,
            request=request,
            extra_data={"request_info": request_data},
        )

        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        rollbar.report_message(
            "Request validation error", level="warning", request=request, extra_data={"errors": exc.errors()}
        )

        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": exc.errors()})

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        rollbar.report_exc_info(request=request)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal server error"}
        )
