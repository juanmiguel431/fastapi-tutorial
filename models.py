from enum import Enum
from pydantic import BaseModel, field_validator
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class Genre(Enum):
    Rock = 'Rock'
    Electronic = 'Electronic'
    Showgaze = 'Showgaze'
    HipHop = 'Hip-Hop'


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


class AlbumUpsertDto(BaseModel):
    title: str
    release_date: date


class BandUpsertDto(BaseModel):
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


class AlbumDto(BaseModel):
    title: str
    release_date: date


class BandDto(BaseModel):
    id: int
    name: str
    genre: Genre
    albums: list[AlbumDto] = []
