from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from core.db import Base


class Category(Base):
    name = Column(String(200), unique=True, nullable=False)

    cats = relationship(
        "Cat",
        back_populates="category"
    )


class Cat(Base):
    user_id = Column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    category_id = Column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
    )
    color = Column(String(200), nullable=False)
    age = Column(Integer, nullable=False)
    desc = Column(Text)

    user = relationship(
        "User",
        back_populates="cats"
    )
    category = relationship(
        "Category",
        back_populates="cats"
    )
    ratings = relationship(
        "Rating",
        back_populates="cat"
    )


class Rating(Base):
    user_id = Column(ForeignKey("users.id"))
    cat_id = Column(ForeignKey("cats.id"))
    stars = Column(Integer)

    user = relationship(
        "User",
        back_populates="ratings"
    )
    cat = relationship(
        "Cat",
        back_populates="ratings"
    )
