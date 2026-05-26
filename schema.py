from enum import Enum
from pydantic import BaseModel, field_validator
from datetime import date


class Genre(Enum):
    Rock = 'Rock'
    Electronic = 'Electronic'
    Showgaze = 'Showgaze'
    HipHop = 'Hip-Hop'


class Album(BaseModel):
    title: str
    release_date: date


class Band(BaseModel):
    id: int
    name: str
    genre: Genre
    albums: list[Album] = []

class BandUpsertDto(BaseModel):
    name: str
    genre: Genre
    albums: list[Album] = []

    @field_validator('genre', mode='before')
    @classmethod
    def normalize_genre(cls, value):
        if isinstance(value, str):
            normalized = value.lower()

            for genre in Genre:
                if genre.value.lower() == normalized:
                    return genre

        return value
