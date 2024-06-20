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

    sqlalchemy_database_uri: str = "sqlite:///./test.db"


settings = Settings()