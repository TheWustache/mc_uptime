from flask import session, redirect, url_for, render_template, request, abort, jsonify
from app.user import login_user, logout_user, loggedin, is_admin, user_exists, user_has_app, get_availible_id, create_user
from app import app
from app.db import get_dbc
from app.application import app_exists, app_add_user
from app.controller import next_session

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
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/overview')
def overview():
    if loggedin():
        username = session['username']
        # get apps of user
        db, c = get_dbc()
        c.execute('''SELECT app.id, name, slot_length, next_day, next_slot
            FROM app
            JOIN availible ON availible.app_id = app.id
            WHERE availible.user = ?''',
                  (username,))
        result = c.fetchall()
        # TODO: pass next session
        for r in result:
            r['next_day'], r['next_slot'] = next_session(r['id'])
        return render_template('overview.html', username=session['username'], userApps=result)
    else:
        return redirect(url_for('login'))


@app.route('/updatetimes/<int:app_id>', methods=['GET', 'POST'])
def updateTimes(app_id):
    # not found if app doesn't exists
    if not app_exists(app_id):
        abort(404)

    if not loggedin():
        return redirect(url_for('login'))

    username = session['username']
    db, c = get_dbc()
    # if form was submitted
    if request.method == 'POST':
        # TODO: remove 3 slots limit
        # get data from form
        slots = []
        for i in range(1, 4):
            slots.append(
                {'day': request.form['day' + str(i)], 'start_time': request.form['start' + str(i)]})
        # get id of slots
        c.execute('''SELECT slot.id
            FROM slot
            JOIN availible ON slot.availible_id = availible.id
            WHERE availible.user = ?
            AND availible.app_id = ?''',
                  (username, app_id))
        slot_ids = c.fetchall()[:3]
        # save data
        for i in range(3):
            c.execute('''UPDATE slot
            SET day = ?, start_time = ?
            WHERE id = ?''',
                      (slots[i]['day'], slots[i]['start_time'], slot_ids[i]['id']))
        # TODO: Wrap in try block before committing (and abort+notify user on failure)
        db.commit()

        return redirect(url_for('overview'))
    # if page was requested
    else:
        # check if user has access to app
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
                FROM app
                WHERE id = ?''',
                      (app_id,))
            slot_length = c.fetchone()['slot_length']

            # get slots
            c.execute('''SELECT day, start_time
                FROM slot
                JOIN availible ON slot.availible_id = availible.id
                WHERE availible.user = ?''',
                      (username,))
            slots = c.fetchall()

            return render_template('updateTimes.html', username=username, app_name=app_name, slot_length=slot_length, slots=slots)


@app.route('/app/<int:app_id>/settings', methods=['GET'])
def app_settings(app_id):

    # not found if app doesn't exists
    if not app_exists(app_id):
        abort(404)
    # user needs to be logged in
    if not loggedin():
        return redirect(url_for('login'))

    username = session['username']
    # forbidden if user does not have access (operator for app or admin)
    # TODO: implement operator status
    if not is_admin(username):
        abort(403)

    db, c = get_dbc()
    # get app info
    c.execute('''SELECT name, filepath, slot_length, id
        FROM app
        WHERE id = ?''',
              (app_id,))
    result_app = c.fetchone()
    # get app users
    c.execute('''SELECT user.username
        FROM availible
        JOIN user ON user.username = availible.user
        JOIN app ON app.id = availible.app_id
        WHERE app.id = ?''',
              (app_id,))
    result_users = c.fetchall()
    users = list((u['username'] for u in result_users))

    return render_template('app_settings.html', username=username, app=result_app, users=users)


@app.route('/ajax/app/add_user', methods=['POST'])
def ajax_app_add_user():
    if loggedin():
        if is_admin(session['username']):
            user = request.json['user']
            app_id = request.json['app_id']
            if user_exists(user):
                if not user_has_app(user, app_id):
                    # TODO: encapsulate
                    app_add_user(app_id, user)
                    return jsonify(success='True', user=user)
    # if anything went wrong
    return jsonify(success='False')


@app.route('/ajax/app/remove_user', methods=['POST'])
def ajax_app_remove_user():
    if loggedin():
        if is_admin(session['username']):
            user = request.json['user']
            app_id = request.json['app_id']
            if user_exists(user):
                if user_has_app(user, app_id):
                    # remove user from app
                    db, c = get_dbc()
                    c.execute('''DELETE FROM availible
                        WHERE user = ?
                        AND app_id = ?''',
                              (user, app_id))
                    db.commit()
                    return jsonify(success='True', user=user)
    # if anything went wrong
    return jsonify(success='False')


@app.route('/ajax/app/update_settings', methods=['POST'])
def ajax_app_update_settings():
    if loggedin():
        if is_admin(session['username']):
            json = request.json
            db, c = get_dbc()
            c.execute('''UPDATE app
                SET name = ?, filepath = ?, slot_length = ?
                WHERE id = ?''',
                      (json['name'], json['filepath'], json['slot_length'], json['app_id']))
            db.commit()
    return jsonify(name=request.json['name'])


@app.route('/app/<int:app_id>')
def app_overview(app_id):
    # not found if app doesn't exists
    if not app_exists(app_id):
        abort(404)
    # user needs to be logged in
    if not loggedin():
        return redirect(url_for('login'))

    username = session['username']
    db, c = get_dbc()
    # get app info
    c.execute('''SELECT name, slot_length, id
        FROM app
        WHERE id = ?''',
              (app_id,))
    result_app = c.fetchone()
    # get app users
    c.execute('''SELECT user.username
        FROM availible
        JOIN user ON user.username = availible.user
        JOIN app ON app.id = availible.app_id
        WHERE app.id = ?''',
              (app_id,))
    result_users = c.fetchall()
    users = list((u['username'] for u in result_users))

    return render_template('app.html', username=username, app=result_app, users=users, admin=is_admin(username))


@app.route('/admin')
def admin_panel():
    # user needs to be logged in
    if not loggedin():
        return redirect(url_for('login'))

    username = session['username']
    # forbidden if user does not have access (operator for app or admin)
    # TODO: implement operator status
    if not is_admin(username):
        abort(403)

    db, c = get_dbc()
    # get all apps
    c.execute('''SELECT name, id
        FROM app''')
    result_apps = c.fetchall()

    # get all users
    c.execute('''SELECT username
        FROM user''')
    result_users = c.fetchall()
    users = list((u['username'] for u in result_users))

    return render_template('admin_panel.html', username=username, apps=result_apps, users=users)


@app.route('/admin/new_app', methods=['GET', 'POST'])
def new_app():
    # user needs to be logged in
    if not loggedin():
        return redirect(url_for('login'))

    username = session['username']
    # forbidden if user does not have access (operator for app or admin)
    if not is_admin(username):
        abort(403)

    return render_template('new_app.html')


@app.route('/admin/new_user', methods=['GET', 'POST'])
def new_user():
    #TODO: encapsulate this shite
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

        return redirect(url_for('admin_panel'))

    # if page was requested
    else:
        return render_template('new_user.html', username=username)


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


@app.route('/ajax/admin/new_app/submit', methods=['POST'])
def ajax_admin_newapp_submit():
    # TODO: encapsulate maybe?
    db, c = get_dbc();
    name = request.json['name']
    filepath = request.json['filepath']
    # create new app
    c.execute('''INSERT INTO app (name, filepath)
        VALUES (?, ?)''',
        (name, filepath))
    db.commit()
    # get app id
    app_id = c.lastrowid
    # add users
    for u in request.json['users']:
        app_add_user(app_id, u)
    return ('', 204);


@app.route('/ajax/admin/remove_app', methods=['POST'])
def ajax_admin_remove_app():
    if loggedin():
        if is_admin(session['username']):
            app_id = request.json['app_id']
            if app_exists(app_id):
                # remove app
                db, c = get_dbc()
                c.execute('''DELETE FROM app
                    WHERE id = ?''',
                          (app_id,))
                db.commit()
                return jsonify(success='True', app_id=app_id)
    # if anything went wrong
    return jsonify(success='False')
