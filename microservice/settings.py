from pydantic import BaseSettings


class Settings(BaseSettings):
    AUTHENTICATION_HEADER_PREFIX: str
    SECRET_KEY: str
    HASH_ALGORITHM: str
    AWS_DYNAMODB_REGION: str
    AWS_ACCESS_KEY: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_DYNAMODB_TABLE_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
