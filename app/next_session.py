from app.db import get_dbc
import datetime


def optimal_slot():
    db, c = get_dbc()
    # get all slots with the amount of user_slot references
    c.execute('''SELECT slot.start_time, user_slot.day, COUNT(*) AS votes
        FROM slot
        JOIN user_slot ON slot.id = user_slot.slot_id
        GROUP BY slot.id, user_slot.day''')
    slots = c.fetchall()
    # find slots with the most votes and, for slots with the same amount, fitting the secondary criteria best
    optimal = {'day': 4, 'start_time': 36, 'votes': 0}
    for s in slots:
        if s['votes'] > optimal['votes']:
            optimal = s
    return (optimal['day'], optimal['start_time'])


def next_week():
    """Returns beginning of next week (Mo, 0:00am)"""
    t = datetime.date.today()
    return datetime.datetime(year=t.year, month=t.month, day=t.day) + datetime.timedelta(days=7 - datetime.date.today().weekday()) + datetime.timedelta(seconds=1)


def next_session(withinWeek=False):
    next_day, next_start = optimal_slot()
    weeks = 0
    if withinWeek and datetime.date.today().weekday() >= next_day:
        weeks = -1
    return next_week() + datetime.timedelta(weeks=weeks, days=next_day, hours=next_start * 0.5)
