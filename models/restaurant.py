from __future__ import annotations
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

class RestaurantBase(BaseModel):
    name: str = Field(..., description="Name of the restaurant", json_schema_extra={"example": "Joe's Pizza"})
    cuisine: str = Field(..., description="Type of cuisine", json_schema_extra={"example": "Italian"})
    city_id: UUID = Field(..., description="UUID of the city where the restaurant is located", json_schema_extra={"example": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"})
    rating: Optional[float] = Field(None, description="Average rating (0-5)", json_schema_extra={"example": 4.5})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "Joe's Pizza", "cuisine": "Italian", "city_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa", "rating": 4.5},
                {"name": "Sushi Place", "cuisine": "Japanese", "city_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb", "rating": 4.8},
            ]
        }
    }

class RestaurantCreate(RestaurantBase):
    model_config = RestaurantBase.model_config

class RestaurantUpdate(BaseModel):
    name: Optional[str] = Field(None, json_schema_extra={"example": "Pizzeria Uno"})
    cuisine: Optional[str] = Field(None, json_schema_extra={"example": "American"})
    city_id: Optional[UUID] = Field(None, description="UUID of the city", json_schema_extra={"example": "cccccccc-cccc-4ccc-8ccc-cccccccccccc"})
    rating: Optional[float] = Field(None, description="Average rating", json_schema_extra={"example": 4.7})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "New Place"},
                {"cuisine": "Mexican"},
                {"rating": 4.9},
            ]
        }
    }

class RestaurantRead(RestaurantBase):
    id: UUID = Field(default_factory=uuid4, description="Server-generated Restaurant ID", json_schema_extra={"example": "cccccccc-cccc-4ccc-8ccc-cccccccccccc"})
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp", json_schema_extra={"example": "2025-01-15T10:20:30Z"})
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp", json_schema_extra={"example": "2025-01-16T12:00:00Z"})

    model_config = RestaurantBase.model_config
