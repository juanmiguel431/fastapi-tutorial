from enum import Enum
from pydantic import BaseModel
from datetime import date


class Genre(Enum):
    Rock = 'rock'
    Electronic = 'electronic'
    Showgaze = 'showgaze'
    HipHop = 'hip-hop'


class Album(BaseModel):
    title: str
    release_date: date


class Band(BaseModel):
    id: int
    name: str
    genre: str
    albums: list[Album] = []
