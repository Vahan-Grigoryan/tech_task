"""
DB connection and Base abstract model for all other models
"""
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declared_attr, sessionmaker, DeclarativeBase
from .config import Settings
from .utils import from_camel_to_snake_case


db_settings = Settings().db
connection_url = URL.create(**db_settings.model_dump())
engine = create_engine(connection_url)
main_session = sessionmaker(engine)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return from_camel_to_snake_case(cls.__name__) + 's'

    id = Column(Integer, primary_key=True)
