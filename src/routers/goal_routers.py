from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.config.database import get_session
from src.domain.models.goal_model import Goal
from src.schemas.v1.goal_schemas import CreateGoalSchema, GetGoalresponse

router = APIRouter()


@router.post(
    '/goal', status_code=HTTPStatus.CREATED, response_model=GetGoalresponse
)
async def createGoal(
    goal: CreateGoalSchema, session: Session = Depends(get_session)
):
    db_goal = session.scalar(select(Goal).where((Goal.title == goal.title)))

    if db_goal:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Goal already exists',
        )

    db_goal = Goal(
        title=goal.title,
        desired_weekly_frequency=goal.desired_weekly_frequency,
    )

    session.add(db_goal)
    session.commit()
    session.refresh(db_goal)

    return db_goal
