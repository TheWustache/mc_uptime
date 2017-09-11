from flask import Flask, session, redirect, url_for, render_template, request
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
    return render_template('login.html')

# set the secret key
app.secret_key = '\xa5\xb8n0K~\xdb\x1d\xb2\xb0v\x0f\x03\xc5-\x8c\x94\xeeBI\xb4q\xbc\xac'
