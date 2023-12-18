from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import Annotated

PortNumber = Annotated[int, Field(gt=0, le=65535)]


class DbSettings(BaseSettings):
    db: str
    user: str
    password: str
    mapping_port: PortNumber


class TgBotSettings(BaseSettings):
    token: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra="allow",
        env_nested_delimiter='__',  # delimiter between nested submodels, naming example: POSTGRES__PASSWORD
    )

    postgres: DbSettings
    tg_bot: TgBotSettings
