# app/schemas.py

from pydantic import BaseModel, Field, validator
from typing import Tuple, List, Optional
from datetime import date, datetime


class PreferenceInput(BaseModel):
    """
    Schema for user preferences input.
    """
    budget: Tuple[int, int] = Field(..., example=[250, 8])
    check_in: Tuple[date, int] = Field(..., example=["2024-05-01", 7])
    check_out: Tuple[date, int] = Field(..., example=["2024-05-10", 7])
    neigh_name: Tuple[str, int] = Field(..., example=["Downtown", 10])

    @validator('budget')
    def budget_non_negative(cls, v):
        value, importance = v
        if value < 0:
            raise ValueError('Budget cannot be negative')
        if not 1 <= importance <= 10:
            raise ValueError('Budget importance coefficient must be between 1 and 10')
        return v

    @validator('check_in')
    def check_in_not_past(cls, v):
        check_in_date, importance = v
        today = date.today()
        if check_in_date < today:
            raise ValueError('Check-in date cannot be in the past')
        if not 1 <= importance <= 10:
            raise ValueError('Check-in importance coefficient must be between 1 and 10')
        return v

    @validator('check_out')
    def check_out_after_check_in(cls, v, values):
        check_out_date, importance = v
        check_in_date = values.get('check_in', (None, None))[0]
        if check_in_date and check_out_date < check_in_date:
            raise ValueError('Check-out date cannot be before check-in date')
        if not 1 <= importance <= 10:
            raise ValueError('Check-out importance coefficient must be between 1 and 10')
        return v

    @validator('neigh_name')
    def neigh_name_not_empty(cls, v):
        neigh_name, importance = v
        if not neigh_name:
            raise ValueError('Neighborhood name cannot be empty')
        if not 1 <= importance <= 10:
            raise ValueError('Neighborhood importance coefficient must be between 1 and 10')
        return v


class RoomSuggestion(BaseModel):
    """
    Schema for room suggestions in the response.
    """
    listing_id: int
    airbnb_name: str
    price: float
    host_id: int
    neigh_name: str
    room_type: str
    score: float
    attribute_scores: Optional[dict] = None  # Optional: Detailed scores per attribute


class SuggestionResponse(BaseModel):
    """
    Schema for the overall suggestion response.
    """
    suggestions: List[RoomSuggestion]