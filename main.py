from typing import Annotated
from sqlalchemy import func
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import HTMLResponse
from models import Band, Genre, BandUpsertDto, BandDto, Album
from contextlib import asynccontextmanager
from db import create_db_and_tables, SessionDep
from sqlmodel import select


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load
    create_db_and_tables()

    yield
    # Clean up

app = FastAPI(lifespan=lifespan)


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
        session: SessionDep,
        genre: Genre | None = None,
        has_albums: bool | None = None,
        q: Annotated[str | None, Query(min_length=4, max_length=10)] = None,
) -> list[BandDto]:
    statement = select(Band)

    if genre:
        statement = statement.where(Band.genre == genre)

    if has_albums:
        statement = statement.where(Band.albums.any())
    elif has_albums is False:
        statement = statement.where(~Band.albums.any())

    if q:
        statement = statement.where(
            func.lower(Band.name).contains(q.lower())
        )

    bands = session.exec(statement).all()

    dto_bands = [BandDto.from_entity(b) for b in bands]

    return dto_bands


@app.get('/bands/{band_id}', response_model=BandDto)
def get_band(
        session: SessionDep,
        band_id: Annotated[int, Path(title='The band id')],
) -> BandDto:
    band = session.get(Band, band_id)

    if  band is None:
        raise HTTPException(status_code=404, detail='Band not found')

    dto = BandDto.from_entity(band)
    return dto


@app.get('/bands/genre/{genre}', response_model=list[BandDto])
def get_band_by_genre(
        session: SessionDep,
        genre: Genre,
) -> list[BandDto]:
    statement = select(Band).where(Band.genre == genre)
    bands = session.exec(statement).all()

    dto_bands = [BandDto.from_entity(b) for b in bands]
    return dto_bands


@app.post('/bands', response_model=BandDto)
def create_band(
        session: SessionDep,
        payload: BandUpsertDto,
) -> BandDto:
    band = Band(name=payload.name, genre=payload.genre)
    session.add(band)

    if payload.albums:
        for album in payload.albums:
            album_obj = Album(title=album.title, release_date=album.release_date, band=band)
            session.add(album_obj)

    session.commit()
    session.refresh(band)

    dto = BandDto.from_entity(band)
    return dto
