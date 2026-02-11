# import os
# from pydantic_settings import BaseSettings


# class Settings(BaseSettings):
#     # Firebase
#     FIREBASE_CREDENTIALS_PATH: str = os.getenv(
#         "FIREBASE_CREDENTIALS_PATH", "./firebase-credentials.json"
#     )

#     # CORS
#     ALLOWED_ORIGINS: list = [
#         "http://localhost:5173",
#         "http://localhost:3000",
#         "http://127.0.0.1:5173",
#         "http://127.0.0.1:3000",
#     ]

#     # Database (optional - if you need a database)
#     DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

#     # API Keys
#     SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")

#     # Logging
#     LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

#     class Config:
#         env_file = ".env"
#         case_sensitive = True


# settings = Settings()
