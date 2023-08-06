from pydantic import BaseSettings


class Settings(BaseSettings):
    default_standard: str = "Bruce Schneier's Algorithm"


settings = Settings()
