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
        crew = read.get_title_crew(db, id)
        directors = crew.directors.split(',')
        writers = crew.writers.split(',')
        names = read.get_name_basic(db, list({*directors, *writers}))
        crew.directors = [next(i for i in names if i.nconst == d) for d in directors]
        crew.writers = [next(i for i in names if i.nconst == w) for w in writers]
        return crew

@mediaRouter.get("/media/{id}/principals", tags=["media"])
async def get_media_principals(id: str, db: Session = Depends(get_db)):
        principals = read.get_title_principals(db, id)
        names = read.get_name_basic(db, list({p.nconst for p in principals}))
        for p in principals:
                p.name = next(n for n in names if n.nconst == p.nconst)
        return principals

@mediaRouter.get("/media/{id}/ratings", tags=["media"])
async def get_media_ratings(id: str, db: Session = Depends(get_db)):
        return read.get_title_ratings(db, id)

@mediaRouter.get("/media/{id}/episodes", tags=["media"])
async def get_media_episodes(id: str, db: Session = Depends(get_db)):
        return read.get_title_episodes(db, id)
