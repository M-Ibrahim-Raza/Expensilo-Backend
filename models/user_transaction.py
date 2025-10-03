from typing import Optional
from datetime import datetime
from sqlalchemy import BigInteger, ForeignKey, func, Numeric, String, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UserTransaction(Base):
    __tablename__ = "user_transaction"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        comment="Reference to user",
    )

    transaction_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("transaction.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        comment="Reference to transaction",
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
        comment="Transaction amount",
    )

    details: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, comment="Additional transaction details"
    )

    attachments: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String), nullable=True, comment="File attachments stored as array"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp(),
        comment="Transaction timestamp)",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        comment="Update timestamp",
    )

    # =====================| TO BE REVIEWED | =====================

    user = relationship("User", back_populates="transactions", lazy="joined")

    transaction = relationship("Transaction", back_populates="users", lazy="joined")

    def __repr__(self) -> str:
        return (
            f"<UserTransaction(user_id={self.user_id}, "
            f"transaction_id={self.transaction_id}, "
            f"amount={self.amount})>"
        )
