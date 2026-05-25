from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()


class Band(BaseModel):
    id: int
    name: str
    genre: str


BANDS: list[Band] = [
    Band(id= 1, name='The Kings', genre='Rock'),
    Band(id= 2, name='The Rolling Stones', genre='Rock'),
    Band(id= 3, name='The Beatles', genre='Rock'),
    Band(id= 4, name='Pink Floyd', genre='Rock'),
    Band(id= 5, name='The Who', genre='Rock'),
    Band(id= 6, name='Aphex Twin', genre='Electronic'),
    Band(id= 7, name='Slowdive', genre='Showgaze'),
    Band(id= 8, name='Wu-Tang Clan', genre='Hip-Hop'),
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


@app.get('/bands/{band_id}', response_model=Band)
def get_band(band_id: int) -> Band:
    band = next((b for b in BANDS if b.id == band_id), None)

    if  band is None:
        raise HTTPException(status_code=404, detail='Band not found')

    return band

@app.get('/bands/genre/{genre}', response_model=list[Band])
def get_band(genre: str) -> list[Band]:
    bands = [b for b in BANDS if b.genre.lower() == genre.lower()]
    return bands

