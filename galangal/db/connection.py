import settings
import sqlalchemy
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine(settings.DATABASE_URL)
Session = sessionmaker(engine)
