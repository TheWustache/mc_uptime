from app.db import get_dbc
from datetime import datetime

settings_path = '/Users/leo/Projects/mc_uptime_server/app/settings.json'


def get_setting(setting):
    db, c = get_dbc()
    # fetch from db
    c.execute('''SELECT value, type
        FROM setting
        WHERE key = ?''',
              (setting,))
    result = c.fetchone()
    val = result['value']
    t = result['type']
    # convert type if necessary
    if t == 'int':
        val = int(val)
    elif t == 'bool':
        val = val == 'True'
    elif t == 'date':
        val = datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
    return val


def set_setting(setting, value):
    db, c = get_dbc()
    # get type
    t = 'string'
    if type(value) is int:
        t = 'int'
    elif type(value) is bool:
        t = 'bool'
    elif type(value) is datetime:
        t = 'date'
    # convert value to string
    value = str(value)
    # write to db
    c.execute('''UPDATE setting
        SET value = ?, type = ?
        WHERE key = ?''',
              (value, t, setting))
    db.commit()
