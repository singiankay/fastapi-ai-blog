from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra="allow")
    openai_api_key: str
    database_url: str
    database_port: str
    database_user: str
    database_password: str
    database_name: str
    echo_sql: bool = True
    test: bool = False
    project_name: str = "My FastAPI project"

    # class Config:
    #     env_file = ".env"
    #     extra = "allow"  # this all


settings = Settings(
    env_file='.env', env_file_encoding='utf-8')  # type: ignore
