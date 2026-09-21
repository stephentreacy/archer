from pydantic_settings import BaseSettings, SettingsConfigDict


class CdkSettings(BaseSettings):
    archer_public_key: str

    model_config = SettingsConfigDict(extra="ignore")
