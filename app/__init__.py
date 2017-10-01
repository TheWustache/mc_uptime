from flask import Flask

app = Flask(__name__)
app.secret_key = b'\xa5\xb8n0K~\xdb\x1d\xb2\xb0v\x0f\x03\xc5-\x8c\x94\xeeBI\xb4q\xbc\xac'
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

from app import views
from app.db import teardown_db
