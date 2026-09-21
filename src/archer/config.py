from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings

from archer.models.training import TrainingData


class DiscordConfig(BaseSettings):
    discord_token: str = Field(..., repr=False)  # Hide from repr/errors
    attendance_channel_id: int
    training_data: TrainingData

    model_config = ConfigDict(env_file=".env", extra="ignore")


class HandlerSettings(BaseSettings):
    archer_public_key: str = Field(..., repr=False)

    model_config = ConfigDict(env_file=".env", extra="ignore")
