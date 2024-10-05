from dataclasses import asdict
from typing import Annotated
from fastapi import Depends, HTTPException
from core.dependencies import db_session
from api.auth.dependencies import current_user
from . import db_manipulations, models, schemas


def _get_cats(
    db_session: db_session,
    category_name: str | None = "mixed"
):
    return db_manipulations.get_cats(
        db_session,
    	category_name
    )


def _create_cat(
    db_session: db_session,
    user: current_user,
    cat_input_data: schemas.CatInputData = Depends()
):
    return db_manipulations.create_cat(
        db_session,
        user.id,
        asdict(cat_input_data)
    )


def _alter_cat(
    db_session: db_session,
    user: current_user,
    cat_id: int,
    cat_alter_data: schemas.CatAlterData = Depends()
):
    """Alter and return cat, if cat not found, raise exception"""
    cat = db_manipulations.alter_cat(
        db_session,
        cat_id,
        user.id,
        cat_alter_data.get_filled_fields()
    )
    if not cat:
        raise HTTPException(400, f"Updatable cat with id {cat_id} and created by you, not found")
    
    return cat


def _delete_cat(
    db_session: db_session,
    user: current_user,
    cat_id: int,
):
    """Delete cat, if cat not found, raise exception"""
    cat = db_manipulations.delete_cat(
        db_session,
        cat_id,
        user.id,
    )
    if not cat:
        raise HTTPException(400, f"Deletable cat with id {cat_id} and created by you, not found")
    

def _rate_cat(
    db_session: db_session,
    user: current_user,
    cat_id: int,
    stars: int = 5
):
    db_manipulations.rate_cat(db_session, user.id, cat_id, stars)


get_cats = Annotated[list[models.Cat], Depends(_get_cats)]
create_cat = Annotated[models.Cat, Depends(_create_cat)]
alter_cat = Annotated[list[models.Cat], Depends(_alter_cat)]
delete_cat = Depends(_delete_cat)
rate_cat = Depends(_rate_cat)
