from flask import Flask
from app.settings import set_setting
from app.next_session import next_session

app = Flask(__name__)
with app.app_context():
    print(next_session(True))
