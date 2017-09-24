from flask import session, redirect, url_for, render_template, request, abort, jsonify
from app.user import login_user, logout_user, loggedin, is_admin, user_exists, user_has_app, get_availible_id, create_user
from app import app
from app.db import get_dbc

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
        return render_template('overview.html', username=session['username'])
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
        return redirect(url_for('overview'))

    # if page was requested
    else:
        return render_template('updateTimes.html', username=username)






@app.route('/admin')
def admin_panel():
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

    return render_template('admin_panel.html', username=username, users=users)




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
