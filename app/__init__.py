import os

from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_cors import CORS

template_dir = os.path.abspath('../Myblog_frontend/templates')
static_dir = os.path.abspath('../Myblog_frontend/static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# CORS(app)

from app import routes, models
