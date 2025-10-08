from typing import Optional

from sqlalchemy import String, BigInteger, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enums import TransactionType
from .base import Base


class Transaction(Base):
    __tablename__ = "transaction"

    __table_args__ = (
        UniqueConstraint("type", "title", "category_id", name="uq_type_title_category"),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="Unique identifier for transaction",
    )

    category_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        ForeignKey("category.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
        comment="Reference to category (NULL Allowed)",
    )

    type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, name="transaction_type_enum"),
        nullable=False,
        comment="Transaction type: EXPENSE or INCOME",
    )

    title: Mapped[str] = mapped_column(
        String, nullable=False, comment="Transaction title"
    )

    category = relationship("Category", back_populates="transactions", lazy="joined")

    users = relationship(
        "UserTransaction",
        back_populates="transaction",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Transaction(id={self.id}, title='{self.title}', category_id={self.category_id})>"
