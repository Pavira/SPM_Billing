# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthCredentials
# from app.core.security import verify_token
# import logging

# logger = logging.getLogger(__name__)
# security = HTTPBearer()


# async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
#     """Extract and verify Firebase token from request headers"""
#     try:
#         token = credentials.credentials
#         decoded_token = await verify_token(token)
#         return decoded_token
#     except Exception as e:
#         logger.error(f"Authentication failed: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
