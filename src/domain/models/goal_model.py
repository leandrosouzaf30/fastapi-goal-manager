from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class Goal:
    __tablename__ = 'goals'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    desired_weekly_frequency: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    complete_goals: Mapped[list['CompleteGoal']] = relationship(
        init=False, back_populates='goal', cascade='all, delete-orphan'
    )


@table_registry.mapped_as_dataclass
class CompleteGoal:
    __tablename__ = 'complete_goals'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    goal_id: Mapped[int] = mapped_column(ForeignKey('goals.id'))

    goal: Mapped[Goal] = relationship(
        init=False, back_populates='complete_goals'
    )
