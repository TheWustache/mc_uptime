from app.db import get_dbc
import datetime

def optimal_slot(app_id):
    db, c = get_dbc()
    # get all slots associated with app
    c.execute('''SELECT slot.day, slot.start_time, availible.user
        FROM availible
        JOIN slot ON slot.availible_id = availible.id
        JOIN app ON app.id = availible.app_id
        WHERE app.id = ?''',
              (app_id,))
    slots = c.fetchall()
    # split by user
    user_slots = {}
    for s in slots:
        if s['user'] not in user_slots:
            user_slots[s['user']] = []
        user_slots[s['user']].append({'day':s['day'], 'start_time':s['start_time']})

    # get slot length
    c.execute('''SELECT slot_length
        FROM app
        WHERE id = ?''',
              (app_id,))
    slot_length = c.fetchone()['slot_length']

    # determine best slot
    # brute force. definitely crap.
    optimal = {'day':'Mo', 'slot':0, 'overlap':0}
    for day in ('Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'):
        day_optimal = {'day':day, 'slot':0, 'overlap':0}
        for i in range(48 - slot_length):
            overlap = 0
            for key in user_slots:
                user_optimal = {'day':day, 'slot':i, 'overlap':0}
                for s in user_slots[key]:
                    if s['day'] == day:
                        slot_diff = abs(s['start_time'] - i)
                        local_overlap = slot_length - slot_diff
                        if slot_diff < slot_length and local_overlap > user_optimal['overlap']:
                            user_optimal['overlap'] = local_overlap
                overlap += user_optimal['overlap']
            if overlap > day_optimal['overlap']:
                day_optimal['slot'] = i
                day_optimal['overlap'] = overlap
        if day_optimal['overlap'] > optimal['overlap']:
            optimal = day_optimal
    return optimal

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
