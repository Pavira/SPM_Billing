from app.core.firebase import verify_firebase_token
import logging

logger = logging.getLogger(__name__)


async def verify_token(token: str):
    """Verify and decode Firebase token"""
    try:
        if not token:
            raise ValueError("Token not provided")

        # Remove 'Bearer ' prefix if present
        if token.startswith("Bearer "):
            token = token[7:]

        decoded_token = verify_firebase_token(token)
        return decoded_token
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise
