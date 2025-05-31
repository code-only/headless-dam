# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_DB: str

    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    ES_HOST: str
    ES_INDEX: str = "assets"

    STORAGE_TYPE: str = "local"  # or "s3"
    ASSET_LOCAL_DIR: str = "./uploaded_assets"
    
    S3_BUCKET: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_REGION: str

    class Config:
        env_file = ".env"

settings = Settings()
