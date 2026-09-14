from enum import StrEnum
from functools import lru_cache
from urllib.parse import quote
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr

class EnvironmentOptions(StrEnum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    TESTING = "testing"
    PRODUCTION = "production"

class AppSettings(BaseSettings):
    APP_NAME: str
    API_PREFIX: str = "/api"

class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOptions = EnvironmentOptions.DEVELOPMENT

class PostgresSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DB: int

class DatabaseSettings(BaseSettings):
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

class RateLimitSettings(BaseSettings):
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_WINDOW: int = 60
    RATE_LIMIT_LIMIT: int = 100

class Settings(
    EnvironmentSettings, 
    DatabaseSettings, 
    PostgresSettings, 
    AuthSettings, 
    EmailSettings, 
    AppSettings, 
    RedisSettings,
    RateLimitSettings
    ):

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def REDIS_URL(self) -> str:
        password = quote(self.REDIS_PASSWORD, safe="")
        return f"redis://:{password}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @property
    def RATE_LIMIT_DEFAULT(self) -> str:
        return f"{self.RATE_LIMIT_LIMIT} per {self.RATE_LIMIT_WINDOW} seconds"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == EnvironmentOptions.PRODUCTION

    
@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()