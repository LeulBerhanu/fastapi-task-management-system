from enum import StrEnum
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr

class EnvironmentOptions(StrEnum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    TESTING = "testing"
    PRODUCTION = "production"

class AppSettings(BaseSettings):
    APP_NAME: str

class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOptions = EnvironmentOptions.DEVELOPMENT

class DatabaseSettings(BaseSettings):
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 5
    DATABASE_POOL_MAX_OVERFLOW: int = 10
    DATABASE_POOL_PRE_PING: bool = True

class AuthSettings(BaseSettings):
    JWT_SECRET_KEY: str
    HASH_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

class EmailSettings(BaseSettings):
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: EmailStr
    EMAIL_PORT: int = 587
    EMAIL_SERVER: str = "smtp.gmail.com"
    EMAIL_STARTTLS: bool = True
    EMAIL_SSL_TLS: bool = False

class Settings(EnvironmentSettings, DatabaseSettings, AuthSettings, EmailSettings, AppSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == EnvironmentOptions.PRODUCTION

    
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()