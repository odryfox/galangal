import sqlalchemy
from sqlalchemy import orm


class DB:
    def __init__(self, url: str):
        self.engine = sqlalchemy.create_engine(url)

    def create_session(self):
        return orm.scoped_session(orm.sessionmaker(bind=self.engine))
