from enum import Enum
from typing import Union
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.database import read
from . import get_db
import httpx

mediaRouter = APIRouter()

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0'}


class MediaType(Enum):
    MOVIE = "movie"
    TV = "tv"


@mediaRouter.get("/media/{type}/popular")
async def get_popular_media(type: MediaType):
    base_url = "https://www.imdb.com/chart"
    if type == MediaType.MOVIE:
        request_url = f"{base_url}/moviemeter"
    elif type == MediaType.TV:
        request_url = f"{base_url}/tvmeter"
    return await read.get_popular_media(request_url)


@mediaRouter.get("/media/{media_id}", tags=['media'])
async def get_media_by_id(media_id: str, full: bool | None = False, db: Session = Depends(get_db)):
    result = read.get_title_basic(db, full, media_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No media with id {media_id}"
        )
    return result


@mediaRouter.get("/media/{media_id}/webdata", tags=["media"])
async def get_media_web_data(media_id: str):
    result = httpx.get(f'https://m.imdb.com/title/{media_id}/', headers=headers)
    imdbParse = read.ImdbMediaParser()
    imdbParse.feed(result.text)
    return {"posterUrl": imdbParse.posterUrl, "description": imdbParse.description}


@mediaRouter.get("/media/{media_id}/poster", tags=["media"], response_class=RedirectResponse)
def get_media_poster(media_id: str):
    return f"/media/{media_id}/webdata"


@mediaRouter.get("/media/{media_id}/crew", tags=['media'])
async def get_media_crew(media_id: str, db: Session = Depends(get_db)):
    crew = read.get_title_crew(db, media_id)
    directors = crew.directors.split(',')
    writers = crew.writers.split(',')
    names = read.get_name_basic(db, list({*directors, *writers}))
    crew.directors = [next(i for i in names if i.nconst == d)
                      for d in directors]
    crew.writers = [next(i for i in names if i.nconst == w) for w in writers]
    return crew


@mediaRouter.get("/media/{media_id}/principals", tags=["media"])
async def get_media_principals(media_id: str, db: Session = Depends(get_db)):
    principals = read.get_title_principals(db, media_id)
    names = read.get_name_basic(db, list({p.nconst for p in principals}))
    for p in principals:
        p.name = next(n for n in names if n.nconst == p.nconst)
    return principals


@mediaRouter.get("/media/{media_id}/ratings", tags=["media"])
async def get_media_ratings(media_id: str, db: Session = Depends(get_db)):
    return read.get_title_ratings(db, media_id)


@mediaRouter.get("/media/{id}/episodes", tags=["media"])
async def get_media_episodes(id: str, db: Session = Depends(get_db)):
    return read.get_title_episodes(db, id)
