from datetime import date

from pydantic import BaseModel


class TrainingSession(BaseModel):
    name: str
    time: str
    location: str


class SeasonSchedule(BaseModel):
    start_date: date
    end_date: date
    training_sessions: dict[str, list[TrainingSession]]


class TrainingData(BaseModel):
    indoor: SeasonSchedule
    outdoor: SeasonSchedule
