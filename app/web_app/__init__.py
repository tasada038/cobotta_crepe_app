from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)    # Create Flask Instance
app.secret_key = b'random string...'    # Session Secret

app.config.from_object('web_app.config')

db = SQLAlchemy(app)
from web_app.models import customer

import web_app.views