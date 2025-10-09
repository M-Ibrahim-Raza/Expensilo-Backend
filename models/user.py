from __future__ import annotations

from typing import Optional

from sqlalchemy import String, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="Unique identifier for user",
    )

    name: Mapped[str] = mapped_column(
        String, nullable=False, comment="User's full name"
    )

    email: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, comment="User's email address"
    )

    hashed_password: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, comment="hashed password for authentication"
    )

    google_auth: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, comment="Google OAuth authentication token"
    )

    preferences: Mapped[Optional[dict]] = mapped_column(
        JSONB, nullable=True, comment="User preferences stored as JSON"
    )

    categories = relationship(
        "UserCategory",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    transactions = relationship(
        "UserTransaction",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
