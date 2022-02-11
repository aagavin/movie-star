from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session

from src.database import schemas, read
from . import get_db
import httpx

mediaRouter = APIRouter()


@mediaRouter.get("/media/{id}", tags=['media'])
async def get_media_by_id(id: str, full: bool | None = False, response=Response, db: Session = Depends(get_db)):
    result = read.get_title_basic(db, full, id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No media with id {id}"
        )
    return result


@mediaRouter.get("/media/{id}/poster", tags=["media"])
async def get_media_web_data(id: str):
    return get_media_poster(id)


@mediaRouter.get("/media/{id}/webdata", tags=["media"])
async def get_media_web_data_v2(id: str):
    return get_media_poster(id)


def get_media_poster(id: str):
    result = httpx.get(f'https://m.imdb.com/title/{id}/')
    imdbParse = read.ImdbParser()
    imdbParse.feed(result.text)
    return {"posterUrl": imdbParse.posterUrl, "description": imdbParse.description}


@mediaRouter.get("/media/{id}/crew", tags=['media'])
async def get_media_crew(id: str, db: Session = Depends(get_db)):
    crew = read.get_title_crew(db, id)
    directors = crew.directors.split(',')
    writers = crew.writers.split(',')
    names = read.get_name_basic(db, list({*directors, *writers}))
    crew.directors = [next(i for i in names if i.nconst == d)
                      for d in directors]
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
