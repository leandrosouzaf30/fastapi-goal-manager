from sqlalchemy import select

from src.domain.models.goal_model import Goal


def test_create_goal(session):
    new_goal = Goal(title='Estudar', desired_weekly_frequency='4')
    session.add(new_goal)
    session.commit()

    goal = session.scalar(select(Goal).where(Goal.title == 'Estudar'))

    assert goal.title == 'Estudar'
