from abc import ABC

from dotenv import load_dotenv

load_dotenv()


class Config(ABC):
    pass


class EnvironmentConfig(Config):
    pass
