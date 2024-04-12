from dotenv import load_dotenv
import os

load_dotenv()


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    JWT_SECRET_KEY = os.environ.get("FLASK_JWT_SECRET_KEY")


