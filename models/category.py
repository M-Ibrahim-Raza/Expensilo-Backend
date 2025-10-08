from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="Unique identifier for category",
    )

    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        comment="Category name",
    )

    users = relationship(
        "UserCategory",
        back_populates="category",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    transactions = relationship(
        "Transaction", back_populates="category", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"
