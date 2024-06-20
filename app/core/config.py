from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = "localhost"
    environment: str = "development"

    app_name: str = "Library Management API"
    app_run_name: str = "main:app"
    app_version: str = "v1"
    api_port: int = 8000

    @property
    def api_version_str(self) -> str:
        return f"/api/{self.app_version}"

    postgres_server: str
    postgres_port: int = 5432
    postgres_user: str
    postgres_password: str
    postgres_db: str = ""

    @computed_field
    @property
    def sqlalchemy_database_uri(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_server,
            port=self.postgres_port,
            path=self.postgres_db,
        )
    
    init_db: bool


settings = Settings()
