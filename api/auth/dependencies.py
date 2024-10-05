"""
Dependencies for path operations.
Dependencies starting with the underscore are intended for a valid alias of type.
"""
import re
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import exc
from typing_extensions import Annotated
from . import models, db_manipulations, utils, schemas
from core import dependencies as global_deps


async def _create_user(
    db_session: global_deps.db_session,
    user_data: schemas.UserInputData = Depends()
) -> models.User:
    """Create and return user to path operation"""
    try:
        user = await db_manipulations.create_user(
            db_session,
            {
                "email": user_data.email,
                "password": user_data.password,
            }
        )
    except exc.IntegrityError as e:
        # if any error will occur
        # while creating user in db(email uniqueness violation for example),
        # it will be shown to user
        error_string = re.sub(
            r"\(|\)|DETAIL:  |Key ",
            '',
            str(e.orig).split('\n')[-2]
        )
        raise HTTPException(
            status_code=400,
            detail={
                "message": error_string
            }
        )

    return user


def _get_current_user(
    db_session: global_deps.db_session,
    settings: global_deps.settings,
    access_token: Annotated[str,
        Depends(OAuth2PasswordBearer(tokenUrl="tokens"))
    ]
) -> models.User | None:
    """
    Find and return user by provided access_token in header.
    If access_token not present or expired, raises error
    """
    payload = utils.decode_token(settings, access_token, "Access token expired")
    return db_manipulations.get_user(db_session, {"id": payload["user_id"]})


def _authenticate_user(
    db_session: global_deps.db_session,
    user_credetnials: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> models.User:
    """
    Find user by email(username in OAuth2PasswordRequestForm)
    and check password, if it invalid, raise error,
    else return found user
    """
    user = db_manipulations.get_user(
        db_session,
	    {"email": user_credetnials.username}
    )
    if not user or not user.check_password(user_credetnials.password):
        raise HTTPException(
            status_code=401,
            detail={
                "message": "Invalid email or password"
            }
        )

    return user


authenticate_user = Annotated[models.User, Depends(_authenticate_user)]
create_user = Annotated[models.User, Depends(_create_user)]
current_user = Annotated[models.User, Depends(_get_current_user)]
