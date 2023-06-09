from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    APP_NAME: str = "KnowledgeAI"
    VERSION: str = "0.1.0"

    CWD = Path(__file__).parent
    DATA: Path = CWD.parent / "data"
    DATABASE: str = "docsearch.faiss"

    BACKEND: str = "chat_gpt"
    MODEL: str = "gpt-3.5-turbo"
    TEMPERATURE: int = 0

    OPENAI_API_KEY: str = ""
    TAGLINE: str = "Ask a question"

    SYSTEM_PROMPT: str = (
        "You are a helpful assistant that answers questions."
        " If you are unsure about the answer politely decline and offer an original"
        " joke instead. No cheesy jokes about scientists or computer please!"
        " Stick to the language used in question."
    )

    # number of documents retrieved from the database
    TOP_K: int = 3

    LOG_QUESTIONS: bool = True
    LOG_ANSWERS: bool = True
    LOG_PROMPTS: bool = False

    class Config:
        """Read configuration from .env file."""

        env_file = ".env"


settings = Settings()
