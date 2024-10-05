from fastapi import HTTPException
from sqlalchemy import and_, delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload
from . import models


def list_all_categories(db_session: Session):
    """Get all categories from db"""
    return db_session.execute(
        select(models.Category)
    ).scalars().all()


def get_cats(
    db_session: Session,
    category_name: str | None = None
):
    """
    Get categories from db with or without category_name filter
    """
    statement = select(models.Cat)
    if category_name:
        statement = statement.join(
            models.Category,
            and_(
                models.Category.id == models.Cat.category_id,
                models.Category.name.contains(category_name),
            )
        )

    return db_session.execute(
        statement
    ).scalars().all()


def get_cat(
    db_session: Session,
    cat_id: int
):
    return db_session.get(models.Cat, cat_id)


def create_cat(
    db_session: Session,
    user_id: int,
    cat_input_data: dict
):
    """Create and return new cat in db"""
    cat = models.Cat(
        user_id=user_id,
        **cat_input_data
    )
    db_session.add(cat)
    db_session.flush()
    db_session.refresh(cat)

    return cat


def alter_cat(
    db_session: Session,
    cat_id: int,
    user_id: int,
    cat_alter_filled_data: dict
):
    """
    Alter cat by cat_id(and by implicitly received user_id from authed user).
    Return altered cat or None if cat from user not found
    """
    return db_session.execute(
        update(models.Cat).
        where(models.Cat.id == cat_id, models.Cat.user_id == user_id).
        values(**cat_alter_filled_data).
        returning(models.Cat).
        options(
            selectinload(models.Cat.user),
            selectinload(models.Cat.category)
        )
    ).scalar_one_or_none()


def delete_cat(
    db_session: Session,
    cat_id: int,
    user_id: int,
):
    """
    Delete cat by cat_id(and by implicitly received user_id from authed user).
    Return deleted cat or None if cat from user not found
    """
    return db_session.execute(
        delete(models.Cat).
        where(models.Cat.id == cat_id, models.Cat.user_id == user_id).
        returning(models.Cat)
    ).scalar_one_or_none()


def rate_cat(
    db_session: Session,
    user_id: int,
    cat_id: int,
    stars: int
):
    """
    Update(if exists) or create(if not exist) user rating
    related with cat with cat_id, set appropriate stars.
    If cat(for to rate) not found, raise exception.
    """
    old_rating = db_session.execute(
        select(models.Rating).
        filter_by(user_id=user_id, cat_id=cat_id)
    ).scalar_one_or_none()
    if old_rating:
        old_rating.stars = stars
        return

    try:
        new_rating = models.Rating(
            user_id=user_id,
            cat_id=cat_id,
            stars=stars
        )
        db_session.add(new_rating)
        db_session.flush()
    except IntegrityError:
        raise HTTPException(400, "Cat not found")
