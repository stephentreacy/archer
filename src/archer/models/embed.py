import random

from pydantic import BaseModel, Field


class EmbedField(BaseModel):
    name: str = Field(..., max_length=256)
    value: str = Field(..., max_length=1024)
    inline: bool = True


class Embed(BaseModel):
    title: str = Field(..., max_length=256)
    color: int = Field(
        default_factory=lambda: random.randint(0, 0xFFFFFF), ge=0, le=0xFFFFFF
    )
    fields: list[EmbedField] = Field(..., max_length=25)
