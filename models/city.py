from __future__ import annotations
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field

class CityBase(BaseModel):
    name: str = Field(..., description="Name of the city", json_schema_extra={"example": "New York"})
    country: str = Field(..., description="Country of the city", json_schema_extra={"example": "USA"})
    population: Optional[int] = Field(None, description="Population of the city", json_schema_extra={"example": 8419000})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "New York", "country": "USA", "population": 8419000},
                {"name": "Paris", "country": "France", "population": 2148000},
            ]
        }
    }

class CityCreate(CityBase):
    model_config = CityBase.model_config

class CityUpdate(BaseModel):
    name: Optional[str] = Field(None, json_schema_extra={"example": "San Francisco"})
    country: Optional[str] = Field(None, json_schema_extra={"example": "USA"})
    population: Optional[int] = Field(None, json_schema_extra={"example": 870000})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "Los Angeles"},
                {"population": 4000000},
                {"country": "Germany"},
            ]
        }
    }

class CityRead(CityBase):
    id: UUID = Field(default_factory=uuid4, description="Server-generated City ID", json_schema_extra={"example": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"})
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp", json_schema_extra={"example": "2025-01-15T10:20:30Z"})
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp", json_schema_extra={"example": "2025-01-16T12:00:00Z"})

    model_config = CityBase.model_config
    