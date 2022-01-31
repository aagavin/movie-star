from ctypes import Union
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import schemas, read
from . import get_db
import httpx

mediaRouter = APIRouter()

@mediaRouter.get("/media/{id}", tags=['media'])
async def get_media_by_id(id: str, full: bool | None = False, db: Session = Depends(get_db)):
        return read.get_title_basic(db, full, id)


@mediaRouter.get("/media/{id}/poster", tags=["media"])
async def get_media_poster(id: str, db: Session = Depends(get_db)):
        result = httpx.get(f'https://m.imdb.com/title/{id}/')
        imdbParse = read.ImdbParser()
        imdbParse.feed(result.text)
        return {"posterUrl": imdbParse.data}


@mediaRouter.get("/media/{id}/crew", tags=['media'])
async def get_media_crew(id: str, db: Session = Depends(get_db)):
        name_cache = {}
        crew = read.get_title_crew(db, id)
        crew.directors = read.get_name_basic(db, crew.directors.split(','))
        crew.writers = read.get_name_basic(db, crew.writers.split(','))
        return crew

@mediaRouter.get("/media/{id}/principals", tags=["media"])
async def get_media_principals(id: str, db: Session = Depends(get_db)):
        principals = read.get_title_principals(db, id)
        print(principals)
        for p in principals:
                print(p)
                p.name = read.get_name_basic(db, p.nconst)
        return principals

@mediaRouter.get("/media/{id}/ratings", tags=["media"])
async def get_media_ratings(id: str, db: Session = Depends(get_db)):
        return read.get_title_ratings(db, id)

@mediaRouter.get("/media/{id}/episodes", tags=["media"])
async def get_media_episodes(id: str, db: Session = Depends(get_db)):
        return read.get_title_episodes(db, id)
