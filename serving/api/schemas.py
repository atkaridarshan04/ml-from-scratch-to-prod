from typing import List
from pydantic import BaseModel, Field


class HousingFeatures(BaseModel):
    longitude: float
    latitude: float
    housing_median_age: float
    total_rooms: float
    total_bedrooms: float
    population: float
    households: float
    median_income: float
    ocean_proximity: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "longitude": -122.23,
                    "latitude": 37.88,
                    "housing_median_age": 41,
                    "total_rooms": 880,
                    "total_bedrooms": 129,
                    "population": 322,
                    "households": 126,
                    "median_income": 8.3252,
                    "ocean_proximity": "NEAR BAY"
                }
            ]
        }
    }


class PredictionRequest(BaseModel):
    data: List[HousingFeatures]


class PredictionResponse(BaseModel):
    predictions: List[float]