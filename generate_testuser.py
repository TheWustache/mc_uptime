from app.user import create_user
import sys
from flask import Flask

app = Flask(__name__)
with app.app_context():
    if len(sys.argv) >= 3:
        create_user(sys.argv[1], 'x', 'y', sys.argv[2], 6)
    else:
        print("Not enough args!")
