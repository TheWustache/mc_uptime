import sys
from app.user import user_exists
from flask import Flask

app = Flask(__name__)
with app.app_context():
    if len(sys.argv) >= 2:
        if user_exists(sys.argv[1]):
            print(sys.argv[1] + " exists!")
        else:
            print(sys.argv[1] + " does not exist!")
