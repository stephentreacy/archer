import json
import logging
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

from archer.config import DiscordConfig
from archer.discord_client import DiscordAPIClient
from archer.models.embed import Embed, EmbedField
from archer.models.training import TrainingData, TrainingSession

logger = logging.getLogger(__name__)


def load_training_data(
    file_path: Path = Path("src/archer/scripts/trainings.json"),
) -> TrainingData:
    """Load training data from the JSON file."""
    with Path.open(file_path) as f:
        data = json.load(f)
    return TrainingData.model_validate(data)


def get_training_sessions(
    training_data: TrainingData, training_date: date
) -> list[TrainingSession]:
    """Get training sessions scheduled on a date."""
    training_day = training_date.strftime("%A")
    training_sessions = []

    for season_schedule in [training_data.indoor, training_data.outdoor]:
        if season_schedule.start_date <= training_date <= season_schedule.end_date:
            sessions = season_schedule.training_sessions.get(training_day, [])
            training_sessions.extend(sessions)

    return training_sessions


def post_training(
    discord_client: DiscordAPIClient,
    training_date: date,
    training_sessions: list[TrainingSession],
) -> None:
    """Post training sessions in the attendance channel."""

    for training_session in training_sessions:
        logger.info(
            f"Posting session: {training_session.name} at {training_session.time}",
        )
        embed = Embed(
            title=f"{training_date.strftime('%A')} {training_session.name}",
            fields=[
                EmbedField(name="Date", value=training_date.strftime("%d/%m/%y")),
                EmbedField(name="Time", value=training_session.time),
                EmbedField(name="Location", value=training_session.location),
            ],
        )

        discord_client.send_embedded_messages(
            channel_id=discord_client.attendance_channel_id,
            embeds=[embed],
        )

    logger.info("Successfully posted all training sessions")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    config = DiscordConfig()
    training_data = load_training_data()

    tomorrow_date = datetime.now(UTC).date() + timedelta(days=1)

    training_sessions = get_training_sessions(
        training_data=training_data, training_date=tomorrow_date
    )
    discord_client = DiscordAPIClient(
        config.discord_token, config.attendance_channel_id
    )

    post_training(discord_client, tomorrow_date, training_sessions)
