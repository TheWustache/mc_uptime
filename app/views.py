from flask import session, redirect, url_for, render_template, request
from app.user import login_user, logout_user
from app import app
from app.db import get_db


@app.route('/')
def index():
    if 'username' in session:
        return render_template('overview.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # check if user is already logged in
    if 'username' in session:
        return redirect(url_for('index'))

    # if form was submitted
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user(username, password):
            return redirect(url_for('index'))
        # TODO: Notify user that login was unsuccessful

    # if login page was requested
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# @app.route('/overview')
# def overview():
#     if 'username' in session:


@app.route('/updatetimes/<int:app_id>')
def udpateTimes(app_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    # check if user has access to app
    username = session['username']
    db = get_db()
    c = db.cursor()
    c.execute('''SELECT COUNT(*)
        FROM user
        JOIN availible ON user.username = availible.user
        JOIN app ON app.id = availible.app_id
        WHERE user = ?
        AND app.id = ?
        GROUP BY app.id''',
        (username, app_id))
    hasApp = c.fetchone()
    if hasApp is None:
        return "'%s' does not have app '%i'" % (username, app_id)
    else:
        # get name of app
        c.execute('''SELECT name
            FROM app
            WHERE id = ?''',
            (app_id,))
        app_name = c.fetchone()['name']

        # get slot length
        c.execute('''SELECT slot_length
            FROM availible
            WHERE user = ?
            AND app_id = ?''',
            (username, app_id))
        slot_length = c.fetchone()['slot_length']

        # get slots
        c.execute('''SELECT day, start_time
            FROM slot
            JOIN availible ON slot.availible_id = availible.id
            WHERE availible.user = ?''',
            (username,))
        slots = c.fetchall()

        return render_template('updateTimes.html', username=username, app_name=app_name, slot_length=slot_length, slots=slots)
