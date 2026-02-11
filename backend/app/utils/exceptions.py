from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base application exception"""

    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class AuthenticationError(AppException):
    """Authentication error"""

    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)


class AuthorizationError(AppException):
    """Authorization error"""

    def __init__(self, detail: str = "Not authorized"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


class NotFoundError(AppException):
    """Resource not found error"""

    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class ValidationError(AppException):
    """Validation error"""

    def __init__(self, detail: str = "Validation failed"):
        super().__init__(
            detail=detail, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
