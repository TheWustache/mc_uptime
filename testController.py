from flask import Flask
from app.controller import next_session

app = Flask(__name__)
with app.app_context():
    print(next_session(1))
