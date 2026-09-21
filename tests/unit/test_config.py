import json

import pytest

from archer.config import DiscordConfig
from archer.models.training import TrainingData


@pytest.fixture
def mock_env(monkeypatch, test_training_data_dict: dict):
    monkeypatch.setenv("DISCORD_TOKEN", "test_token")
    monkeypatch.setenv("ATTENDANCE_CHANNEL_ID", "123")
    monkeypatch.setenv("TRAINING_DATA", json.dumps(test_training_data_dict))


class TestConfig:
    def test_discord_settings(self, mock_env, test_training_data_model: TrainingData):
        settings = DiscordConfig()
        assert settings.discord_token == "test_token"
        assert settings.attendance_channel_id == 123
        assert settings.training_data == test_training_data_model
