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
    
    # Context pushing
    with app.app_context():
        # Initialize extensions
        db.init_app(app)
        jwt.init_app(app)
        migrate.init_app(app, db, compare_type=True)
        
        # Register routes
        from app.routes.routes import bp
        app.register_blueprint(bp, url_prefix="/grademate")
        
        # Setup CORS
        CORS(app, resources={r"/grademate/*": {"origins": "*"}})
        

    from app.errors import blueprint as errors_bp
    app.register_blueprint(errors_bp)


    # db.create_all()
    # db.session.commit()

    return app