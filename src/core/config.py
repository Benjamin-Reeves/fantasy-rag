from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Database settings
    db_user: str = "default_user"
    db_pass: str = "default_pass"
    db_name: str = "default_db"
    db_host: str = "localhost"
    db_port: str = "5432"

    # Embedding model settings
    embedding_model: str = "all-MiniLM-L6-v2"

    # API keys
    anthropic_api_key: str = ""


# Create a single instance to be imported throughout the app
settings = Settings()
