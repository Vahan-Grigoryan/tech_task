from fastapi import APIRouter, HTTPException, Response
from . import db_manipulations, schemas, dependencies
from core.dependencies import db_session


router = APIRouter()


@router.get(
    "/categories",
    response_model=list[schemas.Category]
)
def list_categories(
    db_session: db_session
):
    """List all categories"""
    return db_manipulations.list_all_categories(
        db_session
    )


@router.get(
    "/cats",
    response_model=list[schemas.Cat]
)
def list_cats(
    cats: dependencies.get_cats
):
    """List cats with or without filtering by category"""
    return cats


@router.get(
    "/cats/{cat_id}",
    response_model=schemas.CatExtended
)
def get_cat(
    db_session: db_session,
    cat_id: int
):
    """Get detail info about cat by id"""
    cat = db_manipulations.get_cat(db_session, cat_id)
    if not cat:
        raise HTTPException(404, "Cat not found")
    return cat


@router.post(
    "/cats",
    response_model=schemas.CatExtended
)
def create_cat(created_cat: dependencies.create_cat):
    """Create new cat"""
    return created_cat


@router.patch(
    "/cats/{cat_id}",
    response_model=schemas.CatExtended
)
def alter_cat(alter_cat: dependencies.alter_cat):
    """Alter cat"""
    return alter_cat


@router.delete(
    "/cats/{cat_id}",
    dependencies=[dependencies.delete_cat]
)
def delete_cat():
    """Delete cat by id"""
    return Response(status_code=204)


@router.get(
    "/cats/{cat_id}/rate",
    dependencies=[dependencies.rate_cat]
)
def rate_cat():
    """"Rate cat by id"""
    return Response(status_code=204)
