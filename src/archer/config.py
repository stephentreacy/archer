from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class DiscordConfig(BaseSettings):
    discord_token: str = Field(..., repr=False)  # Hide from repr/errors
    attendance_channel_id: int

    model_config = ConfigDict(env_file=".env", extra="ignore")
