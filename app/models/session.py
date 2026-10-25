from datetime import datetime
from sqlalchemy import (
    String, DateTime, ForeignKey, CheckConstraint, func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Ровно одно из двух заполнено — гарантирует CHECK ниже
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    organization_id: Mapped[int | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    # SHA-256 hex = ровно 64 символа
    refresh_token_hash: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, nullable=False
    )

    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "(user_id IS NOT NULL AND organization_id IS NULL) OR "
            "(user_id IS NULL AND organization_id IS NOT NULL)",
            name="ck_sessions_single_owner",
        ),
    )