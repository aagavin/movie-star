import httpx
from httpx import Response
from html.parser import HTMLParser
from typing import Union
from lxml import html
from sqlalchemy.orm import Session

from . import models

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0'}


class ImdbMediaParser(HTMLParser):

    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.posterUrl = ''
        self.isDescription = False
        self.description = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'img' and self.posterUrl == '':
            for attr in attrs:
                if attr[0] == 'src' and attr[1].startswith('https://m.media-amazon.com/images'):
                    self.posterUrl = attr[1]
        if tag == 'span' and self.description == '':
            for attr in attrs:
                if attr[0] == 'data-testid' and attr[1].startswith('plot-xl'):
                    self.isDescription = True

    def handle_data(self, text: str) -> None:
        if self.isDescription:
            self.description = text
            self.isDescription = False


async def get_popular_media(url):
    pop_media = []
    async with httpx.AsyncClient() as client:
        response: Response = await client.get(url, headers=headers, follow_redirects=True)
        doc = html.fromstring(response.text)
        pop_list = doc.find_class('ipc-metadata-list-summary-item')
        if not pop_list:
            return {}

        for row in pop_list:
            pop_media.append({
                "id": row.find_class('ipc-title-link-wrapper').pop().attrib.get('href').split('/')[2],
                "poster": row.find('.//img').attrib.get('src'),
                "title": row.find_class('ipc-title__text').pop().text_content(),
                "rating": row.find_class('ipc-rating-star--base')[0].attrib.get('aria-label')
            })
    return pop_media


def get_title_basic(db: Session, full: bool, tconst: str):
    if full:
        return db.query(models.TitleAkas).filter(models.TitleAkas.titleId == tconst).order_by(
            models.TitleAkas.ordering.asc()).all()
    return db.query(models.TitleBasic).filter(models.TitleBasic.tconst == tconst).first()


def get_title_crew(db: Session, tconst: str):
    return db.query(models.TitleCrew).filter(models.TitleCrew.tconst == tconst).first()


def get_title_principals(db: Session, tconst: str):
    return db.query(models.TitlePrincipals).filter(models.TitlePrincipals.tconst == tconst).all()


def get_title_ratings(db: Session, tconst: str):
    return db.query(models.TitleRatings).filter(models.TitleRatings.tconst == tconst).first()


def get_title_episodes(db: Session, tconst: str):
    return db.query(models.TitleEpisode).filter(models.TitleEpisode.parentTconst == tconst).order_by(
        models.TitleEpisode.seasonNumber).all()


def get_name_basic(db: Session, nconst: Union[list, str]):
    if isinstance(nconst, list):
        return db.query(models.NameBasics).filter(models.NameBasics.nconst.in_(nconst)).all()
    return db.query(models.NameBasics).filter(models.NameBasics.nconst == nconst).first()
