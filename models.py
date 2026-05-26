from enum import Enum
from typing import Any, Self

from pydantic import BaseModel, field_validator, ConfigDict
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class Genre(Enum):
    ROCK = 'Rock'
    ELECTRONIC = 'Electronic'
    SHOWGAZE = 'Showgaze'
    HIP_HOP = 'Hip-Hop'


class Album(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    release_date: date
    band_id: int = Field(foreign_key='band.id')
    band: 'Band' = Relationship(back_populates='albums')


class Band(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    genre: Genre
    albums: list[Album] = Relationship(back_populates='band')
    date_formed: date | None


class BaseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_entity(cls, entity: Any) -> Self:
        return cls.model_validate(entity)

class AlbumUpsertDto(BaseDto):
    title: str
    release_date: date


class BandUpsertDto(BaseDto):
    name: str
    genre: Genre
    albums: list[AlbumUpsertDto] = []

    @field_validator('genre', mode='before')
    @classmethod
    def normalize_genre(cls, value):
        if isinstance(value, str):
            normalized = value.lower()

            for genre in Genre:
                if genre.value.lower() == normalized:
                    return genre

        return value


class AlbumDto(BaseDto):
    id: int
    title: str
    release_date: date


class BandDto(BaseDto):
    id: int
    name: str
    genre: Genre
    albums: list[AlbumDto] = []
