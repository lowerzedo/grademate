activate venv:
- source venv/bin/activate

run the server:
- export FLASK_DEBUG=TRUE
- flask run

if added changes to db Models:
- flask db migrate
- flask db upgrade
