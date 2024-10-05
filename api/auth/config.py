"""
Config for auth service
"""
from pydantic import BaseModel


class AuthSettings(BaseModel):
    jwt_algorithm: str
    jwt_access_token_lifetime: int
    jwt_refresh_token_lifetime: int

