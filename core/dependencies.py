"""
Global dependencies that can be used in any service 
"""
from functools import lru_cache
from fastapi import Depends
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from .config import Settings
from .db import main_session


@lru_cache
def get_settings():
    return Settings()

settings = Annotated[Settings, Depends(get_settings)]

def get_db_session():
    with main_session.begin() as session:
        yield session

db_session = Annotated[Session, Depends(get_db_session)]

