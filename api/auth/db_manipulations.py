from sqlalchemy import select
from . import models


async def create_user(db_session, user_credentials: dict) -> models.User:
    """Create user with given credentials"""
    password = user_credentials.pop("password")
    user = models.User(**user_credentials)
    user.set_password(password)
    db_session.add(user)
    return user


def get_user(db_session, search_fields: dict) -> models.User | None:
    """Find user by search_fields and return it or None"""
    return db_session.execute(
        select(models.User)
        .filter_by(**search_fields)
    ).scalar_one_or_none()
