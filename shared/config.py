import os

class Config:
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_REAL_HOST: str = os.getenv("DB_REAL_HOST")
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
    DATABASE_REAL_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_REAL_HOST}:5432/{DB_NAME}"
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    NOREPLY_EMAIL: str = os.getenv("NOREPLY_EMAIL")
    NOREPLY_PASSWORD: str = os.getenv("NOREPLY_PASSWORD")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT")