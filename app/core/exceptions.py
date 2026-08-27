class AppError(Exception):
    def __init__(self, message: str = "Internal Server Error", status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppError):
    def __init__(self, message: str = "Resource Not Found", status_code: int = 404):
        super().__init__(message, status_code)


class ConflictError(AppError):
    def __init__(self, message: str = "Resource already exists", status_code: int = 409) -> None:
        super().__init__(message, status_code)


class BadRequestError(AppError):
    def __init__(self, message: str = "Bad request", status_code: int = 400) -> None:
        super().__init__(message, status_code)

class UnauthorizedError(AppError):
    def __init__(self, message: str = "Unauthorized access", status_code: int = 401) -> None:
        super().__init__(message, status_code)

class ForbiddenError(AppError):
    def __init__(self, message: str = "Forbidden access", status_code: int = 403) -> None:
        super().__init__(message, status_code)