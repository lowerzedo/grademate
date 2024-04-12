from flask_cors import CORS
from app import app_main

app = app_main

CORS(app, resources={r"/*": {"origins": "*"}})


if __name__ == "__main__":
    app.run(debug = True)
