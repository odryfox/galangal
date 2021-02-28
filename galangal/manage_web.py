from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from infrastructure.web import create_app
from infrastructure.web.config import EnvironmentConfig


def migrate_db(database_url: str):
    alembic_config = AlembicConfig('alembic.ini')
    alembic_config.set_main_option('sqlalchemy.url', database_url)
    alembic_upgrade(alembic_config, 'head')


config = EnvironmentConfig()

migrate_db(database_url=config.DATABASE_URL)
app = create_app(config=config)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=config.DEBUG)
