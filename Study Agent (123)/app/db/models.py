from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """SQLAlchemy 基类。"""


class UserProfileModel(Base):
    """用户画像表。"""

    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    summary: Mapped[str] = mapped_column(Text)
    strengths: Mapped[dict] = mapped_column(JSON, default=list)
    weaknesses: Mapped[dict] = mapped_column(JSON, default=list)
    preferences: Mapped[dict] = mapped_column(JSON, default=list)
    risk_points: Mapped[dict] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class LearningPlanModel(Base):
    """学习计划与学习轨迹。"""

    __tablename__ = "learning_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    profile_id: Mapped[int | None] = mapped_column(Integer, index=True)
    topic: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(Text)
    units_json: Mapped[dict] = mapped_column(JSON)  # 存整个 LessonUnit 列表
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

