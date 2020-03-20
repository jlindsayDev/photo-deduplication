from flask import Flask
from . import Config

app = Flask(__name__)
app.config.from_object(Config)

from . import views