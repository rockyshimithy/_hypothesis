from flask_migrate import Migrate

from hypothesis.factory import create_app, db

app = create_app()
migrate = Migrate(app, db)
