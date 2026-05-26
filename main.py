from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import HTMLResponse
from models import Band, Genre, BandUpsertDto, BandDto
from contextlib import asynccontextmanager
from db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load
    create_db_and_tables()

    yield
    # Clean up

app = FastAPI(lifespan=lifespan)


RAW_BANDS: list = [
    {'id': 1, 'name': 'The Kings', 'genre': 'Rock'},
    {'id': 2, 'name': 'The Rolling Stones', 'genre': 'Rock'},
    {'id': 3, 'name': 'The Beatles', 'genre': 'Rock'},
    {'id': 4, 'name': 'Pink Floyd', 'genre': 'Rock', 'albums': [
        {'title': 'Abbey Road', 'release_date': '1969-07-21'},
    ]},
    {'id': 5, 'name': 'The Who', 'genre': 'Rock'},
    {'id': 6, 'name': 'Aphex Twin', 'genre': 'Electronic'},
    {'id': 7, 'name': 'Slowdive', 'genre': 'Showgaze'},
    {'id': 8, 'name': 'Wu-Tang Clan', 'genre': 'Hip-Hop'},
]

BANDS: list[BandDto] = [BandDto(**b) for b in RAW_BANDS]

@app.get('/')
def index() -> dict[str, str]:
    return {'Hello': 'World'}


@app.get('/items/{item_id}')
def get_item(item_id: int, q: Annotated[str | None, Query(max_length=5)] = None):
    return {'item_id': item_id, 'q': q}


@app.get('/about', response_class=HTMLResponse)
def about() -> str:
    return 'An exceptional company'

@app.get('/bands')
def get_bands(
        genre: Genre | None = None,
        has_albums: bool | None = None,
        q: Annotated[str | None, Query(min_length=4, max_length=10)] = None,
) -> list[BandDto]:
    bands = BANDS

    if  genre:
        bands = [b for b in bands if b.genre == genre]

    if has_albums is not None:
        bands = [b for b in bands if bool(b.albums) == has_albums]

    if q:
        bands = [b for b in bands if q.lower() in b.name.lower()]

    return bands


@app.get('/bands/{band_id}', response_model=BandDto)
def get_band(band_id: Annotated[int, Path(title='The band id')]) -> BandDto:
    band = next((b for b in BANDS if b.id == band_id), None)

    if  band is None:
        raise HTTPException(status_code=404, detail='Band not found')

    return band

@app.get('/bands/genre/{genre}', response_model=list[BandDto])
def get_band_by_genre(genre: Genre) -> list[BandDto]:
    bands = [b for b in BANDS if b.genre == genre]
    return bands


@app.post('/bands', response_model=BandDto)
def create_band(payload: BandUpsertDto) -> BandDto:
    band_id = BANDS[-1].id + 1
    band = BandDto(id=band_id, **payload.model_dump())

    BANDS.append(band)
    RAW_BANDS.append(band.model_dump())

    return band
