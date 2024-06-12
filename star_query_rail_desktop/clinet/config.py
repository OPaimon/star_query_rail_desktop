from pydantic import BaseSettings
from star_query_rail_client import AuthenticatedClient, Client


class Settings(BaseSettings):
    API_url: str = "http://localhost:8000"


class Status(BaseSettings):
    _instance = None
    email: str | None = None
    userid: int | None = None
    character: list[int] | None = None
    token: str | None = None


settings = Settings()
status = Status()
