from pydantic import BaseModel


class TitleBasicBase(BaseModel):
    tconst: str
    titleType: str
    primaryTitle: str
    originalTitle: str
    isAdult: str
    startYear: str
    endYear: str
    runtimeMinutes: int
    genres: str


class TitleBasicCreate(TitleBasicBase):
    pass


class TitleBasic(TitleBasicBase):
    tconst: str

    class Config:
        orm_mode = True


class TitleAkasBase(BaseModel):
    id: int
    titleId: str
    ordering: int
    title: str
    region: str
    language: str
    types: str
    attributes: str
    isOriginalTitle: str


class TitleAkas(TitleAkasBase):
    titleId: str

    class Config:
        orm_mode = True

