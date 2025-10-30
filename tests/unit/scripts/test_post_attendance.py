import json
from datetime import date
from pathlib import Path
from unittest.mock import Mock

import pytest

from archer.discord_client import DiscordAPIClient
from archer.models.embed import EmbedField
from archer.models.training import TrainingData, TrainingSession
from archer.scripts.post_attendance import (
    get_training_sessions,
    load_training_data,
    post_training,
)


@pytest.fixture
def test_training_data_dict() -> dict:
    return {
        "indoor": {
            "start_date": "2025-01-01",
            "end_date": "2025-02-28",
            "training_sessions": {
                "Monday": [
                    {
                        "time": "07:00-09:00",
                        "name": "Development Squad Training",
                        "location": "Kingfisher (Hall 3)",
                    },
                    {
                        "time": "17:00-20:00",
                        "name": "Advanced Training",
                        "location": "Kingfisher (Hall 3)",
                    },
                ],
                "Tuesday": [
                    {
                        "time": "07:00-09:00",
                        "name": "Development Squad Training",
                        "location": "Kingfisher (Hall 3)",
                    }
                ],
            },
        },
        "outdoor": {
            "start_date": "2025-02-01",
            "end_date": "2025-03-31",
            "training_sessions": {
                "Tuesday": [
                    {
                        "time": "14:00-18:00",
                        "name": "Outdoor Training",
                        "location": "Dangan",
                    }
                ]
            },
        },
    }


@pytest.fixture
def test_training_file(tmp_path: Path, test_training_data_dict: dict):
    temp_file = tmp_path / "test_trainings.json"
    temp_file.write_text(json.dumps(test_training_data_dict))
    return temp_file


@pytest.fixture
def test_training_data_model(test_training_data_dict: dict) -> TrainingData:
    return TrainingData.model_validate(test_training_data_dict)


@pytest.fixture
def discord_client_mock():
    return Mock(spec=DiscordAPIClient, attendance_channel_id=123)


class TestPostAttendance:
    def test_load_training_data(
        self, test_training_file: Path, test_training_data_model: TrainingData
    ):
        training_data = load_training_data(
            file_path=test_training_file,
        )
        assert training_data == test_training_data_model

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
