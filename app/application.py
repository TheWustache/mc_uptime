from app.db import get_db

#TODO: get_app_info(app_id)

def app_exists(app_id):
    db = get_db()
    c = db.cursor()
    c.execute('''SELECT COUNT(*)
        FROM app
        WHERE id = ?
        GROUP BY id''',
        (app_id,))
    result = c.fetchone()

    return result is not None
