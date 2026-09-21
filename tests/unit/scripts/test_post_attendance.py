from datetime import date
from unittest.mock import Mock

import pytest

from archer.discord_client import DiscordAPIClient
from archer.models.embed import EmbedField
from archer.models.training import TrainingData, TrainingSession
from archer.scripts.post_attendance import (
    get_training_sessions,
    post_training,
)


@pytest.fixture
def discord_client_mock():
    return Mock(spec=DiscordAPIClient, attendance_channel_id=123)


class TestPostAttendance:
    def test_get_training_sessions_indoor(self, test_training_data_model: TrainingData):
        indoor_monday_date = date(2025, 1, 6)  # Monday

        training_sessions = get_training_sessions(
            training_data=test_training_data_model, training_date=indoor_monday_date
        )
        assert (
            training_sessions
            == test_training_data_model.indoor.training_sessions["Monday"]
        )

    def test_get_training_sessions_outdoor(
        self, test_training_data_model: TrainingData
    ):
        outdoor_tuesday_date = date(2025, 3, 4)  # Tuesday

        training_sessions = get_training_sessions(
            training_data=test_training_data_model, training_date=outdoor_tuesday_date
        )
        assert (
            training_sessions
            == test_training_data_model.outdoor.training_sessions["Tuesday"]
        )

    def test_get_training_sessions_indoor_and_outdoor(
        self, test_training_data_model: TrainingData
    ):
        outdoor_tuesday_date = date(2025, 2, 4)  # Tuesday

        training_sessions = get_training_sessions(
            training_data=test_training_data_model, training_date=outdoor_tuesday_date
        )
        assert (
            training_sessions
            == test_training_data_model.indoor.training_sessions["Tuesday"]
            + test_training_data_model.outdoor.training_sessions["Tuesday"]
        )

    def test_indoor_training_sessions(self, discord_client_mock):
        test_date = date(2025, 1, 6)  # Monday

        sessions = [
            TrainingSession(
                name="Test Training", time="07:00-09:00", location="Test Location"
            )
        ]
        post_training(discord_client_mock, test_date, sessions)

        call_args = discord_client_mock.send_embedded_messages.call_args

        assert call_args[1]["channel_id"] == discord_client_mock.attendance_channel_id

        embed = call_args[1]["embeds"][0]

        assert embed.title == "Monday Test Training"
        assert embed.color

        assert len(embed.fields) == 3
        fields = embed.fields
        assert fields[0] == EmbedField(name="Date", value="06/01/25", inline=True)
        assert fields[1] == EmbedField(name="Time", value="07:00-09:00", inline=True)
        assert fields[2] == EmbedField(
            name="Location", value="Test Location", inline=True
        )
