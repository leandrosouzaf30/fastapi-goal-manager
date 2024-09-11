from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.config.database import get_session
from src.domain.models.goal_model import CompleteGoal, Goal
from src.schemas.v1.goal_schemas import (
    GetGoalresponse,
    GoalComplete,
    GoalSchema,
    Message,
)

router = APIRouter()


@router.post(
    '/create_goal',
    status_code=HTTPStatus.CREATED,
    response_model=GetGoalresponse,
)
async def createGoal(
    goal: GoalSchema, session: Session = Depends(get_session)
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


@router.get(
    '/week_pending_goals/',
    status_code=HTTPStatus.OK,
    response_model=List[dict],
)
async def getGoals(
    session: Session = Depends(get_session), skip: int = 0, limit: int = 100
):
    goals = session.query(Goal).all()
    result = []
    for goal in goals:
        completed_count = len(goal.complete_goals)
        remaining_frequency = goal.desired_weekly_frequency - completed_count
        result.append({
            'id': goal.id,
            'title': goal.title,
            'desired_weekly_frequency': remaining_frequency,
            'created_at': goal.created_at,
        })
    return result


@router.put('/update_goal/{goal_id}', response_model=GetGoalresponse)
async def update_goal(
    goal_id: int,
    goal: GoalSchema,
    session: Session = Depends(get_session),
):
    db_goal = session.scalar(select(Goal).where((Goal.id == goal_id)))

    if not db_goal:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Goal not found',
        )

    db_goal.title = goal.title
    db_goal.desired_weekly_frequency = goal.desired_weekly_frequency
    session.commit()
    session.refresh(db_goal)

    return db_goal


@router.delete('/delete_goal/{goal_id}', response_model=Message)
async def delete_goal(goal_id: int, session: Session = Depends(get_session)):
    db_goal = session.scalar(select(Goal).where((Goal.id == goal_id)))

    if not db_goal:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Goal not found',
        )
    session.delete(db_goal)
    session.commit()

    return {'message': 'Goal deleted'}


@router.post(
    '/complete_goal', status_code=HTTPStatus.CREATED, response_model=Message
)
async def completeGoal(
    goal_complete: GoalComplete, session: Session = Depends(get_session)
):
    new_complete_goal = CompleteGoal(goal_id=goal_complete.goal_id)
    session.add(new_complete_goal)
    session.commit()
    session.refresh(new_complete_goal)

    return {'message': 'Completed'}
