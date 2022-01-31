import csv
import gzip
import sys
from pathlib import Path
import httpx
import shutil
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


dirname = base_path = Path(__file__).parent

shutil.copyfile(dirname / '../database/models.py', dirname / 'models.py')

from models import Base, TitleBasic, TitleAkas, TitleCrew, TitlePrincipals, TitleRatings, TitleEpisode, NameBasics

session = httpx.Client()

engine = create_engine("sqlite:///./src/data.sqlite", echo=True, future=True)
connection = engine.connect()


Base.metadata.create_all(engine)


datasets = [
    # {
    #     "url": "https://datasets.imdbws.com/title.basics.tsv.gz",
    #     "class": TitleBasic
    # },
    # {
    #     "url": "https://datasets.imdbws.com/title.akas.tsv.gz",
    #     "class": TitleAkas
    # },
    {
        "url": "https://datasets.imdbws.com/title.crew.tsv.gz",
        "class": TitleCrew
    }
    # {
    #     "url": "https://datasets.imdbws.com/title.episode.tsv.gz",
    #     "class": TitleEpisode
    # },
    # {
    #     "url": "https://datasets.imdbws.com/name.basics.tsv.gz",
    #     "class": NameBasics
    # },
    # {
    #     "url": "https://datasets.imdbws.com/title.ratings.tsv.gz",
    #     "class": TitleRatings
    # }
    # {
    #     "url": "https://datasets.imdbws.com/title.principals.tsv.gz",
    #     "class": TitlePrincipals
    # }
]

Session = sessionmaker(engine)
s: Session = Session()

for dataset in datasets:
    filename = dataset['url'].split('/')[3]
    # dataSetResp = session.get(dataset['url'], follow_redirects=True)
    # with open(filename, 'wb') as f:
    #     f.write(dataSetResp.content)
    with gzip.open(filename, 'rt') as f:
        tsvFile = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        try:
            while True:
                insert_list = []
                done = False
                for _ in range(25000):
                    item = next(tsvFile, None)
                    if item is None:
                        done = True
                        break
                    insert_list.append(item)
                if done:
                    break
                insertRes = s.bulk_insert_mappings(dataset['class'], insert_list)
                commitRes = s.commit()
        except Exception as e:
            print(e)


print('====> closeing session')
s.close()
print('====> done session')

print('====> closeing connection')
connection.close()
print('====> done connection')

exit()