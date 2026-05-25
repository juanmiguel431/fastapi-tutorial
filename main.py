from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from typing import TypedDict

app = FastAPI()


class Band(TypedDict):
    id: int
    name: str
    genre: str


BANDS: list[Band] = [
    {'id': 1, 'name': 'The Kings', 'genre': 'Rock'},
    {'id': 2, 'name': 'The Rolling Stones', 'genre': 'Rock'},
    {'id': 3, 'name': 'The Beatles', 'genre': 'Rock'},
    {'id': 4, 'name': 'Pink Floyd', 'genre': 'Rock'},
    {'id': 5, 'name': 'The Who', 'genre': 'Rock'},
    {'id': 6, 'name': 'Aphex Twin', 'genre': 'Electronic'},
    {'id': 7, 'name': 'Slowdive', 'genre': 'Showgaze'},
    {'id': 8, 'name': 'Wu-Tang Clan', 'genre': 'Hip-Hop'},
]

@app.get('/')
def index() -> dict[str, str]:
    return {'Hello': 'World'}


@app.get('/items/{item_id}')
def get_item(item_id: int, q: str | None = None):
    return {'item_id': item_id, 'q': q}


@app.get('/about', response_class=HTMLResponse)
def about() -> str:
    return 'An exceptional company'

@app.get('/bands')
def get_bands() -> list[Band]:
    return BANDS


@app.get('/bands/{band_id}')
def get_band(band_id: int) -> Band | None:
    band = next((b for b in BANDS if b['id'] == band_id), None)
    return band

