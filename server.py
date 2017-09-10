from flask import Flask, session, redirect, url_for, current_app, request
app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        session.pop('username', None)
        return 'index'
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = 'set'
        return redirect(url_for('index'))
    return current_app.send_static_file('login.html')

# set the secret key.  keep this really secret:
app.secret_key = '\xa5\xb8n0K~\xdb\x1d\xb2\xb0v\x0f\x03\xc5-\x8c\x94\xeeBI\xb4q\xbc\xac'
