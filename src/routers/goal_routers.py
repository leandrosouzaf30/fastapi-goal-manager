from fastapi import APIRouter

from src.schemas.v1.goal_schemas import CreateGoalSchema, GetGoalresponse

router = APIRouter()


@router.post('/goal', response_model=GetGoalresponse)
async def createGoal(goal: CreateGoalSchema):
    pass
