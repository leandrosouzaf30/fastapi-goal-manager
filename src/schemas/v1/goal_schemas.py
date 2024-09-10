from pydantic import BaseModel


class GetGoalresponse(BaseModel):
    id: int
    title: str
    desired_weekly_frequency: int


class CreateGoalSchema(BaseModel):
    title: str
    desired_weekly_frequency: int
