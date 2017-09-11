from flask import Flask

app = Flask(__name__)
app.secret_key = b'\xa5\xb8n0K~\xdb\x1d\xb2\xb0v\x0f\x03\xc5-\x8c\x94\xeeBI\xb4q\xbc\xac'

from app import views
