from urllib import response
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate(db)



def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    app_context = app.app_context()
    app_context.push()

    # Initialize DB
    db.init_app(app)

    jwt.init_app(app)

    # Initialize migrate
    migrate.init_app(app, db, compare_type=True)


    from app.routes.routes import bp
    app.register_blueprint(bp, url_prefix="/grademate")

    # from app.errors import blueprint as errors_bp
    # app.register_blueprint(errors_bp)


    db.create_all()
    db.session.commit()

    return app