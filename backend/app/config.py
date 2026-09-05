import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ojone.db")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    USDA_API_KEY: str = os.getenv("USDA_API_KEY", "")

    # App metadata
    APP_NAME: str = "OjoneAI"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = (
        "AI-powered food tracking and calorie coaching assistant"
    )

    # CORS — allow all origins for hackathon demo
    CORS_ORIGINS: list[str] = ["*"]


settings = Settings()
