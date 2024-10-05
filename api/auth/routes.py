from typing import Annotated
from fastapi import APIRouter, Cookie
from fastapi.responses import JSONResponse
from api.auth import utils
from core import dependencies as global_deps
from . import dependencies, schemas


router = APIRouter()


@router.post(
    "/registration",
    response_model=schemas.UserDataResponse
)
async def register_user(
    created_user: dependencies.create_user,
):
    """User registration endpoint"""

    return created_user


@router.post("/tokens")
def tokens(
    user: dependencies.authenticate_user,
    settings: global_deps.settings
):
    """
	Create pair tokens, 
    return access_token and it's type in response body,
    return refresh_token as httponly cookie
	"""
    access_token = utils.create_token(
        settings,
        "access_token",
        {"user_id": user.id},
    )
    refresh_token = utils.create_token(
        settings,
        "refresh_token",
        {"user_id": user.id},
    )
    response = JSONResponse(
        {"access_token": access_token, "token_type": "Bearer"}
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        settings.auth.jwt_refresh_token_lifetime,
        httponly=True
    )
    return response


@router.get("/refresh", response_model=schemas.AccessToken)
def refresh_access_token(
    refresh_token: Annotated[str, Cookie()],
    settings: global_deps.settings
):
    """Refresh access token by received refresh token in cookies"""
    payload = utils.decode_token(settings, refresh_token, "Refresh token expired")
    access_token = utils.create_token(
        settings,
        "access_token",
        {"user_id": payload["user_id"]},
    )
    return {"access_token": access_token, "token_type": "Bearer"}


