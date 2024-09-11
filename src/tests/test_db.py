from sqlalchemy import select

from src.domain.models.goal_model import CompleteGoal, Goal


def test_create_goal(session):
    new_goal = Goal(title='Estudar', desired_weekly_frequency='4')
    session.add(new_goal)
    session.commit()

    goal = session.scalar(select(Goal).where(Goal.title == 'Estudar'))

    assert goal.title == 'Estudar'


def test_complete_goal(session, goal: Goal):
    new_complete_goal = CompleteGoal(goal_id=goal.id)
    session.add(new_complete_goal)
    session.commit()
    session.refresh(new_complete_goal)

    goal = session.scalar(select(Goal).where(Goal.id == goal.id))

    assert new_complete_goal in goal.complete_goals
