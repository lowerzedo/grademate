from flask_cors import CORS
from app import app_main

app = app_main

CORS(app)

if __name__ == "__main__":
    app.run(debug = True)
