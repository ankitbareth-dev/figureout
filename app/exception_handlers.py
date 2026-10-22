
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.errors import ErrorBody, ErrorDetail, ErrorResponse


async def validation_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    if not isinstance(exc, RequestValidationError):
        raise exc

    details: list[ErrorDetail] = []

    for error in exc.errors():
        location = error["loc"]
        field = str(location[-1]) if location else "request"

        details.append(
            ErrorDetail(
                field=field,
                message=error["msg"],
            )
        )

    response = ErrorResponse(
        error=ErrorBody(
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details=details,
        )
    )

    return JSONResponse(
        status_code=422,
        content=response.model_dump(),
    )


async def http_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    if not isinstance(exc, HTTPException):
        raise exc

    response = ErrorResponse(
        error=ErrorBody(
            code=f"HTTP_{exc.status_code}",
            message=(
                exc.detail
                if isinstance(exc.detail, str)
                else "Request failed"
            ),
            details=[],
        )
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(),
        headers=exc.headers,
    )
