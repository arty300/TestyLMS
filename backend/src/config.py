from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017/lms"
    SECRET_KEY: str = "your-secret-key"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

settings = Settings()