from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import logging

app = Flask(__name__)
csrf = CSRFProtect(app)

if len(app.logger.handlers) >0:
  app.logger.handlers[0].setFormatter(logging.Formatter("[%(asctime)s] - %(message)s"))
db = SQLAlchemy()
from app import routes