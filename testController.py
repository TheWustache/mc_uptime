from flask import Flask
from app.settings import set_setting
from app.next_session import optimal_slot

app = Flask(__name__)
with app.app_context():
    optimal_slot()
