from archer.discord_client import DiscordAPIClient


class TestDiscordAPIClient:
    """Test suite for DiscordAPIClient."""

    def test_init_sets_correct_attributes(self):
        """Test that initialization sets all required attributes correctly."""
        bot_token = "test_token_123"
        channel_id = "987654321"

        client = DiscordAPIClient(bot_token, channel_id)

        assert client.bot_token == bot_token
        assert client.attendance_channel_id == channel_id
        assert client.base_url == "https://discord.com/api/v10"
