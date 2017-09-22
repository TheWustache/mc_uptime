from app.db import get_dbc
from app.user import get_availible_id

#TODO: get_app_info(app_id)

def app_exists(app_id):
    db, c = get_dbc()
    c.execute('''SELECT COUNT(*)
        FROM app
        WHERE id = ?
        GROUP BY id''',
        (app_id,))
    result = c.fetchone()

    return result is not None

# TODO: make slot number adjustable
def app_add_user(app_id, user):
    # add user to app
    db, c = get_dbc()
    c.execute('''INSERT INTO availible (user, app_id)
        VALUES (?, ?)''',
              (user, app_id))
    # give users slots
    # TODO: make slot amount adjustable
    availible_id = get_availible_id(
        user, app_id)
    c.execute('''INSERT INTO slot (day, start_time, availible_id)
        VALUES ('Mo', 0, ?), ('Mo', 0, ?), ('Mo', 0, ?)''',
              (availible_id, availible_id, availible_id))
    db.commit()
