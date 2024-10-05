from dataclasses import asdict, dataclass
from typing import Annotated
from fastapi import Form
from pydantic import BaseModel, ConfigDict
from api.auth.schemas import UserDataResponse


class ORMMixin(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Category(ORMMixin):
    id: int
    name: str


class Cat(ORMMixin):
    id: int
    color: str
    age: int
    desc: str | None = None


class CatExtended(Cat):
    user: UserDataResponse
    category: Category


@dataclass(slots=True)
class CatInputData:
    category_id: Annotated[int, Form()]
    color: Annotated[str, Form(examples=["whitegray"])]
    age: Annotated[int, Form(examples=[3])]
    desc: Annotated[str | None, Form(examples=["Some desc..."])] = None


@dataclass(slots=True)
class CatAlterData:
    category_id: Annotated[int | None, Form()] = None
    color: Annotated[str | None, Form()] = None
    age: Annotated[int | None, Form()] = None
    desc: Annotated[str | None, Form()] = None

    def get_filled_fields(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
