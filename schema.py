from enum import Enum
from pydantic import BaseModel
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
