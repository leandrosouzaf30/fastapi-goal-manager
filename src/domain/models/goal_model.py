from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

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
