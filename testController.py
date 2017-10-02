from flask import Flask
from app.settings import set_setting
from app.next_session import next_session
from app.controller import Controller
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
with app.app_context():
    s = BackgroundScheduler()
    s.start()
    c = Controller()
