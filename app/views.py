from flask import session, redirect, url_for, render_template, request, abort, jsonify
from app.user import login_user, logout_user, loggedin, is_admin, user_exists, user_has_app, get_availible_id, create_user, user_get_user_slot_ids
from app import app
from app.db import get_dbc
from app.settings import get_setting, set_setting
from app.next_session import next_session

# TODO: split into multiple files


@app.route('/')
def index():
    # if 'username' in session:
    #     return render_template('index.html', username=session['username'])
    # return redirect(url_for('login'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # check if user is already logged in
    if loggedin():
        return redirect(url_for('overview'))

    # if form was submitted
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_user(username, password):
            return redirect(url_for('overview'))
        # TODO: Notify user that login was unsuccessful

    # if login page was requested
    return render_template('login.html.j2')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/overview')
def overview():
    if loggedin():
        username = session['username']
        return render_template('overview.html.j2', username=session['username'])
    else:
        return redirect(url_for('login'))


@app.route('/updatetimes/', methods=['GET', 'POST'])
def updateTimes():
    if not loggedin():
        return redirect(url_for('login'))

    username = session['username']
    db, c = get_dbc()
    # if form was submitted
    if request.method == 'POST':
        # delete all user_slot entries for user
        c.execute('''DELETE FROM user_slot
            WHERE user = ?''',
                  (username,))
        # get slots
        c.execute('''SELECT id
            FROM slot
            ORDER BY start_time ASC''')
        slots = list(s['id'] for s in c.fetchall())
        # for each slot and each weekday: add user_slot entry if checked
        new_entries = []
        for s in slots:
            for day in range(7):
                if request.form.get('slot:{}-day:{}'.format(s, day)) is not None:
                    new_entries.append((username, s, day))
        c.executemany('''INSERT INTO user_slot
            VALUES (null, ?, ?, ?)''',
                      new_entries)
        db.commit()
        return redirect(url_for('overview'))

    # if page was requested
    else:
        # get slots
        c.execute('''SELECT id, start_time
            FROM slot
            ORDER BY start_time ASC''')
        slots = c.fetchall()
        # get slot length
        slot_length = get_setting('slot_length')
        # get slots associated with user
        c.execute('''SELECT slot_id, day
            FROM user_slot
            WHERE user = ?''',
                  (username,))
        user_slots = c.fetchall()
        return render_template('updateTimes.html.j2', username=username, slots=slots, slot_length=slot_length, user_slots=user_slots)


@app.route('/admin')
def admin_panel():
    # user needs to be logged in
    if not loggedin():
        return redirect(url_for('login'))

    username = session['username']
    # forbidden if user does not have access (operator for app or admin)
    if not is_admin(username):
        abort(403)

    return render_template('admin_panel.html.j2', username=username)


@app.route('/admin/users')
def admin_users():
    # user needs to be logged in
    if not loggedin():
        return redirect(url_for('login'))

    username = session['username']
    # forbidden if user does not have access (operator for app or admin)
    if not is_admin(username):
        abort(403)

    # get all users
    db, c = get_dbc()
    c.execute('''SELECT username
        FROM user''')
    result_users = c.fetchall()
    users = list((u['username'] for u in result_users))

    return render_template('admin_users.html.j2', username=username, users=users)


@app.route('/admin/slots', methods=['GET', 'POST'])
def admin_slots():
    # user needs to be logged in
    if not loggedin():
        return redirect(url_for('login'))

    username = session['username']
    # forbidden if user does not have access (operator for app or admin)
    if not is_admin(username):
        abort(403)

    # get all slots
    db, c = get_dbc()
    c.execute('''SELECT start_time
        FROM slot''')
    result_slots = c.fetchall()
    slots = list((s['start_time'] for s in result_slots))

    # get slot length
    slot_length = get_setting('slot_length')

    return render_template('admin_slots.html.j2', username=username, slots=slots, slot_length=slot_length)


@app.route('/admin/new_user', methods=['GET', 'POST'])
def new_user():
    # TODO: encapsulate this shite
    # user needs to be logged in
    if not loggedin():
        return redirect(url_for('login'))

    username = session['username']
    # forbidden if user does not have access (operator for app or admin)
    if not is_admin(username):
        abort(403)

    # if form was submitted
    if request.method == 'POST':
        # create user
        u = request.form['username']
        pw = request.form['password']
        fn = request.form['firstname']
        ln = request.form['lastname']
        a = request.form.get('admin') is not None
        v = request.form.get('can_vote') is not None
        # TODO: check that users doesn't exist

        create_user(u, fn, ln, pw, a, v)

        return redirect(url_for('admin_users'))

    # if page was requested
    else:
        return render_template('new_user.html.j2', username=username)


@app.route('/ajax/admin/remove_user', methods=['POST'])
def ajax_admin_remove_user():
    if loggedin():
        if is_admin(session['username']):
            user = request.json['user']
            if user_exists(user):
                # remove user
                db, c = get_dbc()
                c.execute('''DELETE FROM user
                    WHERE username = ?''',
                          (user,))
                db.commit()
                return jsonify(success='True', user=user)
    # if anything went wrong
    return jsonify(success='False')


@app.route('/ajax/user_query')
def user_query():
    users = []
    searchterm = request.args.get('searchterm')
    # only search if searchterm is not empty
    if searchterm:
        db, c = get_dbc()
        # get all users that begin with searchterm
        var = searchterm + '%'
        c.execute('''SELECT username
            FROM user
            WHERE username LIKE ?''',
                  (var,))
        result = c.fetchall()
        # extract usernames
        if result is not None:
            users.extend(u['username'] for u in result)
    return jsonify(users=users)


@app.route('/ajax/admin/slots/update', methods=['POST'])
def ajax_admin_slots_update():
    if loggedin():
        if is_admin(session['username']):
            # update slot length
            set_setting('slot_length', int(request.json['slot_length']))
            return ('', 204)
    else:
        abort(403)


@app.route('/ajax/admin/slots/add_slot', methods=['POST'])
def ajax_admin_slots_add_slot():
    if loggedin():
        if is_admin(session['username']):
            # add slot
            db, c = get_dbc()
            c.execute('''INSERT INTO slot
                VALUES (null, ?)''',
                      (request.json['slot'],))
            db.commit()
            return ('', 204)
    else:
        abort(403)


@app.route('/ajax/admin/slots/remove_slot', methods=['POST'])
def ajax_admin_slots_remove_slot():
    if loggedin():
        if is_admin(session['username']):
            # remove slot
            db, c = get_dbc()
            c.execute('''DELETE FROM slot
                WHERE start_time = ?''',
                      (request.json['slot']))
            db.commit()
            return ('', 204)
    else:
        abort(403)


@app.route('/admin/general')
def admin_general():
    # user needs to be logged in
    if not loggedin():
        return redirect(url_for('login'))

    username = session['username']
    # forbidden if user does not have access (operator for app or admin)
    if not is_admin(username):
        abort(403)

    return render_template('admin_general.html.j2', username=username)


@app.route('/ajax/admin/general/recalculate_session', methods=['POST'])
def ajax_admin_general_recalculate_session():
    # user needs to be logged in
    if not loggedin():
        return redirect(url_for('login'))

    username = session['username']
    # forbidden if user does not have access (operator for app or admin)
    if not is_admin(username):
        abort(403)

    set_setting('next_session', next_session(True))
    return ('', 204)
