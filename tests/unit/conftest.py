import pytest

from archer.models.training import TrainingData


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
def test_training_data_model(test_training_data_dict: dict) -> TrainingData:
    return TrainingData.model_validate(test_training_data_dict)
