from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UserCategory(Base):
    __tablename__ = "user_category"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        comment="Reference to user",
    )

    category_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("category.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        comment="Reference to category",
    )

    # =====================| TO BE REVIEWED | =====================

    user = relationship("User", back_populates="categories", lazy="joined")

    category = relationship("Category", back_populates="users", lazy="joined")

    def __repr__(self) -> str:
        return f"<UserCategory(user_id={self.user_id}, category_id={self.category_id})>"
