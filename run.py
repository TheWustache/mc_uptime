#!flask/bin/python
from app import app
import sys

debug = False
if len(sys.argv) >= 2:
    if sys.argv[1] in ['True', 'true', 'T', 't', '1', 'Yes,''yes', 'Y', 'y']:
        debug = True
app.run(debug=debug)
