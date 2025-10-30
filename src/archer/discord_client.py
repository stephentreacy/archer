from typing import Any

import requests

from archer.models.embed import Embed


class DiscordAPIClient:
    def __init__(self, bot_token: str, attendance_channel_id: str):
        self.bot_token = bot_token
        self.attendance_channel_id = attendance_channel_id
        self.base_url = "https://discord.com/api/v10"
        self.session = requests.Session()
        self.session.headers.update(
            {"Authorization": f"Bot {bot_token}", "Content-Type": "application/json"}
        )

    def _send_request(
        self,
        url: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        response = self.session.post(f"{url}", json=payload)
        response.raise_for_status()
        return response.json()

    def send_embedded_messages(
        self,
        channel_id: str,
        embeds: list[Embed],
    ) -> None:
        payload = {"embeds": [embed.model_dump() for embed in embeds]}
        self._send_request(f"{self.base_url}/channels/{channel_id}/messages", payload)
