from sqlalchemy import (Column, Integer, Float, String, create_engine, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TitleBasic(Base):
    __tablename__ = 'titleBasic'
    tconst = Column(String, primary_key=True, index=True)
    titleType = Column(String)
    primaryTitle = Column(String)
    originalTitle = Column(String)
    isAdult = Column(String(length=1))
    startYear = Column(String(length=4))
    endYear = Column(String(length=4))
    runtimeMinutes = Column(Integer)
    genres = Column(String)


    def __init__(self, tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres) -> None:
        self.tconst = tconst
        self.titleType = titleType
        self.primaryTitle = primaryTitle
        self.originalTitle = originalTitle
        self.isAdult = isAdult = True if isAdult == 1 else False
        self.startYear = None if startYear == '\\N' else startYear
        self.endYear = None if endYear == '\\N' else endYear
        self.runtimeMinutes = runtimeMinutes
        self.genres = genres


class TitleAkas(Base):
    __tablename__ = 'titleAkas'
    id = Column(Integer, primary_key=True)
    titleId = Column(String, ForeignKey('titleBasic.tconst'))
    ordering = Column(Integer)
    title = Column(String)
    region = Column(String)
    language = Column(String)
    types = Column(String)
    attributes = Column(String)
    isOriginalTitle = Column(String(length=2))

    def __init__(self, titleId, ordering, title, region, language, types, attributes, isOriginalTitle) -> None:
        self.titleId = titleId
        self.ordering = ordering
        self.title = title
        self.region = region
        self.language = None if language == '\\N' else language
        self.types = types
        self.attributes = attributes
        self.isOriginalTitle = True if isOriginalTitle == 1 else False

class TitleCrew(Base):
    """
    Contains the director and writer information for all the titles in IMDb
    """
    __tablename__ = 'titleCrew'
    id = Column(Integer, primary_key=True)
    tconst = Column(String, ForeignKey('titleBasic.tconst'))
    directors = Column(String)
    writers = Column(String)

class TitlePrincipals(Base):
    """
    Contains the principal cast/crew for titles
    """
    __tablename__ = 'titlePrincipals'
    id = Column(Integer, primary_key=True)
    tconst = Column(String, ForeignKey('titleBasic.tconst'))
    nconst = Column(String, ForeignKey('nameBasics.nconst'))
    ordering = Column(Integer)
    category = Column(String)
    job = Column(String)
    characters = Column(String)

class TitleRatings(Base):
    """
    Contains the IMDb rating and votes information for titles
    """
    __tablename__ = 'titleRatings'
    id = Column(Integer, primary_key=True)
    tconst = Column(String, ForeignKey('titleBasic.tconst'))
    averageRating = Column(Float(precision=2))
    numVotes = Column(Integer)


class TitleEpisode(Base):
    """
    Contains the tv episode information. Fields include
    """
    __tablename__ = 'titleEpisode'
    tconst = Column(String, primary_key=True, index=True)
    parentTconst = Column(String, ForeignKey('titleBasic.tconst'))
    seasonNumber = Column(Integer)
    episodeNumber = Column(Integer)

    def __init__(self, tconst, parentTconst, seasonNumber, episodeNumber) -> None:
        self.tconst = tconst
        self.parentTconst = parentTconst
        self.seasonNumber = seasonNumber
        self.episodeNumber = episodeNumber

        
class NameBasics(Base):
    """
    Contains the following information for names
    """
    __tablename__ = 'nameBasics'
    nconst = Column(String, primary_key=True, index=True)
    primaryName = Column(String)
    birthYear = Column(String(length=4))
    deathYear = Column(String(length=4))
    primaryProfession = Column(String)
    knownForTitles = Column(String)
