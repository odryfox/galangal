from typing import Any

from sqlalchemy.ext.declarative import declarative_base

Base: Any = declarative_base()

from account.models import *
from vocabulary_trainer.models import *
