from application import db
from application.models import Goal


def get_goals():
    goals = dict()
    for goal in db.session.query(Goal).all():
        if len(goals) <= 4:  # 4 may be variable for main page's limit of goals
            goals[goal.goal_url] = goal.goal_name
        else:
            break
    return goals
