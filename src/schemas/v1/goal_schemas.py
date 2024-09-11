from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    message: str


class GetGoalresponse(BaseModel):
    id: int
    title: str
    desired_weekly_frequency: int
    model_config = ConfigDict(from_attributes=True)


class GoalSchema(BaseModel):
    title: str
    desired_weekly_frequency: int


class GoalsList(BaseModel):
    goals: list[GetGoalresponse]


class GoalComplete(BaseModel):
    goal_id: int
