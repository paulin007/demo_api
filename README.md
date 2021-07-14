different way to run the api:
python app.py
flask run
FLASK_ENV=development flask run

INITIALIZE DB
flask db_create # @app.cli.command('db_create')
flask db_drop
flask db_seed
