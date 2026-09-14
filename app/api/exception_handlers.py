from app.core.exceptions import AppError, NotFoundError, ConflictError, BadRequestError, UnauthorizedError, ForbiddenError, TooManyRequestsError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

async def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

async def conflict_error_handler(request: Request, exc: ConflictError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

async def bad_request_error_handler(request: Request, exc: BadRequestError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

async def unauthorized_error_handler(request: Request, exc: UnauthorizedError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

async def forbidden_error_handler(request: Request, exc: ForbiddenError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

async def too_many_requests_error_handler(request: Request, exc: TooManyRequestsError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"message": exc.message})

async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    response = JSONResponse(status_code=429, content={"message": "Too many requests"})
    view_rate_limit = getattr(request.state, "view_rate_limit", None)
    if view_rate_limit is not None:
        return request.app.state.limiter._inject_headers(response, view_rate_limit)
    return response

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(NotFoundError, not_found_error_handler)
    app.add_exception_handler(ConflictError, conflict_error_handler)
    app.add_exception_handler(BadRequestError, bad_request_error_handler)
    app.add_exception_handler(UnauthorizedError, unauthorized_error_handler)
    app.add_exception_handler(ForbiddenError, forbidden_error_handler)
    app.add_exception_handler(TooManyRequestsError, too_many_requests_error_handler)
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)