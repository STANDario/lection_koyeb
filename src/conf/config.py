from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "dev"
    postgres_db: str = "database_name"
    postgres_user: str = "user"
    postgres_password: str = "password"
    postgres_port: int = 5432
    sqlalchemy_database_url: str = "postgresql+psycopg2://user:password@localhost:5432/postgres"
    secret_key: str = "secret_key"
    algorithm: str = "HS256"
    mail_username: str = "example@meta.ua"
    mail_password: str = "password"
    mail_from: str = "example@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.meta.ua"
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloudinary_name: str = "name"
    cloudinary_api_key: int = 412785245648512
    cloudinary_api_secret: str = "secret_key"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
