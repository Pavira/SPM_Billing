from fastapi import HTTPException, status
from app.schemas.common import SuccessResponse, ErrorResponse


def success_response(data=None, message="Operation successful", status_code=200):
    """Generate success response"""
    return {"status": "success", "message": message, "data": data}


def error_response(
    detail: str, message: str = "Operation failed", status_code: int = 400
):
    """Generate error response"""
    raise HTTPException(
        status_code=status_code,
        detail={"status": "error", "message": message, "detail": detail},
    )
