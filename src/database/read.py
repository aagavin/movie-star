from sqlalchemy.orm import Session
from typing import Union
from html.parser import HTMLParser

from . import models


class ImdbParser(HTMLParser):

    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.posterUrl = ''
        self.isDescription = False
        self.description = ''
        self.isNextEp = False
        self.nextEp = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'img' and self.posterUrl == '':
            for attr in attrs:
                if attr[0] == 'src' and attr[1].startswith('https://m.media-amazon.com/images'):
                    self.posterUrl = attr[1]
        if tag == 'span' and self.description == '':
            for attr in attrs:
                if attr[0] == 'data-testid' and attr[1].startswith('plot-xl'):
                    self.isDescription = True
        if tag == 'div' and self.nextEp == '':
            for attr in attrs:
                if attr[0] == 'class':
                    print(attr[1])
                    # self.isNextEp = True

    def handle_data(self, text: str) -> None:
        if self.isDescription:
            self.description = text
            self.isDescription = False
        if self.isNextEp:
            self.nextEp = text
            self.isNextEp = False


def get_title_basic(db: Session, full: bool, tconst: str):
    if full:
        return db.query(models.TitleAkas).filter(models.TitleAkas.titleId == tconst).order_by(models.TitleAkas.ordering.asc()).all()
    return db.query(models.TitleBasic).filter(models.TitleBasic.tconst == tconst).first()


def get_title_crew(db: Session, tconst: str):
    return db.query(models.TitleCrew).filter(models.TitleCrew.tconst == tconst).first()


def get_title_principals(db: Session, tconst: str):
    return db.query(models.TitlePrincipals).filter(models.TitlePrincipals.tconst == tconst).all()


def get_title_ratings(db: Session, tconst: str):
    return db.query(models.TitleRatings).filter(models.TitleRatings.tconst == tconst).first()


def get_title_episodes(db: Session, tconst: str):
    return db.query(models.TitleEpisode).filter(models.TitleEpisode.parentTconst == tconst).order_by(models.TitleEpisode.seasonNumber).all()


def get_name_basic(db: Session, nconst: Union[list, str]):
    if isinstance(nconst, list):
        return db.query(models.NameBasics).filter(models.NameBasics.nconst.in_(nconst)).all()
    return db.query(models.NameBasics).filter(models.NameBasics.nconst == nconst).first()
