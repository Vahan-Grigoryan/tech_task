"""
This file contains functions that may will be used in many places in this service.
DRY pattern.
"""
from datetime import datetime, timedelta, timezone
from typing import Literal
import jwt
from fastapi import HTTPException
from core.config import Settings


def create_token(
	settings: Settings,
    token_name: Literal["access_token", "refresh_token"],
	payload_part: dict,
):
    """
	Create token and return it
	"""
    if token_name == "access_token":
        token_lifetime = timedelta(minutes=settings.auth.jwt_access_token_lifetime)
    else:
        token_lifetime = timedelta(minutes=settings.auth.jwt_refresh_token_lifetime)

    token = jwt.encode(
        {
            "token_name": token_name, 
	        "exp": datetime.now(timezone.utc) + token_lifetime,
            **payload_part
        },
        settings.secret_key,
        settings.auth.jwt_algorithm,
        headers={"typ":"Bearer"}
    )

    return token

def decode_token(
	settings: Settings,
    token: str,
	token_expired_error_message: str,
):
    """
    Decode token and return payload.
    If token expired, raise appropriate error.
    If unexpected error occured, return it to client.
    """
    try:
        payload = jwt.decode(
            token,
	        settings.secret_key,
	        [settings.auth.jwt_algorithm]
        )
        return payload
        
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail={
                "message": token_expired_error_message
            }
        )

    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Something went wrong"
            }
        )
