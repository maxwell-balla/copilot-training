import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions.domain import DuplicateEmailException, EmployeeNotFoundException

logger = logging.getLogger(__name__)

PROBLEM_JSON = "application/problem+json"


def _problem(status_code: int, detail: str, **extra) -> JSONResponse:
    body = {"type": "about:blank", "title": _title_for(status_code), "status": status_code, "detail": detail}
    body.update(extra)
    return JSONResponse(status_code=status_code, content=body, media_type=PROBLEM_JSON)


def _title_for(status_code: int) -> str:
    return {
        status.HTTP_400_BAD_REQUEST: "Bad Request",
        status.HTTP_404_NOT_FOUND: "Not Found",
        status.HTTP_409_CONFLICT: "Conflict",
    }.get(status_code, "Error")


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(EmployeeNotFoundException)
    async def _not_found(_: Request, exc: EmployeeNotFoundException):
        return _problem(status.HTTP_404_NOT_FOUND, str(exc))

    @app.exception_handler(DuplicateEmailException)
    async def _duplicate(_: Request, exc: DuplicateEmailException):
        return _problem(status.HTTP_409_CONFLICT, str(exc))

    @app.exception_handler(RequestValidationError)
    async def _validation(_: Request, exc: RequestValidationError):
        errors: dict[str, str] = {}
        for err in exc.errors():
            loc = [p for p in err["loc"] if p not in ("body", "query", "path")]
            field = ".".join(str(p) for p in loc) or "request"
            errors.setdefault(field, err.get("msg", "invalid"))
        return _problem(
            status.HTTP_400_BAD_REQUEST, "Validation failed", errors=errors
        )
