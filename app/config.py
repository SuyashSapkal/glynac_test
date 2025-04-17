import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME = "Employee Performance Tracker"
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    ALGORITHM = "HS256"


settings = Settings()
