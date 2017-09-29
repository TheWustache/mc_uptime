from flask import Flask
from app.controller import next_session
from app.settings import set_setting

app = Flask(__name__)
with app.app_context():
    set_setting('slot_length', 6)
