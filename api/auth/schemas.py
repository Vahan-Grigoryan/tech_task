"""
Request bodies for path operations
"""
from dataclasses import dataclass
import re
from typing import Annotated
from email_validator import EmailNotValidError, validate_email
from fastapi import Form, HTTPException
from pydantic import BaseModel, ConfigDict


class UserDataResponse(BaseModel):
    """
    Model used for returning full user data
    (can be used after creating/finding/updating user)
    """
    model_config = ConfigDict(from_attributes=True)

    email: str


class AccessToken(BaseModel):
    access_token: str
    token_type: str


@dataclass(slots=True)
class UserInputData():
    email: Annotated[str, Form(examples=["ex@mail.ru"])]
    password: Annotated[str, Form(
        min_length=8,
        max_length=200,
        examples=["exPASS1010"]
    )]
    
    def check_email(self):
        """
        Validate email.
        Return it if valid, else raise error
        """
        try:
            emailinfo = validate_email(self.email, check_deliverability=True)
            return emailinfo.normalized
     
        except EmailNotValidError as e:
            return {
                "field": "email",
                "message": str(e)
            }
    
    def check_password(self):
        """
        Ensures that password contain 
        minimal required valid characters.
        Return it if valid, else raise error
        """
        match = re.search(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).+$", self.password)
    
        if match: return self.password
    
        return {
            "field": "password",
            "message":  "Password should have at least 1 number, lowercase and uppercase letter"
        }

    def __post_init__(self):
        errors = []
        email = self.check_email()
        password = self.check_password()

        if type(email) == dict:
            errors.append(email)
        if type(password) == dict:
            errors.append(password)
        
        if not errors:
            return
        
        raise HTTPException(status_code=400, detail=errors)

