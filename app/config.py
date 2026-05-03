from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    model_name: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"
    chroma_persist_dir: str = "./chroma_db"
    docs_dir: str = "./docs"

    class Config:
        env_file = ".env"


settings = Settings()
