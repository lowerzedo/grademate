from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from app.routes.routes import bp

db = SQLAlchemy()

app_main = Flask(__name__)

migrate = Migrate()

app_main.config.from_object(Config)
db.init_app(app_main) 
migrate.init_app(app_main, db)
app_main.register_blueprint(bp, url_prefix="/grademate")
