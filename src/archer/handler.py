import json
import logging
from enum import IntEnum
from typing import Any

from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey
from pydantic import BaseModel, ConfigDict, Field

from archer.config import HandlerSettings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def verify_discord_request(headers: dict, body: str, public_key: str):
    """Verify an API Gateway request."""
    signature = headers["x-signature-ed25519"]
    timestamp = headers["x-signature-timestamp"]

    verify_key = VerifyKey(bytes.fromhex(public_key))
    verify_key.verify(
        f"{timestamp}{body}".encode(),
        bytes.fromhex(signature),
    )
    logger.info("Discord request signature verified successfully.")


class InteractionType(IntEnum):
    PING = 1


class InteractionResponseType(IntEnum):
    PONG = 1


class DiscordInteraction(BaseModel):
    """Common envelope shared by Discord interaction payloads."""

    type: InteractionType
    data: dict[str, Any] | None = Field(default_factory=dict)

    model_config = ConfigDict(extra="allow")


def api_response(payload: dict, status_code: int = 200) -> dict:
    """Return a JSON API Gateway response."""
    return {"statusCode": status_code, "body": json.dumps(payload)}


def lambda_handler(event, context):
    """
    Discord Interactions endpoint handler
    Verifies Discord signatures and handles interaction types
    """
    logger.info(f"{event}")
    settings = HandlerSettings()
    headers = event["headers"]
    body = event["body"]

    try:
        verify_discord_request(headers, body, settings.archer_public_key)
    except BadSignatureError as exc:
        logger.warning(f"invalid request signature: {exc}")
        return api_response({"error": "invalid request signature"}, 401)

    logger.info(f"body: {body}")
    interaction = DiscordInteraction.model_validate_json(body)

    if interaction.type == InteractionType.PING:
        return api_response({"type": InteractionResponseType.PONG})
