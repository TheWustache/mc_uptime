from app.db import get_dbc
import datetime

def optimal_slot():
    db, c = get_dbc()
    # get all slots associated with app
    c.execute('''SELECT slot.start_time, user_slot.user, user_slot.day
        FROM slot
        JOIN user_slot ON slot.id = user_slot.slot_id''')
    slots = c.fetchall()
    print(slots)

def weekday_abr_to_num(day):
    d = {'Mo':0, 'Tu':1, 'We':2, 'Th':3, 'Fr':4, 'Sa':5, 'Su':6}
    return d[day] # storm the beach

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def next_session(app_id):
    slot = optimal_slot(app_id)
    return (next_weekday(datetime.date.today(), weekday_abr_to_num(slot['day'])), slot['slot'])
