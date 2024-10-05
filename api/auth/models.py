"""
Models(db tables)
"""
import hashlib
from sqlalchemy import Column,  String
from sqlalchemy.orm import relationship
from core.db import Base


class User(Base):
    """User model"""

    email = Column(String(500), unique=True, nullable=False)
    password = Column(String(200), nullable=False)

    cats = relationship(
        "Cat",
        back_populates="user"
    )
    ratings = relationship(
        "Rating",
        back_populates="user"
    )

    def set_password(self, new_password):
        h = hashlib.sha512(bytes(new_password, encoding="utf-8"))
        self.password = h.hexdigest()

    def check_password(self, password):
        h = hashlib.sha512(bytes(password, encoding="utf-8"))
        return self.password == h.hexdigest()
