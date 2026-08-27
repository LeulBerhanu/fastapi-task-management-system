from app.core.exceptions import AppError, NotFoundError, ConflictError, BadRequestError, UnauthorizedError, ForbiddenError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

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

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(NotFoundError, not_found_error_handler)
    app.add_exception_handler(ConflictError, conflict_error_handler)
    app.add_exception_handler(BadRequestError, bad_request_error_handler)
    app.add_exception_handler(UnauthorizedError, unauthorized_error_handler)
    app.add_exception_handler(ForbiddenError, forbidden_error_handler)