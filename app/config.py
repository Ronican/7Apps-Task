from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field


# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = Field("PDFChatAPI", env="APP_NAME")
    APP_VERSION: str = Field("1.0.0", env="APP_VERSION")
    HOST: str = Field("0.0.0.0", env="HOST")
    PORT: int = Field(8000, env="PORT")

    # Database Configuration
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(5432, env="DB_PORT")
    DB_NAME: str = Field(..., env="DB_NAME")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")

    # Redis Configuration
    REDIS_HOST: str = Field("localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(6379, env="REDIS_PORT")
    REDIS_DB: int = Field(0, env="REDIS_DB")

    # Gemini API
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")

    # Sentry
    SENTRY_DSN: str = Field(None, env="SENTRY_DSN")

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
