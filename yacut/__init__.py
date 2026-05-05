from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .views import views_bp
from .api_views import api_bp
from .error_handlers import errors_bp

app.register_blueprint(views_bp)
app.register_blueprint(api_bp)
app.register_blueprint(errors_bp)
